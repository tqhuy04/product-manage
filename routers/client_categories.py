from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import model.category
import model, schemas
import schemas.category

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/",response_model=list[schemas.category.Categorie])
def get_categories( db: Session = Depends(get_db)):
    return db.query(model.category.Category).all()
@router.get("/{categorie_id}", response_model=schemas.category.Categorie)
def get_categorie(categorie_id : int, db: Session = Depends(get_db)):
    categorie = db.query(model.category.Category).filter(
        model.category.Category.id == categorie_id).first()
    if not categorie:
        raise HTTPException(status_code=404,detail="không tìm thấy danh mục sản phẩm")
    return categorie