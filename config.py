import os

API_ID = int(os.environ.get("API_ID", "123456"))
API_HASH = os.environ.get("API_HASH", "your_api_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")

MONGO_URI = os.environ.get("MONGO_URI", "your_mongodb_uri")
ADMINS = [int(x) for x in os.environ.get("ADMINS", "123456789").split()]

# डिफ़ॉल्ट सेटिंग्स
SHORTENER_URL = os.environ.get("SHORTENER_URL", "shortner.com")
SHORTENER_API = os.environ.get("SHORTENER_API", "your_api_key")
VERIFY_EXPIRE = int(os.environ.get("VERIFY_EXPIRE", "86400")) # 24 घंटे (सेकंड में)
