
from pyrogram import Client, filters
from database.users import update_verify_time

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    if len(message.command) > 1 and message.command[1].startswith("verify_"):
        user_id = message.from_user.id
        await update_verify_time(user_id)
        return await message.reply("✅ **24 घंटे के लिए वेरिफिकेशन सफल हुआ!** अब आप कोई भी फाइल डाउनलोड कर सकते हैं।")
        
    await message.reply("नमस्ते! मूवी या फ़ाइल का नाम लिखकर भेजें।")
  
