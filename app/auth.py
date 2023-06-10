import datetime

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.config import app


# Replace these with your desired username, password, and secret keys
USERNAME = "username"
PASSWORD = "password"
ACCESS_TOKEN_SECRET_KEY = "your_access_token_secret_key"
REFRESH_TOKEN_SECRET_KEY = "your_refresh_token_secret_key"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate(username: str, password: str):
    if username == USERNAME and password == PASSWORD:
        return True
    return False


def create_jwt_token(
        data: dict,
        secret_key: str,
        expires_delta: datetime.timedelta):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.datetime.utcnow() + expires_delta})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt


def create_access_token(data: dict):
    expires_delta = datetime.timedelta(minutes=15)
    return create_jwt_token(data, ACCESS_TOKEN_SECRET_KEY, expires_delta)


def create_refresh_token(data: dict):
    expires_delta = datetime.timedelta(days=7)
    return create_jwt_token(data, REFRESH_TOKEN_SECRET_KEY, expires_delta)


def decode_jwt_token(token: str, secret_key: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt_token(token, ACCESS_TOKEN_SECRET_KEY)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    username = payload.get("sub")
    if username is None or username != USERNAME:
        raise HTTPException(status_code=401, detail="Invalid access token")
    return username


@app.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Для аутентификации"""
    user_auth = authenticate(form_data.username, form_data.password)
    if not user_auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": form_data.username})
    refresh_token = create_refresh_token(data={"sub": form_data.username})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@app.post("/token/refresh")
async def refresh_token(refresh_token: str):
    """Для обновления access токена"""
    payload = decode_jwt_token(refresh_token, REFRESH_TOKEN_SECRET_KEY)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    username = payload.get("sub")
    if username is None or username != USERNAME:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    new_access_token = create_access_token(data={"sub": username})
    return {"access_token": new_access_token, "token_type": "bearer"}
