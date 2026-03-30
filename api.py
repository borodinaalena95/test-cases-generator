from fastapi import FastAPI, Request
from jira_client import get_ticket, post_comment
from llm import generate_test_cases

app = FastAPI()

@app.post("/generate-cases")
async def generate_cases(req: Request):
    data = await req.json()

    comment = data["comment"]["body"]
    issue_key = data["issue"]["key"]

    if "/testcases" in comment:
        ticket = get_ticket(issue_key)
        test_cases = generate_test_cases(ticket)

        post_comment(issue_key, test_cases)

    return {"status": "ok"}