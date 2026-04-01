from fastapi import Request, APIRouter
from src.jira_client import get_ticket, upload_attachment
from src.files_processor import save_markdown
from src.llm import generate_test_cases

router = APIRouter()

@router.get("/")
def root():
    return {"status": "ok"}

@router.post("/generate-cases")
async def generate_cases(req: Request):
    data = await req.json()

    comment = data["comment"]["body"]
    issue_key = data["issue"]["key"]

    if "/testcases" in comment:
        ticket = get_ticket(issue_key)
        test_cases = generate_test_cases(ticket)

        file_path = save_markdown(test_cases)
        upload_attachment(issue_key, file_path)

    return {"status": "ok"}
