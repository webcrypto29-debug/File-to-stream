from pyrogram import Client, filters
from database.users_mdb import verify_token

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    text = message.text
    
    # अगर यूजर शॉर्टनर का टास्क पूरा करके आया है
    if len(text.split()) > 1:
        param = text.split()[1]
        if param.startswith("verify_"):
            token = param.split("verify_")[1]
            user_id = message.from_user.id
            
            # टोकन वैलिडेट करें
            res = await verify_token(user_id, token)
            if res:
                return await message.reply(
                    "🎉 **बधाई हो! 24 घंटे का Pass अनलॉक हो गया है!**\n\n"
                    "अब आप अगले 24 घंटे तक कोई भी मूवी या फ़ाइल सर्च करके बिना किसी लिंक/विज्ञापन के सीधे डाउनलोड कर सकते हैं।"
                )
            else:
                return await message.reply("❌ **अमान्य या एक्सपायर टोकन!** कृपया दोबारा सर्च करके लिंक जनरेट करें।")

    await message.reply("नमस्ते! मूवी या फ़ाइल का नाम लिखकर भेजें।")
    
