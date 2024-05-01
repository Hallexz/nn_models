from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["social_media_db"]
posts_collection = db["posts"]
users_collection = db["users"]