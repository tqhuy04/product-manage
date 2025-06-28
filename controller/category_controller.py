from sqlalchemy.orm import Session
from model.category import Category
from schemas.category import CategorieCreate

def get_all_categories(db: Session):
    return db.query(Category).all()

def get_category_by_id(categorie_id: int, db: Session):
    return db.query(Category).filter(Category.id == categorie_id).first()

def create_category(categorie: CategorieCreate, db: Session):
    new_categorie = Category(**categorie.dict())
    db.add(new_categorie)
    db.commit()
    db.refresh(new_categorie)
    return new_categorie

def update_category(categorie_id: int, data: CategorieCreate, db: Session):
    categorie = db.query(Category).filter(Category.id == categorie_id).first()
    if not categorie:
        raise Exception("Categorie not found")
    for key, value in data.dict().items():
        setattr(categorie, key, value)
    db.commit()
    db.refresh(categorie)
    return categorie

def delete_category(categorie_id: int, db: Session):
    categorie = db.query(Category).filter(Category.id == categorie_id).first()
    if not categorie:
        raise Exception("Categorie not found")
    db.delete(categorie)
    db.commit()
    return {"message": "Xoá thành công"}
