from config import CLAUDE_API_KEY
from claude_client import call_claude_api


def build_prompt(ticket):
    return f"""
    You are a senior QA engineer.
    
    Analyze the Jira ticket AND attached UI designs.
    
    Generate structured test cases including:
    - UI validation
    - API validation
    - Edge cases
    - Accessibility issues
    - Missing requirements
    
    Return .md markdown with:
    - title
    - steps
    - expected_result
    - priority (P0/P1/P2)
    - test_level (unit/api/ui)
    - automation (yes/no + reason)
    
    Ticket Title:
    {ticket['title']}
    
    Ticket Description:
    {ticket['description']}
    
    - group test cases by test level (unit/api/ui) and priority (P0/P1/P2).
    - flag any missing information in the ticket that would be needed to create test cases.
    """

def generate_test_cases(ticket):
    return call_llm_api(
        prompt=build_prompt(ticket),
        images=ticket["images"]  # pass URLs or base64
    )

def call_llm_api(prompt: str, images: list[str]) -> str:
    if CLAUDE_API_KEY:
        response = call_claude_api(prompt, images)
        return response
    else:
        raise ValueError("No API key found for Claude")
