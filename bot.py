from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from script1 import CALLBACK123, home_keyboard, ReplyMarkup123, startmsg, wrongbutton
from ReplyMarckep import download_any_video,available_boards,help_keyboard
import requests
import time
from flask import Flask

from handlers import start, about_inline, close_inline, handle_upload
from inline_handlers import inline_query_handler  # Import inline query handler
from dotenv import load_dotenv
import os
import threading

# बॉट के लिए API क्रेडेंशियल्स
API_ID2 = 24673538
API_HASH2 = "555639745e6ceee1ae3797866136998f"
BOT_TOKEN2 = "7868467316:AAFa2MOEJDtqHDRFR7feb8z2fWZizQU5B1U"
user_status = {}
user_histories = {}
# Pyrogram बॉट क्लाइंट सेटअप
app2 = Client(
    "my_bot",
    api_id=API_ID2,
    api_hash=API_HASH2,
    bot_token=BOT_TOKEN2
)


#####
###
###
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
    return "Movie Bot And All in one Bot is running."

# Initialize Pyrogram Client
app = Client("inline-file-search-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Register Handlers
app.on_message(filters.command("start"))(start)
app.on_callback_query(filters.regex("about_inline"))(about_inline)
app.on_callback_query(filters.regex("close_inline"))(close_inline)
app.on_message(filters.document | filters.video)(handle_upload)
app.on_inline_query()(inline_query_handler)  # Register inline query handler

# Function to run Flask app

# Running Flask and Pyrogram bot concurrently using threads
######
#####
####
         
@app2.on_message(filters.command("start"))
def start(client, message):
    # इनलाइन कीबोर्ड बटन बनाएं
    message.reply_text(
        startmsg,
        reply_markup=home_keyboard
    )
    
@app2.on_message(filters.command("help"))
def start(client, message):
    # इनलाइन कीबोर्ड बटन बनाएं
    message.reply_text(
        startmsg,
        reply_markup=help_keyboard
    )
@app2.on_callback_query()
def callback_query(client, query: CallbackQuery):
    user_id = query.from_user.id  # Get user ID
    user_name = query.from_user.first_name  # Extract user name
    if query.data == "chat_with_assistant":
        user_status[user_id] = "chatting_with_ai"  # Save user status
        query.message.edit_text("Ok Now You are talking to our Ai Assistent...")
        time.sleep(5)
        query.message.delete()
        a=query.message.reply_text(f"Hello {user_name}, How can I assist you today..?")
        time.sleep(5)
        a.message.delete()
    elif query.data == "download_any_video":
      query.message.edit_text("This Features Is Comming Soon.", reply_markup=download_any_video)
    elif query.data == "board_results":
      query.message.edit_text("Please Select Your Board :", reply_markup=available_boards)
    elif query.data in CALLBACK123:
      if query.data in ReplyMarkup123:
        query.message.edit_text(CALLBACK123[query.data], reply_markup=ReplyMarkup123[query.data])
      else:
        query.message.edit_text(CALLBACK123[query.data])
    else:
        query.message.edit_text("No Data Found For Your Clicked Button. Please Contact to Admin to Support",reply_markup=wrongbutton)
@app2.on_message(
    filters.text &  # सिर्फ टेक्स्ट मैसेज
    ~filters.me &   # बॉट के अपने मैसेज को इग्नोर करे
    ~filters.group & # ग्रुप चैट्स को इग्नोर करे
    ~filters.command("start")  # ✅ सभी कमांड्स ("/something") को इग्नोर करे
)
def process_text_messages(client: Client, message: Message):
    user_id = message.from_user.id
    user_msg = message.text
    user_name = message.from_user.first_name
    if user_status.get(user_id) == "chatting_with_ai":
      answer = sendAi_message(user_id,user_name, user_msg)
      message.reply_text(answer)
    else:
        message.reply_text("⚠️ Please Select a Valid Option.")

def sendAi_message(user_id,user_name, user_msg):
    url = "https://text.pollinations.ai/openai"
    headers = {"Content-Type": "application/json"}

    # अगर यूज़र पहली बार मैसेज भेज रहा है, तो उसकी हिस्ट्री इनिशियलाइज़ करें
    if user_id not in user_histories:
        user_histories[user_id] = []

    # नया मैसेज JSON फ़ॉर्मेट में हिस्ट्री में जोड़ें
    user_histories[user_id].append({
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": user_msg
            }
        ]
    })

    # API को भेजने के लिए JSON payload तैयार करें
    payload = {
        "model": "gpt-4",
        "system": f"""
You are Akshay Sharma, the Owner of SingodiyaTech.

SingodiyaTech was founded and developed by Mr. Singodiya and specializes in cutting-edge automation and scalable tech solutions.

You are an expert in Pyrogram and Google Apps Script, developing high-performance Telegram bots and Google Sheets API integrations.

Your work focuses on large-scale automation, seamless user interaction, and performance optimization.

You have expertise in PHP UI development, specifically improving result display systems.

Additionally, you are building a high-performance video streaming platform capable of handling 100M+ users with zero lag.


User Details:

Name: {user_name}

Telegram ID: {user_id}


Your mission is to develop scalable, efficient, and intelligent automation solutions, ensuring seamless integration and user satisfaction.


        """,
        "messages": user_histories[user_id]  # यूज़र की पूरी हिस्ट्री भेजें
    }

    # API कॉल करें
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        assistant_msg = result.get("choices", [{}])[0].get("message", {}).get("content", "")

        # असिस्टेंट का जवाब भी सही फ़ॉर्मेट में स्टोर करें
        user_histories[user_id].append({
            "role": "assistant",
            "content": assistant_msg
        })

        return assistant_msg
    else:
        return f"Error: {response.status_code}, {response.text}"
        
        
def run_flask():
    flask_app.run(host="0.0.0.0", port=5000)

# Function to run Pyrogram bot
def run_bot():
    print("Bot is running...")
    app.run()
def run_bot2():
    print("Bot is running...")
    app2.run()
    
if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    bot1_thread = threading.Thread(target=run_bot, daemon=True)
    bot2_thread = threading.Thread(target=run_bot2, daemon=True)

    flask_thread.start()
    bot1_thread.start()
    bot2_thread.start()

    bot1_thread.join()
    bot2_thread.join()
