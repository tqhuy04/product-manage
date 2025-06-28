from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from controller import product_controller
from schemas.product import Product, ProductCreate
from dependencies.auth import get_current_user
from model.user import User
from fastapi import HTTPException

router = APIRouter(prefix="/admin/products", tags=["Admin Products"])

def check_admin(user: User):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Không đủ quyền")

@router.post("/", response_model=Product)
def create(product: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_admin(current_user)
    return product_controller.create_product(product, db)

@router.put("/{product_id}", response_model=Product)
def update(product_id: int, product: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_admin(current_user)
    return product_controller.update_product(product_id, product, db)

@router.delete("/{product_id}")
def delete(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_admin(current_user)
    return product_controller.delete_product(product_id, db)
