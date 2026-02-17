from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.database import get_db
from app.schemas.users import (
    UserCreate,
    UserRead,
    UserAuthRequest,
    UserAuthResponse,
)
from app.api.dependencies.auth import require_scope
from app.services.jwt_auth import jwt_auth
from app.services.users import (
    create_user,
    list_users,
    get_user_by_id,
    get_user_by_email,
    update_user,
    delete_user,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserRead])
def get_all_users(db: Session = Depends(get_db)):
    return list_users(db)


@router.get("/{id}", response_model=UserRead)
def get_single_user(
    id: UUID,
    db: Session = Depends(get_db),
    payload=Depends(require_scope("get")),
):
    user = get_user_by_id(db, id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.post("/login", response_model=UserAuthResponse)
def login(user_auth: UserAuthRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_auth.email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.password != user_auth.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
        )

    user_payload = {
        "sub": str(user.id),
        "email": user.email,
        "scopes": ["get", "delete", "put"],
    }

    return {
        "token": jwt_auth.create_access_token(user_payload)
    }


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserRead)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user_in.email)

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    return create_user(db, user_in)


@router.put("/{id}", response_model=UserRead)
def update_user_route(
    id: UUID,
    user_in: UserCreate,
    db: Session = Depends(get_db),
    payload=Depends(require_scope("put")),
):
    updated = update_user(
        db,
        user_id=id,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        age=user_in.age,
        pfp_external_link=user_in.pfp_external_link,
    )

    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return updated


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_route(
    id: UUID,
    db: Session = Depends(get_db),
    payload=Depends(require_scope("delete")),
):
    deleted = delete_user(db, id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return