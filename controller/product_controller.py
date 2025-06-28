from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
import model.product
import model, schemas
import schemas.product

def search_products(q: str , db: Session):
    return db.query(model.product.Product).filter(
        func.lower(model.product.Product.name).like (f"%{q.lower()}%")
    ).all()

def get_all_products(db: Session):
    return db.query(model.product.Product).all()

def get_product_by_id(product_id: int , db: Session):
    db_product = db.query(model.product.Product).filter(
        model.product.Product.id == product_id
    ).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    return db_product

def create_product(product: schemas.product.ProductCreate, db: Session):
    db_product = model.product.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(product_id: int, product: schemas.product.Product, db: Session):
    db_product = db.query(model.product.Product).filter(
        model.product.Product.id == product_id
    ).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(product_id: int, db: Session):
    db_product = db.query(model.product.Product).filter(
        model.product.Product.id == product_id
    ).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted"}


def get_products_by_category(categorie_id: int, db: Session):
    return db.query(model.product.Product).filter(
        model.product.Product.categorie_id == categorie_id
    ).all()
