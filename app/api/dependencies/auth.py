from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID
from app.services.jwt_auth import jwt_auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

def get_payload(token: str = Depends(oauth2_scheme)):
    payload = jwt_auth.decode_token(token)
    return payload

def require_scope(permission: str):
    def checker(
        id: UUID,
        payload: dict = Depends(get_payload)
    ):
        scopes = payload.get("scopes", [])

        if permission not in scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Missing permission"
            )

        if str(id) != payload.get("sub"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed"
            )

        return payload

    return checker