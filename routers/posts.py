from fastapi import APIRouter, HTTPException, UploadFile, File
from models import Post, Comment
from database import posts_collection
from bson import ObjectId
from datetime import datetime, timezone
from typing import List
import aiofiles

router = APIRouter(prefix="/posts", tags=["posts"])

def post_helper(post) -> dict:
    return {
        "id": str(post["_id"]),
        "user_id": post["user_id"],
        "text": post["text"],
        "media": post["media"],
        "likes": post["likes"],
        "comments": post["comments"],
        "reposts": post["reposts"],
        "created_at": post["created_at"],
        "updated_at": post["updated_at"]
    }

@router.post("/", response_model=Post)
async def create_post(post: Post):
    post_dict = post.dict()
    post_dict["_id"] = ObjectId()
    post_dict["created_at"] = datetime.now(timezone.utc)
    post_dict["updated_at"] = datetime.now(timezone.utc)
    await posts_collection.insert_one(post_dict)
    post_dict["id"] = str(post_dict.pop("_id"))
    return post_dict

@router.get("/", response_model=List[Post])
async def get_all_posts():
    posts = await posts_collection.find().to_list(1000)
    return [post_helper(post) for post in posts]

@router.get("/{post_id}", response_model=Post)
async def get_post(post_id: str):
    post = await posts_collection.find_one({"_id": ObjectId(post_id)})
    if post:
        return post_helper(post)
    raise HTTPException(status_code=404, detail="Post not found")

@router.put("/{post_id}", response_model=Post)
async def update_post(post_id: str, post: Post):
    post_dict = post.dict()
    post_dict.pop("id", None)
    post_dict["updated_at"] = datetime.now(timezone.utc)
    updated_post = await posts_collection.find_one_and_update(
        {"_id": ObjectId(post_id)},
        {"$set": post_dict},
        return_document=True
    )
    if updated_post:
        return post_helper(updated_post)
    raise HTTPException(status_code=404, detail="Post not found")

@router.delete("/{post_id}")
async def delete_post(post_id: str):
    deleted_post = await posts_collection.find_one_and_delete({"_id": ObjectId(post_id)})
    if deleted_post:
        return {"message": "Post deleted"}
    raise HTTPException(status_code=404, detail="Post not found")

@router.post("/{post_id}/like/{user_id}")
async def like_post(post_id: str, user_id: str):
    post = await posts_collection.find_one({"_id": ObjectId(post_id)})
    if post:
        if user_id in post["likes"]:
            post["likes"].remove(user_id)
        else:
            post["likes"].append(user_id)
        updated_post = await posts_collection.find_one_and_update(
            {"_id": ObjectId(post_id)},
            {"$set": {"likes": post["likes"]}},
            return_document=True
        )
        return post_helper(updated_post)
    raise HTTPException(status_code=404, detail="Post not found")

@router.post("/{post_id}/comment", response_model=Post)
async def add_comment(post_id: str, comment: Comment):
    comment_dict = comment.dict()
    comment_dict["created_at"] = datetime.now(timezone.utc)
    updated_post = await posts_collection.find_one_and_update(
        {"_id": ObjectId(post_id)},
        {"$push": {"comments": comment_dict}},
        return_document=True
    )
    if updated_post:
        return post_helper(updated_post)
    raise HTTPException(status_code=404, detail="Post not found")

@router.post("/{post_id}/repost/{user_id}")
async def repost(post_id: str, user_id: str):
    post = await posts_collection.find_one({"_id": ObjectId(post_id)})
    if post:
        new_post = Post(
            user_id=user_id,
            text=post["text"],
            media=post["media"],
            likes=[],
            comments=[],
            reposts=0
        )
        new_post_dict = new_post.dict()
        new_post_dict["_id"] = ObjectId()
        new_post_dict["created_at"] = datetime.now(timezone.utc)
        new_post_dict["updated_at"] = datetime.now(timezone.utc)
        await posts_collection.insert_one(new_post_dict)

        updated_post = await posts_collection.find_one_and_update(
            {"_id": ObjectId(post_id)},
            {"$inc": {"reposts": 1}},
            return_document=True
        )
        return post_helper(updated_post)
    raise HTTPException(status_code=404, detail="Post not found")

@router.post("/{post_id}/media")
async def upload_media(post_id: str, file: UploadFile = File(...)):
    post = await posts_collection.find_one({"_id": ObjectId(post_id)})
    if post:
        file_name = file.filename
        file_path = f"media/{file_name}"
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        updated_post = await posts_collection.find_one_and_update(
            {"_id": ObjectId(post_id)},
            {"$push": {"media": file_path}},
            return_document=True
        )
        return post_helper(updated_post)
    raise HTTPException(status_code=404, detail="Post not found")

@router.get("/users/{user_id}/posts", response_model=List[Post])
async def get_user_posts(user_id: str):
    posts = await posts_collection.find({"user_id": user_id}).to_list(1000)
    return [post_helper(post) for post in posts]