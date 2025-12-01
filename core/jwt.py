from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from datetime import datetime,timezone
from config import settings
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
password_hash = PasswordHash.recommended()
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt










