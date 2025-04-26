from fastapi import Depends, HTTPException, status
from fastapi.applications import FastAPI
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session, select

from app.db.session import get_session
from app.db.models.user import User
from app.core.security import SECRET_KEY, ALGORITHM,oauth2_scheme

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    statement = select(User).where(User.id == int(user_id))
    user = session.exec(statement).first()
    if user is None:
        raise credentials_exception

    return user
