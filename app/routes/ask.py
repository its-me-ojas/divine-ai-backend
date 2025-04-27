from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.db.models.user import User
from app.schemas.ask import AskRequest
from app.services.groq import get_groq_response


router = APIRouter(prefix="/ask",tags=["Ask"])

@router.post("/")
async def ask_groq(
    request: AskRequest,
    current_user :User = Depends(get_current_user),
):
    user_message = request.prompt
    if not user_message:
        return {"error": "No message provided"}

    groq_response = await get_groq_response(user_message)

    return {"response": groq_response}
