
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMINS
from database.users import get_shortener_settings, update_shortener_settings

@Client.on_message(filters.command("shortener") & filters.user(ADMINS))
async def shortener_panel(client, message):
    st = await get_shortener_settings()
    status_str = "🟢 ON" if st["is_active"] else "🔴 OFF"
    text = f"**Shortener Settings Panel**\n\n**Status:** {status_str}\n**URL:** `{st['url']}`\n**API:** `{st['api']}`"
    
    btn = [
        [InlineKeyboardButton("Toggle ON/OFF", callback_data="toggle_shortener")],
        [InlineKeyboardButton("Close", callback_data="close_panel")]
    ]
    await message.reply(text, reply_markup=InlineKeyboardMarkup(btn))

@Client.on_callback_query(filters.regex("toggle_shortener") & filters.user(ADMINS))
async def toggle_cb(client, query):
    st = await get_shortener_settings()
    new_status = not st["is_active"]
    await update_shortener_settings(is_active=new_status)
    await query.answer(f"Shortener turned {'ON' if new_status else 'OFF'}")
    await shortener_panel(client, query.message)

@Client.on_message(filters.command("set_shortener") & filters.user(ADMINS))
async def set_shortener_cmd(client, message):
    try:
        _, url, api = message.text.split(" ", 2)
        await update_shortener_settings(url=url, api=api)
        await message.reply(f"Shortener updated to:\n**URL:** `{url}`\n**API:** `{api}`")
    except ValueError:
        await message.reply("Format: `/set_shortener siteurl.com apikey`")
