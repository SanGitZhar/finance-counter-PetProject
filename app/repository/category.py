from sqlalchemy.orm import Session

from app.models import Category

def create_category(db: Session, user_id: int, category_name: str) -> Category:
    category = Category(user_id=user_id, name=category_name)
    db.add(category)
    db.flush()
    return category

    


def get_all_categories(db: Session, user_id: int):
    return db.query(Category).filter(Category.user_id ==user_id).all()