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

# 2. वेरिफिकेशन टाइम अपडेट करना
async def update_verify_time(user_id):
    await users_col.update_one(
        {"_id": user_id},
        {"$set": {"last_verified": time.time()}},
        upsert=True
    )

# 3. शॉर्टनर टोकन मैनेज करना
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

# 4. शॉर्टनर सेटिंग्स (गेट और अपडेट)
async def get_shortener_settings():
    st = await settings_col.find_one({"_id": "shortener_config"})
    if not st:
        return {"is_active": True, "url": SHORTENER_URL, "api": SHORTENER_API}
    return st

# यह फ़ंक्शन मिसिंग था, इसे यहाँ जोड़ दिया गया है:
async def update_shortener_settings(is_active=None, url=None, api=None):
    current = await get_shortener_settings()
    new_data = {
        "is_active": is_active if is_active is not None else current["is_active"],
        "url": url if url is not None else current["url"],
        "api": api if api is not None else current["api"],
    }
    await settings_col.update_one({"_id": "shortener_config"}, {"$set": new_data}, upsert=True)
    
