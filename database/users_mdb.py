import motor.motor_asyncio
import time
import uuid
from config import MONGO_URI, SHORTENER_URL, SHORTENER_API

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client["AutoFilterBot"]
users_col = db["users"]
settings_col = db["settings"]
tokens_col = db["tokens"]

# 1. 24 घंटे का स्टेटस चेक
async def is_user_verified(user_id, expire_seconds=86400):
    user = await users_col.find_one({"_id": user_id})
    if not user or "last_verified" not in user:
        return False
    return (time.time() - user["last_verified"]) < expire_seconds

# 2. वेरिफिकेशन कम्पलीट होने पर टाइम सेव करना
async def update_verify_time(user_id):
    await users_col.update_one(
        {"_id": user_id},
        {"$set": {"last_verified": time.time()}},
        upsert=True
    )

# 3. शार्टनर टोकन जनरेट करना (ताकि कोई फेक तरीके से bypass ना कर सके)
async def generate_verify_token(user_id):
    token = str(uuid.uuid4())[:8]
    await tokens_col.update_one(
        {"_id": user_id},
        {"$set": {"token": token, "created_at": time.time()}},
        upsert=True
    )
    return token

async def verify_token(user_id, token):
    doc = await tokens_col.find_one({"_id": user_id})
    if doc and doc.get("token") == token:
        await update_verify_time(user_id)
        await tokens_col.delete_one({"_id": user_id})
        return True
    return False

# 4. ऑन/ऑफ़ और शॉर्टनर सेटिंग्स
async def get_shortener_settings():
    st = await settings_col.find_one({"_id": "shortener_config"})
    if not st:
        return {"is_active": True, "url": SHORTENER_URL, "api": SHORTENER_API}
    return st
    
