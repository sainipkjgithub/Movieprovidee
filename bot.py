from pyrogram import Client, filters
from handlers import start, about_inline, close_inline, handle_upload
from inline_handlers import inline_query_handler  # Import inline query handler
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Bot Credentials
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize Client
app = Client("inline-file-search-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Register Handlers
app.on_message(filters.command("start"))(start)
app.on_callback_query(filters.regex("about_inline"))(about_inline)
app.on_callback_query(filters.regex("close_inline"))(close_inline)
app.on_message(filters.document | filters.video)(handle_upload)
app.on_inline_query()(inline_query_handler)  # Register inline query handler

# Run the Bot
print("Bot is running...")
app.run()