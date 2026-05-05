from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session

from app.dependency import get_current_user, get_db
from app.schemas import CategoryReponse, CreateCategoryRequest
from app.service import category as category_service
from app.models import User

router = APIRouter()

@router.post("/categories", response_model=CategoryReponse)
def create_category(category: CreateCategoryRequest, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    return category_service.create_category(db, current_user, category)

@router.get("/categories", response_model=list[CategoryReponse])
def get_categories_list(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return category_service.get_all_categories(db, current_user)