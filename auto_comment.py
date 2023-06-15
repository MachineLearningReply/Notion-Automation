import requests
from datetime import datetime

# Set up your Notion API integration token and database ID
NOTION_DATABASE_ID = "<NOTION_DATABASE_ID>"
INTEGRATION_TOKEN = "<INTEGRATION_TOKEN>"

# Set up the necessary headers for the API requests
headers = {
    "Authorization": "Bearer {INTEGRATION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# Set the desired date filter
desired_date = datetime.now().strftime("%Y-%m-%d")

# Query the Notion database and retrieve the rows
response = requests.post(
    "https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query",
    headers=headers,
)
data = response.json()
rows = data["results"]

# Iterate through each row
for row in rows:
    row_id = row["id"]

    # Get the value of the 'tags' column for each row
    tags_value = row["properties"]["project"]["select"]["name"]

    # Get the value of the 'status' column for each row
    status_value = row["properties"]["status"]["select"]["name"]

    # Get the last edited revisions for the row
    user_id = row["properties"]["Last edited by"]["people"][0]["id"]

    # Check if the conditions match
    if tags_value == "ongoing" and status_value == "incomplete":
        # Get the user details
        fetch_user_url = "https://api.notion.com/v1/users/{user_id}"
        response = requests.get(fetch_user_url, headers=headers)
        data = response.json()

        # Construct the comment message with user mention
        comment_message = "Hello @{data['name']}! This is a comment for you."

        # Create the comment on Notion
        comment_payload = {
            "parent": {"page_id": row_id},
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": "Hello "},
                },
                {
                    "type": "mention",
                    "mention": {"type": "user", "user": {"id": user_id}},
                },
                {
                    "type": "text",
                    "text": {"content": "! This is a comment for you."},
                },
            ],
        }
        response = requests.post(
            "https://api.notion.com/v1/comments", headers=headers, json=comment_payload
        )

        if response.status_code == 200:
            print("Comment created on Notion for user with ID: {user_id}")
        else:
            print("Failed to create comment on Notion for user with ID: {user_id}")
