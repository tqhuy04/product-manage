from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

# from model import product, categorie, user
from database import engine, Base
 
from routers import auth
# from routers import product
# from routers import categorie

app = FastAPI()
@app.get("/")
def hello():
    return {"message": "Hello FastAPI"}
# app.include_router(auth.router)