import requests
import base64
from config import JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN
from requests.auth import HTTPBasicAuth

def post_comment(issue_key, text):
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}/comment"

    requests.post(
        url,
        auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN),
        json={"body": text},
        headers={"Accept": "application/json"}
    )

def get_ticket(ticket_id):
    print("JIRA_URL:", os.getenv("JIRA_URL"))
    print("JIRA_EMAIL:", os.getenv("JIRA_EMAIL"))
    print("JIRA_API_TOKEN:", os.getenv("JIRA_API_TOKEN"))
    
    url = f"{JIRA_URL}/rest/api/3/issue/{ticket_id}"

    response = requests.get(
        url,
        auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN),
        headers={"Accept": "application/json"}
    )

    data = response.json()

    attachments = data["fields"].get("attachment", [])
    
    image_base64_strings = []
    for att in attachments:
        if att["mimeType"].startswith("image/"):
            image_url = att["content"]
            image_response = requests.get(
                image_url,
                auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
            )
            
            base64_encoded_image = base64.b64encode(image_response.content).decode('utf-8')
            
            # Prepend the data URI scheme
            mime_type = att["mimeType"]
            image_base64_strings.append(f"data:{mime_type};base64,{base64_encoded_image}")


    return {
        "title": data["fields"]["summary"],
        "description": data["fields"]["description"],
        "images": image_base64_strings
    }
