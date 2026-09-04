import aiohttp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import VERIFY_EXPIRE
from database.files_mdb import search_files
from database.users_mdb import is_user_verified, get_shortener_settings, generate_verify_token

async def get_short_link(url, api, long_url):
    api_url = f"https://{url}/api?api={api}&url={long_url}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                data = await resp.json()
                return data.get("shorturl", long_url)
    except Exception:
        return long_url

@Client.on_message(filters.text & (filters.private | filters.group) & ~filters.command(["start", "shortener", "set_shortener"]))
async def filter_handler(client, message):
    user_id = message.from_user.id
    query = message.text
    
    # 1. डेटाबेस से फाइल सर्च करें
    files = await search_files(query)
    if not files:
        return # अगर फाइल नहीं मिली तो इग्नोर करें या 'Not Found' भेजें

    st = await get_shortener_settings()
    verified = await is_user_verified(user_id, VERIFY_EXPIRE)

    # 2. अगर शॉर्टनर ON है और यूजर ने 24h Pass कम्प्लीट नहीं किया है
    if st["is_active"] and not verified:
        bot_username = (await client.get_me()).username
        token = await generate_verify_token(user_id)
        
        # वेरिफिकेशन लिंक (बॉट में रीडायरेक्ट करेगा)
        bypass_link = f"https://t.me/{bot_username}?start=verify_{token}"
        short_link = await get_short_link(st["url"], st["api"], bypass_link)
        
        btn = [[InlineKeyboardButton("🔑 Unlock All Files for 24 Hours", url=short_link)]]
        return await message.reply(
            f"🎬 **`{query}` फ़ाइल मिल गई है!**\n\n"
            f"⚠️ लेकिन आपका **24 घंटे का एक्सेस Pass** खत्म हो चुका है।\n"
            f"नीचे दिए गए लिंक से वेरिफिकेशन पूरा करें, उसके बाद आप पूरे 24 घंटे तक कोई भी फ़ाइल अनलिमिटेड प्राप्त कर सकते हैं:",
            reply_markup=InlineKeyboardMarkup(btn)
        )

    # 3. अगर 24h Pass एक्टिव है या Shortener OFF है -> सीधी फ़ाइलों के बटन दिखाएं
    buttons = []
    for file in files:
        file_name = file['file_name']
        file_id = file['file_id']
        buttons.append([InlineKeyboardButton(f"🎬 {file_name}", callback_data=f"file_{file_id}")])

    await message.reply(f"🔎 **`{query}` के नतीजे:**", reply_markup=InlineKeyboardMarkup(buttons))

# बटन पर क्लिक करने पर डायरेक्ट फ़ाइल भेजना
@Client.on_callback_query(filters.regex(r"^file_"))
async def send_file_cb(client, query):
    file_id = query.data.split("_")[1]
    await query.answer("फ़ाइल भेजी जा रही है...")
    await client.send_cached_media(
        chat_id=query.from_user.id,
        file_id=file_id
    )
    
