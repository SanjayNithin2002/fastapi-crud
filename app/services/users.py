from sqlalchemy.orm import Session
from uuid import UUID

from app.models.users import User
from app.schemas.users import UserCreate

def create_user(db: Session, user_in: UserCreate) -> User:
    user = User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        age=user_in.age,
        email=user_in.email,
        password=user_in.password,
        pfp_external_link=user_in.pfp_external_link,
    )

    db.add(user)
    db.commit()
    db.refresh(user)  # reload (fills id, created_at)

    return user

def get_user_by_id(db: Session, user_id: UUID) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def list_users(db: Session) -> list[User]:
    return db.query(User).all()

def update_user(
    db: Session,
    user_id: UUID,
    first_name: str | None = None,
    last_name: str | None = None,
    age: int | None = None,
    pfp_external_link: str | None = None,
) -> User | None:
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    if first_name is not None:
        user.first_name = first_name

    if last_name is not None:
        user.last_name = last_name

    if age is not None:
        user.age = age

    if pfp_external_link is not None:
        user.pfp_external_link = pfp_external_link

    db.commit()
    db.refresh(user)

    return user

def delete_user(db: Session, user_id: UUID) -> bool:
    user = get_user_by_id(db, user_id)
    if not user:
        return False

    db.delete(user)
    db.commit()
    return True