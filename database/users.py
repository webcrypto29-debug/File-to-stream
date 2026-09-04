import motor.motor_asyncio
import time
from config import MONGO_URI, SHORTENER_URL, SHORTENER_API

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client["AutofilterBot"]
users = db["users"]
settings = db["settings"]

# यूजर का 24-घंटे का टाइमर अपडेट करना
async def update_verify_time(user_id):
    await users.update_one(
        {"_id": user_id},
        {"$set": {"last_verified": time.time()}},
        upsert=True
    )

# चेक करना कि क्या यूजर का 24 घंटा बीत गया है
async def is_user_verified(user_id, expire_time):
    user = await users.find_one({"_id": user_id})
    if not user or "last_verified" not in user:
        return False
    return (time.time() - user["last_verified"]) < expire_time

# शॉटनर कॉन्फिगरेशन मैनेज करना
async def get_shortener_settings():
    st = await settings.find_one({"_id": "shortener_config"})
    if not st:
        return {"is_active": True, "url": SHORTENER_URL, "api": SHORTENER_API}
    return st

async def update_shortener_settings(is_active=None, url=None, api=None):
    current = await get_shortener_settings()
    new_data = {
        "is_active": is_active if is_active is not None else current["is_active"],
        "url": url if url is not None else current["url"],
        "api": api if api is not None else current["api"],
    }
    await settings.update_one({"_id": "shortener_config"}, {"$set": new_data}, upsert=True)
  
