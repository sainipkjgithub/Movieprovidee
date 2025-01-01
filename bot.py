from pyrogram import Client, filters
from flask import Flask
from handlers import start, about_inline, close_inline, handle_upload
from inline_handlers import inline_query_handler  # Import inline query handler
from dotenv import load_dotenv
import os
import threading

# Load environment variables
load_dotenv()

# Bot Credentials
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize Flask app
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Flask app is running."

# Initialize Pyrogram Client
app = Client("inline-file-search-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Register Handlers
app.on_message(filters.command("start"))(start)
app.on_callback_query(filters.regex("about_inline"))(about_inline)
app.on_callback_query(filters.regex("close_inline"))(close_inline)
app.on_message(filters.document | filters.video)(handle_upload)
app.on_inline_query()(inline_query_handler)  # Register inline query handler

# Function to run Flask app
def run_flask():
    flask_app.run(host="0.0.0.0", port=5000)

# Function to run Pyrogram bot
def run_bot():
    print("Bot is running...")
    app.run()

# Running Flask and Pyrogram bot concurrently using threads
if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    run_bot()  # This will run the bot after Flask starts
