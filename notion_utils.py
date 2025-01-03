import requests

# Web App URL (Replace with your deployed Web App URL)
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxlRtbIY1xe8GaxjiikIqOG1V5uH5K7JkErF4WJKGbuOCCBNjLVAh60KLyduKAhtM1bjg/exec?action=fetch"

# Helper Function to Fetch Data from Google Sheets
def fetch_data_from_notion():
    # Sending a GET request to fetch data
    params = {"action": "fetch"}
    response = requests.get(WEB_APP_URL, params=params)
    
    # If response is successful, parse JSON data
    if response.status_code == 200:
        data = response.json()
        movies = []
        for movie in data:
            movies.append({
                "title": movie["title"],
                "file_size": movie["file_size"],
                "file_type": movie["file_type"],
                "file_id": movie["file_id"]
            })
        return movies
    else:
        raise Exception(f"Failed to fetch data: {response.text}")

# Helper Function to Save Data to Google Sheets
def save_to_notion(title, file_size, file_type, file_id):
    # Sending a POST request to save data
    payload = {
        "action": "save",
        "title": title,
        "file_size": file_size,
        "file_type": file_type,
        "file_id": file_id,
    }
    response = requests.post(WEB_APP_URL, json=payload)
    
    # If response is successful, return success message
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to save data: {response.text}")

# Example Usage
