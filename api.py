from fastapi import FastAPI, Request
from jira_client import get_ticket, post_comment

app = FastAPI()

@app.post("/jira-webhook")
async def jira_webhook(req: Request):
    data = await req.json()

    comment = data["comment"]["body"]
    issue_key = data["issue"]["key"]

    if "/testcases" in comment:
        result = get_ticket(issue_key)

        post_comment(issue_key, result)

    return {"status": "ok"}