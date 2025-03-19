from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, ReplyKeyboardRemove
from script1 import CALLBACK123, home_keyboard, ReplyMarkup123, startmsg, wrongbutton
from ReplyMarckep import download_any_video,available_boards,help_keyboard, chat_with_assistant, cancel12
import requests
import time
from flask import Flask
from dotenv import load_dotenv
import os
import threading

load_dotenv()

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "All in one Bot is running."

# बॉट के लिए API क्रेडेंशियल्स
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
user_status = {}
user_histories = {}
user_board_details = {}
wb_id_dict = {
    "rbse_10": 88,
    "rbse_12": 89,
    "up_10": 99,
    "up_12": 100
}
# Pyrogram बॉट क्लाइंट सेटअप
app = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

         
@app.on_message(filters.command("start"))
def start(client, message):
    # इनलाइन कीबोर्ड बटन बना
    user_id = message.from_user.id
    if user_status.get(user_id) == "chatting_with_ai":
      message.reply_text("⚠️Please Cancel this chat first!",reply_markup=cancel12)
    if user_status.get(user_id) == "enter_roll_number":
       if user_id in user_board_details:
         board = user_board_details[user_id]["board"]
         class_name = user_board_details[user_id]["class"]
         result_link = f"https://results.example.com/{board}/{class_name}"
         message.reply_text(f"Check your result here: {result_link}")
    else:
      message.reply_text(
        startmsg,
        reply_markup=home_keyboard
    )
    
@app.on_message(filters.command("help"))
def helpcommand(client, message):
    # इनलाइन कीबोर्ड बटन बनाएं
    message.reply_text(
        startmsg,
        reply_markup=help_keyboard
    )
@app.on_callback_query()
def callback_query(client, query: CallbackQuery):
    user_id = query.from_user.id  # Get user ID
    user_name = query.from_user.first_name  # Extract user name
    if query.data == "chat_with_assistant":
        query.message.edit_text("Ok Now You are talking to our Ai Assistent...")
        time.sleep(2)
        query.message.delete()
        a=query.message.reply_text(f"Hello {user_name}, How can I assist you today..?",reply_markup=chat_with_assistant)
        user_status[user_id] = "chatting_with_ai"  # Save user status
        #a.delete()
    elif query.data == "download_any_video":
      query.message.edit_text("This Features Is Comming Soon.", reply_markup=download_any_video)
    elif query.data.startswith("board_result_") and query.data.endswith(("_10", "_12")):
        parts = query.data.split("_")
        board_name = parts[2]  # Extract board name
        class_name = parts[3]  # Extract class (10 or 12)
    
        user_board_details[user_id] = {"board": board_name, "class": class_name}  # Save user board details
        user_status[user_id] = "enter_roll_number"  # Save user status
    
        query.message.edit_text(f"Board: {board_name.upper()}\nClass: {class_name}. Please Enter Your Roll Number...")
    elif query.data.startswith("board_result_"):
        board_name = query.data.split("_")[-1]  # Extract board name
        buttons = [
        [InlineKeyboardButton("Class 10", callback_data=f"board_result_{board_name}_10")],
        [InlineKeyboardButton("Class 12", callback_data=f"board_result_{board_name}_12")]
        ]
        query.message.edit_text("Select your class:", reply_markup=InlineKeyboardMarkup(buttons))
####CANCEL MSG HANDEL###    
    elif query.data == "cancel":
      user_id = query.from_user.id
      user_name = query.from_user.first_name
      if user_status.get(user_id) == "chatting_with_ai":
        del user_status[user_id]
        msg12 = query.message.reply_text("Session Canceled!", reply_markup=ReplyKeyboardRemove())
        time.sleep(0.7)
        msg12.delete()
        query.message.reply_text(startmsg,reply_markup=home_keyboard)
        query.message.delete()
      elif user_status.get(user_id) == "enter_roll_number":
        del user_status[user_id]
      elif user_status.get(user_id) == "download_any_video":
        del user_status[user_id]
      else:
          query.message.reply_text("⚠️ Nothing to CANCLE. ")
        
    elif query.data in CALLBACK123:
      if query.data in ReplyMarkup123:
        query.message.edit_text(CALLBACK123[query.data], reply_markup=ReplyMarkup123[query.data])
      else:
        query.message.edit_text(CALLBACK123[query.data])
    else:
        query.message.edit_text("No Data Found For Your Clicked Button. Please Contact to Admin to Support",reply_markup=wrongbutton)
