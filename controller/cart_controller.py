from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from model.cart import Cart
from model.cart_item import CartItem

def get_or_create_cart(db: Session, user_id: int):
    cart = db.query(Cart).options(joinedload(Cart.items).joinedload(CartItem.product)).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int):
    cart = get_or_create_cart(db, user_id)
    existing_item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.product_id == product_id).first()
    if existing_item:
        existing_item.quantity += quantity
    else:
        new_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.add(new_item)
    db.commit()
    db.refresh(cart)
    return cart

def update_item(db: Session, user_id: int, item_id: int, quantity: int):
    item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    cart = db.query(Cart).filter(Cart.id == item.cart_id).first()
    if not cart or cart.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    item.quantity = quantity
    db.commit()
    db.refresh(cart)
    return cart

def remove_item(db: Session, user_id: int, item_id: int):
    item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    cart = db.query(Cart).filter(Cart.id == item.cart_id).first()
    if not cart or cart.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    db.delete(item)
    db.commit()
    db.refresh(cart)
    return cart

def clear_cart(db: Session, user_id: int):
    cart = db.query(Cart).options(joinedload(Cart.items).joinedload(CartItem.product)).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    for item in cart.items:
        db.delete(item)
    db.commit()
    db.refresh(cart)
    return cart