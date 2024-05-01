from fastapi import APIRouter, HTTPException
from models import User
from database import users_collection
from bson import ObjectId
from datetime import datetime, timezone

router = APIRouter(prefix="/users", tags=["users"])


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "created_at": user["created_at"]
    }


@router.post("/", response_model=User)
async def create_user(user: User):
    user_dict = user.dict()
    user_dict["_id"] = ObjectId()
    user_dict["created_at"] = datetime.now(timezone.utc)
    await users_collection.insert_one(user_dict)
    user_dict["id"] = str(user_dict.pop("_id"))
    user_dict.pop("password")
    return user_dict


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user_dict = user_helper(user)
        user_dict.pop("password")
        return user_dict
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/{user_id}/follow/{follower_id}")
async def follow_user(user_id: str, follower_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        updated_user = await users_collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$addToSet": {"followers": follower_id}},
            return_document=True
        )
        return user_helper(updated_user)
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/{user_id}/unfollow/{follower_id}")
async def unfollow_user(user_id: str, follower_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        updated_user = await users_collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$pull": {"followers": follower_id}},
            return_document=True
        )
        return user_helper(updated_user)
    raise HTTPException(status_code=404, detail="User not found")
