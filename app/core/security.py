from datetime import timedelta
from fastapi.security.oauth2 import OAuth2PasswordBearer
from typing_extensions import Union
from jose import jwt
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY= "divine_secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES= 7*24*60 # 7 days

def hash_password(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(password:str,hashed:str)-> bool:
    return pwd_context.verify(password,hashed)

def create_access_token(data:dict,expires_delta:Union[timedelta,None]=None):
    to_encode= data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encoded_jwt

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="/auth/login")
