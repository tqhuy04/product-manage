import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from model import product, category
from database import engine, Base
from routers import auth, email, admin_product, client_product
from routers import client_categories, admin_categories

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
    secret_key="qpouttertyuiop",
)

#  Đường dẫn tuyệt đối đến thư mục 'view/public'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "view", "public")

# Routers
app.include_router(auth.router)
app.include_router(admin_product.router)
app.include_router(client_product.router)
app.include_router(client_categories.router)
app.include_router(admin_categories.router)

app.include_router(email.router, prefix="/api", tags=["Email"])
# Mount static files
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")


