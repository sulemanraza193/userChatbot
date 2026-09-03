from fastapi import APIRouter, HTTPException

from ..database import admins_collection
from ..models.admin import AdminLogin


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(data: AdminLogin):

    email = str(data.email).lower().strip()

    admin = admins_collection.find_one({
        "email": email
    })

    if not admin:
        raise HTTPException(
            status_code=401,
            detail="Email is not authorized"
        )

    return {
        "success": True,
        "message": "Login successful",
        "admin": {
            "id": str(admin["_id"]),
            "name": admin.get("name"),
            "email": admin.get("email")
        }
    }