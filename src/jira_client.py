import requests
import base64
from src.config import JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN
from requests.auth import HTTPBasicAuth

def upload_attachment(issue_key, file_path):
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}/attachments"

    with open(file_path, "rb") as f:
        response = requests.post(
            url,
            auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN),
            files={"file": (file_path, f, "text/markdown")},
            headers={
                "X-Atlassian-Token": "no-check"
            }
        )

    response.raise_for_status()

def get_ticket(ticket_id):
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
