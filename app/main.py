from fastapi import FastAPI, Response, status, HTTPException
from app.core.middlewares.security_headers import SecurityHeadersMiddleware
from app.core.config import settings
from app.api.v1.router import router as v1_router

app = FastAPI(
    title = "FastAPI Postgres CRUD", 
    version = "1.0.0", 
    debug = settings.DEBUG
)

# Middlewares
app.add_middleware(SecurityHeadersMiddleware)

# Healthcheck endpoint
@app.get("/health", status_code = status.HTTP_200_OK)
def healthcheck():
    return {"status": "ok"}

# Routers
app.include_router(v1_router, prefix = "/api/v1")
