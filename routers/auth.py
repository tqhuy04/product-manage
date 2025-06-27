from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

from schemas.auth import UserCreate, UserOut, Token
from controller.auth_controller import register_user, login_user
from model.user import User
from util.auth import get_password_hash, verify_password, create_access_token
from database import get_db
from dependencies.auth import get_current_user
from util.email import send_login_notification
import os

from authlib.integrations.starlette_client import OAuth

router = APIRouter(prefix="/auth", tags=["auth"])

# ========== ĐĂNG KÝ ==========
@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db)  

# ========== ĐĂNG NHẬP ==========
@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return login_user(form_data, db)  
