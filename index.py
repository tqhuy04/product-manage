import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import auth

# Khởi tạo DB nếu chưa có
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key="your-secret-key",
)

#  Đường dẫn tuyệt đối đến thư mục 'view/public'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "view", "public")

# Mount static files
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

# Routers
app.include_router(auth.router)
