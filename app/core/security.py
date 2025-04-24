from datetime import timedelta
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

def create_access_token(data:dict)-> str:
    expire= datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp":expire})
    return jwt.encode(data,SECRET_KEY,ALGORITHM)
