from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from pydantic import BaseModel

app = FastAPI(title="JWT Authentication Demo")

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"  # Algorithm used to sign the JWT token (e.g., HS256, RS256)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# HTTPBearer automatically inspects the "Authorization: Bearer <token>" header,
# extracts the raw token, and enables the "Authorize" button in Swagger UI (/docs).
security = HTTPBearer()


# Pydantic schemas
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# Create JWT token function
def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # "exp" is the standard expiration timestamp claim
    to_encode.update({"exp": expire})
    
    # Encodes payload with the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Token verification dependency function
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    # credentials.credentials contains only the raw token string (Bearer prefix is already stripped)
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing subject identifier",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired or invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Login API (Authenticates credentials via request body and returns JWT token)
@app.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest):
    # Check credentials (in production, verify against hashed passwords in a database)
    if credentials.username == "admin" and credentials.password == "admin":
        # "sub" (subject) is the standard JWT claim for user identity
        token = create_token(data={"sub": credentials.username})
        return {
            "access_token": token,
            "token_type": "bearer",
        }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )


# Protected API (Protected by token dependency)
# FastAPI runs verify_token automatically and passes the returned payload as current_user
@app.get("/protected")
def protected(current_user: dict = Depends(verify_token)):
    return {
        "message": "Protected API accessed successfully",
        "user": current_user.get("sub"),
    }


if __name__ == "__main__":
    import uvicorn
    # Using "main:app" string allows reload=True to work properly
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)