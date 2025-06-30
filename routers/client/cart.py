from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from controller import cart_controller
from schemas.cart import CartOut, CartItemCreate, CartItemUpdate
from dependencies.auth import get_current_user
from model.user import User

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/me",response_model=CartOut)
def get_my_cart(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
  
    return cart_controller.get_or_create_cart(db, current_user.id)
@router.post("/add",response_model=CartOut)
def add_item(item: CartItemCreate, db: Session = Depends(get_db), current_user: User =Depends(get_current_user)):
   
    return cart_controller.add_to_cart(db , current_user.id, item.product_id, item.quantity)
@router.put("/item/{item_id}", response_model=CartOut)
def update_item(item_id: int, item: CartItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return cart_controller.update_item(db, current_user.id, item_id, item.quantity)

@router.delete("/item/{item_id}", response_model=CartOut)
def delete_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return cart_controller.remove_item(db, current_user.id, item_id)

@router.delete("/clear", response_model=CartOut)
def clear_all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return cart_controller.clear_cart(db, current_user.id)