@app.on_message(
    filters.text &  # सिर्फ टेक्स्ट मैसेज
    ~filters.me &   # बॉट के अपने मैसेज को इग्नोर करे
    ~filters.group & # ग्रुप चैट्स को इग्नोर करे
    ~filters.command("start") &  # ✅ सभी कमांड्स ("/something") को इग्नोर करे
    ~filters.regex(r"^🚫CANCEL$")
)
def process_text_messages(client: Client, message: Message):
    user_id = message.from_user.id
    user_msg = message.text
    user_name = message.from_user.first_name
    if user_status.get(user_id) == "chatting_with_ai":
      answer = sendAi_message(user_id,user_name, user_msg)
      message.reply_text(answer)
    # WB ID Dictionary for different boards and classes

    elif user_status.get(user_id) == "enter_roll_number":
        if user_id in user_board_details:
            board = user_board_details[user_id]["board"]
            class_name = user_board_details[user_id]["class"]
            roll_no = user_msg.strip()  # Get user input roll number
        
        # Validate roll number (should be 7 digits and numeric)
            if roll_no.isdigit() and len(roll_no) == 7:
                key = f"{board}_{class_name}"  # Generate key for wb_id
                wb_id = wb_id_dict.get(key, 88)  # Default to 88 if not found

                # Generate result document URL
                
                result_link = f"https://sainipankaj12.serv00.net/Result/boardresult.php?tag=raj_10_result&roll_no={roll_no}&year=2024&wb_id={wb_id}&source=3&download"
                
                a=message.reply_text(f"Please Wait...  {result_link}")
                # Send document to user
                result_link_view = result_link.replace("download", "see")
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
                data ={
                   "chat_id": user_id,
                    "caption": "Here is your result document.",
                    "document": result_link,
                    "reply_markup": '{"inline_keyboard": [[{"text": "View Online", "web_app": {"url": "' + result_link_view + '"}}]]}'
                       }
                

                requests.post(url, data=data)
                a.delete()
            else:
                message.reply_text("Invalid roll number! Please enter a 7-digit numeric roll number.")
        else:
           message.reply_text("Please select your board and class first.")
    else:
        message.reply_text("⚠️ Please Select a Valid Option.")
@app.on_message(
    filters.text &  
    ~filters.me &   
    ~filters.group &  
    ~filters.command("start") &  
    filters.regex(r"^🚫CANCEL$")  
)
def canclemsg(client: Client, message: Message):
    user_id = message.from_user.id
    user_msg = message.text
    user_name = message.from_user.first_name
    if user_status.get(user_id) == "chatting_with_ai":
      del user_status[user_id]
      msg12 = message.reply_text("Session Canceled!", reply_markup=ReplyKeyboardRemove())
      time.sleep(0.7)
      msg12.delete()
      message.reply_text(
        startmsg,
        reply_markup=home_keyboard
    )
      
    elif user_status.get(user_id) == "enter_roll_number":
      del user_status[user_id]
    elif user_status.get(user_id) == "download_any_video":
      del user_status[user_id]
    else:
        message.reply_text("⚠️ Nothing to CANCLE. ")
        
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
    flask_app.run(host="0.0.0.0", port=8000)

# Function to run Pyrogram bot
def run_bot():
    print("Bot is running...")
    app.run()

# Running Flask and Pyrogram bot concurrently using threads
if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    run_bot()  # This will run the bot after Flask starts
