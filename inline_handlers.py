import time
from pyrogram.types import InlineQueryResultCachedDocument, InlineQueryResultArticle, InputTextMessageContent
from notion_utils import fetch_data_from_notion
# Cache initialization
cache_data = {
    "data": None,
    "timestamp": 0
}
async def inline_query_handler(client, query):
    global cache_data

    # Check if the cache is valid (within 1 minute)
    current_time = time.time()
    if cache_data["data"] and (current_time - cache_data["timestamp"] < 60):
        # Use cached data if it's within the 1 minute time window
        movies = cache_data["data"]
    else:
        # Fetch new data from Notion
        movies = fetch_data_from_notion()
        cache_data["data"] = movies
        cache_data["timestamp"] = current_time

    results = []
    query_text = query.query.lower().strip()

    # Exact matches
    exact_matches = [
        movie for movie in movies if query_text in movie["title"].lower()
    ]

    # Sort exact matches based on position of query text in title
    exact_matches.sort(key=lambda x: x["title"].lower().index(query_text))

    # Add total results count as an InlineQueryResultArticle
    total_results_text = f"📁 Results - {len(exact_matches)}"
    results.append(
        InlineQueryResultArticle(
            title=total_results_text,
            input_message_content=InputTextMessageContent(total_results_text),
        )
    )

    # Add matched results to the Inline Query
    for movie in exact_matches:
        results.append(
            InlineQueryResultCachedDocument(
                title=movie["title"],
                document_file_id=movie["file_id"],
                description=f"Size: {movie['file_size']}\nType: {movie['file_type']}",
                caption=f"**𝐓𝐈𝐓𝐋𝐄:** {movie['title']}\n**𝐒𝐈𝐙𝐄:** {movie['file_size']}\n**𝐔𝐏𝐋𝐎𝐃𝐄𝐃 𝐁𝐘:** 𝙈𝙍. 𝙎𝙄𝙉𝙂𝙊𝘿𝙄𝙔𝘼",
            )
        )

    # Answer the Inline Query
    await query.answer(results=results[:50], cache_time=0, is_personal=True)
