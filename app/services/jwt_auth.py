from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, status
from app.schemas.users import UserPayload
from app.core.config import settings

class JWTAuth:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(self, user_payload: UserPayload, expiry_minutes: int = 60):
        if not user_payload.get("sub"):
            raise ValueError("JWT payload should contain sub field")
        
        now = datetime.now(timezone.utc)
        default_payload = {
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=expiry_minutes)).timestamp()),
            "iss": "fastapi-crud",
            "aud": "external",
        }
        payload = {**user_payload, **default_payload}
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str):
        try:
            return jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                audience="external",  
                issuer="fastapi-crud", 
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )
            

jwt_auth = JWTAuth(settings.SECRET_KEY)