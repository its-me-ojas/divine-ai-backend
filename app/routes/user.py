from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.schemas.user import UserRead, UserUpdate
from app.core.deps import get_current_user
from app.db.models.user import User
from app.db.session import get_session

router = APIRouter(prefix="/users",tags=["Users"])

@router.get("/me",response_model=UserRead)
def read_me(current_user:User = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=UserRead)
def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update the current user's profile information"""
    # Update user attributes
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    # Save changes to database
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user

@router.get("/protected")
async def protected_route(current_user:User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.email}!"}
