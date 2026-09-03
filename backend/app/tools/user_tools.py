from bson import ObjectId
from datetime import datetime

from ..database import users_collection


def serialize_user(user):
    if not user:
        return None

    return {
        "id": str(user["_id"]),
        "email": user.get("email"),
        "name": user.get("name"),
        "phone": user.get("phone"),
        "city": user.get("city"),
        "country": user.get("country"),
    }


def create_user(
    email: str,
    name: str = None,
    phone: str = None,
    city: str = None,
    country: str = None,
):
    """Create a new user in the database."""

    email = email.lower().strip()

    existing = users_collection.find_one({
        "email": email
    })

    if existing:
        return {
            "success": False,
            "message": "A user with this email already exists.",
            "user": serialize_user(existing)
        }

    user = {
        "email": email,
        "name": name,
        "phone": phone,
        "city": city,
        "country": country,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    
    result = users_collection.insert_one(user)

    user["_id"] = result.inserted_id

    return {
        "success": True,
        "message": "User created successfully.",
        "user": serialize_user(user)
    }


def find_user(
    email: str = None,
    name: str = None,
):
    """Find users by email or name."""

    query = {}

    if email:
        query["email"] = email.lower().strip()

    if name:
        query["name"] = {
            "$regex": f"^{name.strip()}$",
            "$options": "i"
        }

    users = list(
        users_collection.find(query)
    )

    return {
        "success": True,
        "count": len(users),
        "users": [
            serialize_user(user)
            for user in users
        ]
    }


def list_users():
    """Return all users."""

    users = list(
        users_collection.find({})
    )

    return {
        "success": True,
        "count": len(users),
        "users": [
            serialize_user(user)
            for user in users
        ]
    }


def update_user(
    email: str,
    name: str = None,
    phone: str = None,
    city: str = None,
    country: str = None,
):
    """Update an existing user's information."""

    email = email.lower().strip()

    updates = {}

    if name is not None:
        updates["name"] = name

    if phone is not None:
        updates["phone"] = phone

    if city is not None:
        updates["city"] = city

    if country is not None:
        updates["country"] = country

    if not updates:
        return {
            "success": False,
            "message": "No fields were provided for update."
        }

    updates["updated_at"] = datetime.utcnow()

    user = users_collection.find_one_and_update(
        {"email": email},
        {"$set": updates},
        return_document=True
    )

    if not user:
        return {
            "success": False,
            "message": "User not found."
        }

    return {
        "success": True,
        "message": "User updated successfully.",
        "user": serialize_user(user)
    }


def delete_user(email: str):
    """Delete a user by email."""

    email = email.lower().strip()

    user = users_collection.find_one_and_delete({
        "email": email
    })

    if not user:
        return {
            "success": False,
            "message": "User not found."
        }

    return {
        "success": True,
        "message": "User deleted successfully.",
        "user": serialize_user(user)
    }