from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

from schemas.auth import UserCreate, UserOut, Token
from model.user import User
from database import get_db
from dependencies.auth import get_current_user
from controller import auth_controller
from authlib.integrations.starlette_client import OAuth
import os

router = APIRouter(prefix="/auth", tags=["Authentication"])

# ========== CẤU HÌNH OAUTH ==========

oauth = OAuth()

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url="https://accounts.google.com/o/oauth2/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    authorize_params={"access_type": "offline"},
    client_kwargs={"scope": "email profile"},
)

oauth.register(
    name="facebook",
    client_id=os.getenv("FACEBOOK_CLIENT_ID"),
    client_secret=os.getenv("FACEBOOK_CLIENT_SECRET"),
    access_token_url="https://graph.facebook.com/v10.0/oauth/access_token",
    authorize_url="https://www.facebook.com/v10.0/dialog/oauth",
    api_base_url="https://graph.facebook.com/v10.0/",
    client_kwargs={"scope": "email"},
)

# ========== ROUTES ==========

@router.get("/google-login")
async def google_login(request: Request):
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google-callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    return await auth_controller.handle_google_callback(request, db, oauth)

@router.get("/facebook-login")
async def facebook_login(request: Request):
    redirect_uri = os.getenv("FACEBOOK_REDIRECT_URI")
    return await oauth.facebook.authorize_redirect(request, redirect_uri)

@router.get("/facebook-callback")
async def facebook_callback(request: Request, db: Session = Depends(get_db)):
    return await auth_controller.handle_facebook_callback(request, db, oauth)

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return auth_controller.register_user(user, db)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth_controller.login_user(form_data, db)
