from pydantic import BaseModel, Field, EmailStr, HttpUrl, field_validator
from datetime import datetime, timezone
from uuid import UUID, uuid4


class UserBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    age: int = Field(ge=0, le=120)
    email: EmailStr
    pfp_external_link: HttpUrl | None = None


class UserCreate(UserBase):
    id: UUID = Field(default_factory=uuid4)
    password: str = Field(
        min_length=8,
        max_length=50,
        description="Password must contain letters, numbers, and symbols",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, pw: str):

        if not any(c.isalpha() for c in pw):
            raise ValueError("Password must contain at least one letter")

        if not any(c.isdigit() for c in pw):
            raise ValueError("Password must contain at least one digit")

        symbols = "@$!%*#?&^()_-+="
        if not any(c in symbols for c in pw):
            raise ValueError("Password must contain at least one symbol")

        return pw


class UserRead(UserBase):
    id: UUID
    created_at: datetime
    model_config = {"from_attributes": True}