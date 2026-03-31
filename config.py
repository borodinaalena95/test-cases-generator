import os
from dotenv import load_dotenv

if not os.getenv('RAILWAY_ENVIRONMENT_ID'):
    load_dotenv()
    print("using load dotenv")

print("hello" + os.getenv('RAILWAY_ENVIRONMENT_ID'))

print("JIRA_URL:", os.getenv("JIRA_URL"))
print("JIRA_EMAIL:", os.getenv("JIRA_EMAIL"))
print("JIRA_API_TOKEN:", os.getenv("JIRA_API_TOKEN"))

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
