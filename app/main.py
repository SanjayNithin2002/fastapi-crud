from fastapi import FastAPI, Response, status, HTTPException

from app.core.middlewares.security_headers import SecurityHeadersMiddleware

app = FastAPI(
    title = "FastAPI Postgres CRUD", 
    version = "1.0.0"
)

app.add_middleware(SecurityHeadersMiddleware)
# Use this for success
@app.get("/health", status_code = status.HTTP_200_OK)
def healthcheck():
    return {"status": "ok"}

# Use this for failure
@app.get("/health-2")
def healthcheck_2():
    raise HTTPException(status_code=404, detail="Not accesible")
