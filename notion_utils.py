from notion_client import Client as NotionClient

# Notion API Credentials
NOTION_TOKEN = "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"
DATABASE_ID = "1697280d4cf580ab9857c44b7f0dd95b"

# Initialize Notion Client
notion = NotionClient(auth=NOTION_TOKEN)

# Helper Function to Fetch Data from Notion Database
def fetch_data_from_notion():
    response = notion.databases.query(database_id=DATABASE_ID)
    movies = []
    for page in response["results"]:
        title = page["properties"]["File Name"]["title"][0]["text"]["content"]
        file_size = page["properties"]["File Size"]["rich_text"][0]["text"]["content"]
        file_type = page["properties"]["File Type"]["rich_text"][0]["text"]["content"]
        file_id = page["properties"]["File ID"]["rich_text"][0]["text"]["content"]
        movies.append({"title": title, "file_size": file_size, "file_type": file_type, "file_id": file_id})
    return movies

# Helper Function to Save Data to Notion
def save_to_notion(title, file_size, file_type, file_id):
    notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "File Name": {"title": [{"text": {"content": title}}]},
            "File Size": {"rich_text": [{"text": {"content": file_size}}]},
            "File Type": {"rich_text": [{"text": {"content": file_type}}]},
            "File ID": {"rich_text": [{"text": {"content": file_id}}]},
        },
    )