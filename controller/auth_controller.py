# controllers/auth_controller.py

from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from model.user import User
from util.auth import get_password_hash, verify_password, create_access_token
import os

async def handle_google_callback(request: Request, db: Session, oauth):
    token = await oauth.google.authorize_access_token(request)
    resp = await oauth.google.get("userinfo", token=token)
    user_info = resp.json()

    email = user_info.get("email")
    name = user_info.get("name")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            username=name,
            email=email,
            hashed_password="google_oauth",
            role="user"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token(data={"sub": user.username})
    return RedirectResponse(url=f"/sendemail.html?token={access_token}")

async def handle_facebook_callback(request: Request, db: Session, oauth):
    token = await oauth.facebook.authorize_access_token(request)
    resp = await oauth.facebook.get("me?fields=id,name,email", token=token)
    user_info = resp.json()

    email = user_info.get("email")
    name = user_info.get("name")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            username=name,
            email=email,
            hashed_password="facebook_oauth",
            role="user"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token(data={"sub": user.username})
    return RedirectResponse(url=f"/sendemail.html?token={access_token}")

def register_user(user, db: Session):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Tên đăng nhập đã tồn tại")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email đã tồn tại")

    hashed_password = get_password_hash(user.password)
    new_user = User(
    username=user.username,
    email=user.email,
    hashed_password=hashed_password,
    role=user.role  # ← Lấy từ request
)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(form_data, db: Session):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Sai thông tin đăng nhập")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}