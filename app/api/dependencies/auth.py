from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.services.JWTAuth import JWTAuth
from app.core.settings import settings

jwt_auth = JWTAuth(settings.SECRET_KEY)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_payload(token: str = Depends(oauth2_scheme)):
    payload = jwt_auth.decode_token(token)
    return payload

def require_scope(permission: str):
    def checker(payload: dict = Depends(get_payload)):
        scopes = payload.get("scopes", [])

        if permission not in scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permission: {permission}"
            )

        return payload

    return checker