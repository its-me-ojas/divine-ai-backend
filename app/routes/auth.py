from fastapi import APIRouter, status
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from starlette.exceptions import HTTPException

from app.core.security import create_access_token, hash_password, verify_password
from app.db.models.user import User
from app.db.session import get_session
from app.schemas.user import UserCreate, UserLogin, UserRead

router = APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    hashed_pw = hash_password(user.password)
    db_user=User(
        email=user.email,
        hashed_password=hashed_pw,
        preferred_language=user.preferred_language,
        verse_theme=user.verse_theme,
    )

    try:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

@router.post("/login")
def login(
    form_data:OAuth2PasswordRequestForm= Depends(),
    # user:UserLogin,
    session:Session=Depends(get_session)
):
    statement=select(User).where(User.email==form_data.username)
    result=session.exec(statement).first()

    if not result or not verify_password(form_data.password,result.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    token = create_access_token({"sub":str(result.id)})
    return {"access_token":token,"token_type":"bearer"}
