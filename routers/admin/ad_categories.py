from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from model.category import Category
from schemas.category import Categorie, CategorieCreate
from dependencies.auth import get_current_user
from model.user import User

router = APIRouter(prefix="/admin/categories", tags=["Admin Categories"])


def check_admin(user: User):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Không đủ quyền")


@router.post("/", response_model=Categorie)
def post_categorie(
    categorie: CategorieCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_admin(current_user)
    db_categorie = Category(**categorie.dict())
    db.add(db_categorie)
    db.commit()
    db.refresh(db_categorie)
    return db_categorie


@router.put("/{categorie_id}", response_model=Categorie)
def update_categorie(
    categorie_id: int,
    categorie: CategorieCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_admin(current_user)
    db_categorie = db.query(Category).filter(Category.id == categorie_id).first()
    if not db_categorie:
        raise HTTPException(status_code=404, detail="Không tìm thấy")
    for key, value in categorie.dict().items():
        setattr(db_categorie, key, value)
    db.commit()
    db.refresh(db_categorie)
    return db_categorie


@router.delete("/{categorie_id}")
def delete_categorie(
    categorie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_admin(current_user)
    db_categorie = db.query(Category).filter(Category.id == categorie_id).first()
    if not db_categorie:
        raise HTTPException(status_code=404, detail="Không tìm thấy")
    db.delete(db_categorie)
    db.commit()
    return {"message": "Xoá thành công"}
