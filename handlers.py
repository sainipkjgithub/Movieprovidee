from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultCachedDocument, InlineQueryResultArticle, InputTextMessageContent
from notion_utils import fetch_data_from_notion, save_to_notion



# Admin and Channel Information
ADMIN_IDS = [5943119285, 6150091802,7222712791]
CHANNEL_ID = -1002469822258

#@app.on_message(filters.command("start"))
async def start(client, message):
    user_name = message.from_user.first_name
    user_contact_link = f"tg://user?id={message.from_user.id}"
    owner_contact_link = "http://t.me/mr_singodiyabot"
    if message.from_user.id in ADMIN_IDS:
        await message.reply_text(
            "Hello My God! How are you? Let's upload a movie or video.",reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔍 Search Movies", switch_inline_query_current_chat=""
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "➕𝐀𝐃𝐃 𝐌𝐄 𝐓𝐎 𝐘𝐎𝐔𝐑 𝐆𝐑𝐎𝐔𝐏➕", url="https://t.me/AllMy_MoviesBot?startgroup=true"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "ℹ️𝐀𝐁𝐎𝐔𝐓", callback_data="about_inline"
                    ),
                      InlineKeyboardButton(
                        "𝐔𝐏𝐃𝐀𝐓𝐄𝐒 🔔", url="https://t.me/aibots72"
                    ),

                ]
            ]
        ),
        )
    else:
        

        await message.reply_text(
            f"""
Hello [{user_name}]({user_contact_link})! Welcome to 𝗠𝗢𝗩𝗜𝗘 𝗣𝗥𝗢𝗩𝗜𝗗𝗘𝗥 𝗕𝗢𝗧.

☟︎**☟︎Are you searching for a movie.☟︎**☟︎

➪CLICK On  **🔍 Search Movies** to search your movie.

[𝑱𝑶𝑰𝑵 𝑼𝑷𝑫𝑨𝑻𝑬𝑺 𝑪𝑯𝑨𝑵𝑵𝑬𝑳 𝑻𝑶 𝑮𝑬𝑻 𝑴𝑶𝑹𝑬 𝑷𝑶𝑾𝑬𝑹𝑭𝑼𝑳𝑳 𝑨𝑵𝑫 𝑼𝑺𝑬𝑭𝑼𝑳𝑳 𝑩𝑶𝑻𝑺](https://t.me/aibots72).
            """,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔍 Search Movies", switch_inline_query_current_chat=""
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "➕𝐀𝐃𝐃 𝐌𝐄 𝐓𝐎 𝐘𝐎𝐔𝐑 𝐆𝐑𝐎𝐔𝐏➕", url="https://t.me/AllMy_MoviesBot?startgroup=true"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "ℹ️𝐀𝐁𝐎𝐔𝐓", callback_data="about_inline"
                    ),
                      InlineKeyboardButton(
                        "𝐔𝐏𝐃𝐀𝐓𝐄𝐒 🔔", url="https://t.me/aibots72"
                    ),

                ]
            ]
        ),
            
        )

# Callback Query Handler for About Inline
#@app.on_callback_query(filters.regex("about_inline"))
async def about_inline(client, callback_query):
    await callback_query.message.edit_text(
        """ **Hello I am a Movie Provider Bot.** 

▪**I can provide any movie▪**

**✧How To use Me✧**
➤ Just /start the bot.
➤Click on **🔍 Search Movie**.
➤Search your Movie by fill the Movie Name. 


▸If you Didn't Find Your Movie. Please Contact to the Admin ◂

○ **Owner**: **[✪Mr. Singodiya✪](http://t.me/mr_singodiyabot)**
○ **Channel**: [AI Bots](https://t.me/aibots72)
○ **Support Group**: [AI Bot Support](https://t.me/aibotes)
        """,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔒 Close", callback_data="close_inline")]]
        ),
        disable_web_page_preview=True,
    )

# Callback Query Handler for Close Inline
#@app.on_callback_query(filters.regex("close_inline"))
async def close_inline(client, callback_query):
    user_name = callback_query.from_user.first_name
  
    user_contact_link = f"tg://user?id={callback_query.from_user.id}"
    owner_contact_link = "http://t.me/mr_singodiyabot"
    await callback_query.message.edit_text(
        f"""
Hello [{user_name}]({user_contact_link})! Welcome to 𝗠𝗢𝗩𝗜𝗘 𝗣𝗥𝗢𝗩𝗜𝗗𝗘𝗥 𝗕𝗢𝗧.

☟︎**☟︎Are you searching for a movie.☟︎**☟︎

➪CLICK On  **🔍 Search Movies** to search your movie.

[𝑱𝑶𝑰𝑵 𝑼𝑷𝑫𝑨𝑻𝑬𝑺 𝑪𝑯𝑨𝑵𝑵𝑬𝑳 𝑻𝑶 𝑮𝑬𝑻 𝑴𝑶𝑹𝑬 𝑷𝑶𝑾𝑬𝑹𝑭𝑼𝑳𝑳 𝑨𝑵𝑫 𝑼𝑺𝑬𝑭𝑼𝑳𝑳 𝑩𝑶𝑻𝑺](https://t.me/aibots72).
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔍 Search Movies", switch_inline_query_current_chat=""
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "➕𝐀𝐃𝐃 𝐌𝐄 𝐓𝐎 𝐘𝐎𝐔𝐄 𝐆𝐑𝐎𝐔𝐏➕", url="https://t.me/AllMy_MoviesBot?startgroup=true"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "✔︎ 𝐀𝐁𝐎𝐔𝐓", callback_data="about_inline"
                    ),
                      InlineKeyboardButton(
                        "𝐔𝐏𝐃𝐀𝐓𝐄𝐒🔔", url="https://t.me/aibots72"
                    ),

                ]
            ]
        ),
    )

# Handle File Upload
#@app.on_message(filters.document | filters.video)
async def handle_upload(client, message):
    # Check if the user is an admin
    if message.from_user.id not in ADMIN_IDS:
        await message.reply_text("😎😊Enjoy Your Movie 🎥 If you want to add aur request for a movie please contact to admin @mr_singodiyabot")
        return

    # Process file upload (only for admins)
    if message.video:
        file_type = "Video"
        file_name = message.video.file_name
        file_size = f"{message.video.file_size / 1024 / 1024:.2f} MB"
        file_id = message.video.file_id
    elif message.document:
        file_type = "Document"
        file_name = message.document.file_name
        file_size = f"{message.document.file_size / 1024 / 1024:.2f} MB"
        file_id = message.document.file_id
    else:
        return

    # Save to Notion directly
    save_to_notion(file_name, file_size, file_type, file_id)

    # Send to Channel
    if file_type == "Document":
        await client.send_document(
            CHANNEL_ID,
            document=file_id,
            caption=f"**Title:** {file_name}\n**Size:** {file_size}\n**Type:** {file_type}",
        )
    elif file_type == "Video":
        await client.send_video(
            CHANNEL_ID,
            video=file_id,
            caption=f"**Title:** {file_name}\n**Size:** {file_size}\n**Type:** {file_type}",
        )

    # Success Message
    await message.reply_text("✅ **Uploaded Successfully**")
