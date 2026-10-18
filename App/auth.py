from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from datetime import datetime, timedelta
from App.config import settings
from typing import Optional
from App.schemas import TokenData
from fastapi import HTTPException

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

#Verifica password
def verify_pwd(plain_pwd:str, hashed_pwd:str) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)

#Hash password
def get_pwd_hash(password:str) -> str:
    return pwd_context.hash(password)

#Crea Token
def create_access_token(data:dict, expires_delta: Optional[timedelta] = None):

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

#Verifica Token
def verify_token(token:str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email:str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=404,
                detail="Credenziali errate!"
            )
        return TokenData(email=email)
    
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=404,
            detail="Credenziali errate!"
        )
