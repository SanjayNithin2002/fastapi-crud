from fastapi import APIRouter, HTTPException, status, Response, Depends
from app.schemas.users import UserCreate, UserRead, UserAuthRequest, UserAuthResponse
from app.api.dependencies.auth import get_payload, require_scope
from app.services.jwt_auth import jwt_auth
from uuid import UUID

router = APIRouter(tags = ["users"])

users: dict[UUID, UserCreate] = {}

@router.get("/", response_model = list[UserRead])
def get_all_users():
    return list(users.values())

@router.get("/{id}", response_model = UserRead)
def get_user_by_id(id: UUID, payload = Depends(require_scope("get"))):
    user = users.get(id)
    if user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
    
    return user

@router.post("/login", response_model = UserAuthResponse)
def login(user_auth: UserAuthRequest):
    user = next((u for u in users.values() if u.email == user_auth.email), None)
    if user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
    if user.password != user_auth.password:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid password")
    user_payload = {
        "sub": str(user.id), 
        "email": user.email, 
        "scopes": ["get", "delete", "put"]
    }
    return {
        "token": jwt_auth.create_access_token(user_payload)
    }
    
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = UserRead)
def create_user(user: UserCreate):
    users[user.id] = user
    return user

@router.put("/{id}", response_model = UserRead)
def update_user(id: UUID, user: UserCreate, payload = Depends(require_scope("put"))):
    if not id in users:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
    
    updated_user = user.model_copy(update={"id": id})
    users[id] = updated_user
    return updated_user

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_user(id: UUID, payload = Depends(require_scope("delete"))):
    if not id in users:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
    
    users.pop(id)
    return

