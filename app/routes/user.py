from fastapi import APIRouter, Depends
from app.schemas.user import UserRead
from app.core.deps import get_current_user
from app.db.models.user import User

router = APIRouter(prefix="/users",tags=["Users"])

@router.get("/me",response_model=UserRead)
def read_me(current_user:User= Depends(get_current_user)):
    return current_user

@router.get("/protected")
async def protected_route(current_user:User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.email}!"}
