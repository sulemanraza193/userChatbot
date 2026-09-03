from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..services.gemini_service import chat_with_gemini


router = APIRouter(
    prefix="/api/chat",
    tags=["AI Chat"]
)


class ChatRequest(BaseModel):
    message: str


@router.post("/")
def chat(data: ChatRequest):

    if not data.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message is required"
        )

    try:

        response = chat_with_gemini(
            data.message
        )

        return {
            "success": True,
            "message": response
        }

    except Exception as error:

        print("CHAT ERROR:", error)

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )