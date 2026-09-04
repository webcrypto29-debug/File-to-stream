import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import DB_CHANNEL
from database.files_mdb import save_file, get_search_results

# 1. चैनल से ऑटो-इंडेक्सिंग (वीडियो, डॉक्यूमेंट, ऑडियो)
@Client.on_message(filters.chat(DB_CHANNEL) & (filters.document | filters.video | filters.audio))
async def auto_index_media(client, message):
    media = message.document or message.video or message.audio
    if media:
        file_id = media.file_id
        file_name = media.file_name or message.caption or "Unknown_File"
        file_size = media.file_size
        
        # डेटाबेस में सेव करना
        await save_file(file_id, file_name, file_size)
        print(f"[INDEX SUCCESS] Saved file: {file_name}")

# 2. ग्रुप और प्राइवेट चैट में ऑटो-फिल्टर (सर्च)
@Client.on_message(filters.text & ~filters.command)
async def auto_filter_search(client, message):
    query = message.text.strip()
    
    # 2 अक्षर से छोटे टेक्स्ट पर सर्च न करें
    if len(query) < 2:
        return

    files = await get_search_results(query)
    
    if not files:
        return

    # सर्च रिज़ल्ट के इनलाइन बटन्स बनाना
    buttons = []
    for file in files[:10]: # टॉप 10 रिज़ल्ट
        btn_text = f"📁 {file['file_name']} [{round(file['file_size']/(1024*1024), 1)} MB]"
        # फाइल ID या वेरिफिकेशन लिंक बटन में पास करें
        buttons.append([InlineKeyboardButton(text=btn_text, callback_data=f"file_{file['_id']}")])

    await message.reply_text(
        text=f"🔍 **Search Results for:** `{query}`",
        reply_markup=InlineKeyboardMarkup(buttons)
                        )
    
