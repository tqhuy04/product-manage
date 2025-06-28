from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from controller import product_controller
from schemas.product import Product


router = APIRouter(prefix="/products", tags=["Client Products"])

@router.get("/", response_model=list[Product])
def get_products(db: Session = Depends(get_db)):
    return product_controller.get_all_products(db)

@router.get("/search", response_model=list[Product])
def search_products(q: str = Query(...), db: Session = Depends(get_db)):
    return product_controller.search_products(q, db)

@router.get("/category/{category_id}", response_model=list[Product])
def get_by_category(category_id: int, db: Session = Depends(get_db)):
    return product_controller.get_products_by_category(category_id, db)

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return product_controller.get_product_by_id(product_id, db)
