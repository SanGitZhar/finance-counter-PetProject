from fastapi import APIRouter

from app.schemas import UserRequest, UserResponse
from app.service import users as users_service

router = APIRouter()

@router.post("/users", response_model=UserResponse)
def create_user(payload: UserRequest):
    return users_service.create_user(payload)
