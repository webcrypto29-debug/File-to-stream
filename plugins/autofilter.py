import aiohttp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import VERIFY_EXPIRE
from database.users import is_user_verified, get_shortener_settings

async def get_short_link(url, api, long_url):
    api_url = f"https://{url}/api?api={api}&url={long_url}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as resp:
            data = await resp.json()
            return data.get("shorturl", long_url)

@Client.on_message(filters.text & filters.private & ~filters.command(["start", "shortener", "set_shortener"]))
async def filter_handler(client, message):
    user_id = message.from_user.id
    st = await get_shortener_settings()
    
    # चेक करें कि क्या शॉटनर ऑन है और यूजर का 24-घंटे का टाइमर पूरा हो चुका है
    if st["is_active"]:
        verified = await is_user_verified(user_id, VERIFY_EXPIRE)
        if not verified:
            bot_username = (await client.get_me()).username
            bypass_link = f"https://t.me/{bot_username}?start=verify_{user_id}"
            short_link = await get_short_link(st["url"], st["api"], bypass_link)
            
            btn = [[InlineKeyboardButton("🔑 Complete 24h Token Verification", url=short_link)]]
            return await message.reply(
                "⚠️ **आपकी 24 घंटे की वेरिफिकेशन खत्म हो चुकी है।**\nनिचे दिए गए लिंक से सत्यापन करें, फिर फाइल डाउनलोड करें:",
                reply_markup=InlineKeyboardMarkup(btn)
            )

    # अगर वेरिफिकेशन चालू है या शॉटनर बंद है तो फाइल दें
    await message.reply(f"🔎 Results for: `{message.text}`\n(यहाँ फ़ाइल या सर्च रिज़ल्ट इनलाइन बटन में भेजें)")
  
