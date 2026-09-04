import os
import asyncio
from aiohttp import web
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN

# Render डिफ़ॉल्ट रूप से PORT पर्यावरण चर (Environment Variable) प्रदान करता है
PORT = int(os.environ.get("PORT", 8080))

# 1. Health Check Handler - Render इसी पर चेक करके Deployment SUCCESS करेगा
async def ping_handler(request):
    return web.Response(text="AutoFilter Bot is Active & Running!")

# 2. Pyrogram Client Init
app = Client(
    "AutoFilterBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

async def start_all():
    # सबसे पहले Web Server शुरू करो ताकि Render तुरंत "Port Detected" बोल दे
    web_app = web.Application()
    web_app.router.add_get("/", ping_handler)
    
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"--> Web Server successfully running on port {PORT}")

    # अब Telegram Bot चालू करो
    print("--> Starting Pyrogram Bot...")
    await app.start()
    print("--> Bot started successfully!")

    # बॉट को चालू रखने के लिए idle()
    await idle()
    await app.stop()

if __name__ == "__main__":
    # Async Event Loop
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_all())
    except KeyboardInterrupt:
        print("Bot Stopped.")
