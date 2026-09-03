from fastapi import APIRouter, HTTPException

from ..models.user import UserCreate, UserUpdate
from ..tools.user_tools import (
    create_user,
    list_users,
    find_user,
    update_user,
    delete_user,
)


router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


@router.get("/")
def get_users():
    return list_users()


@router.post("/")
def add_user(data: UserCreate):

    result = create_user(
        email=str(data.email),
        name=data.name,
        phone=data.phone,
        city=data.city,
        country=data.country,
    )

    if not result["success"]:
        raise HTTPException(
            status_code=409,
            detail=result["message"]
        )

    return result


@router.get("/find")
def search_user(
    email: str = None,
    name: str = None,
):
    return find_user(
        email=email,
        name=name
    )


@router.patch("/{email}")
def edit_user(
    email: str,
    data: UserUpdate
):

    result = update_user(
        email=email,
        name=data.name,
        phone=data.phone,
        city=data.city,
        country=data.country,
    )

    if not result["success"]:
        raise HTTPException(
            status_code=404,
            detail=result["message"]
        )

    return result


@router.delete("/{email}")
def remove_user(email: str):

    result = delete_user(email)

    if not result["success"]:
        raise HTTPException(
            status_code=404,
            detail=result["message"]
        )

    return result