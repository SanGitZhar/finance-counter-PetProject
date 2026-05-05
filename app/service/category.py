from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas import CategoryReponse, CreateCategoryRequest
from app.models import User
from app.repository import category as category_repository


def create_category(db: Session, current_user: User, category: CreateCategoryRequest) -> CategoryReponse:
    category = category_repository.create_category(db, current_user.id, category.name)
    db.commit()
    return CategoryReponse.model_validate(category)

    
    

def get_all_categories(db: Session, current_user:User) -> list[CategoryReponse]:
    #создать проверку на наличие в репозитории и вызвать
    categories = category_repository.get_all_categories(db, current_user.id)
    return [CategoryReponse.model_validate(category) for category in categories]