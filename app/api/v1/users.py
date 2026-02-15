from fastapi import APIRouter, HTTPException, status, Response
from app.schemas.users import UserCreate, UserRead
from uuid import UUID

router = APIRouter(tags = ["users"])

users: dict[UUID, UserCreate] = {}

@router.get("/", response_model = list[UserRead])
def get_all_users():
    return list(users.values())

@router.get("/{id}", response_model = UserRead)
def get_user_by_id(id: UUID):
    user = users.get(id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "User not found")
    
    return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = UserRead)
def create_user(user: UserCreate):
    users[user.id] = user
    return user

@router.put("/{id}", response_model = UserRead)
def update_user(id: UUID, user: UserCreate):
    if not id in users:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    updated_user = user.model_copy(update={"id": id})
    users[id] = updated_user
    return updated_user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: UUID):
    if not id in users:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    users.pop(id)
    return

