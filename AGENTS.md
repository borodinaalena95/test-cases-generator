# AGENTS.md - Test Cases Generator

## Project Overview

**TestCasesGenerator** is a Python automation tool that generates structured QA test cases from Jira tickets combined with UI design images. The system extracts ticket metadata via Jira API, sends images + ticket details to Claude AI for analysis, and outputs markdown-formatted test cases.

### Architecture: Three-Module Pipeline

```
User Input (ticket_id)
    ↓
jira_client.py: Fetch ticket + image attachments from Jira
    ↓
llm.py: Send ticket + images to Claude Sonnet for test case generation
    ↓
main.py: Orchestrate and output markdown results
```

## Key Patterns & Conventions

### 1. **Data Flow: Ticket Object Structure**

The `get_ticket()` function returns a standardized dict that flows through the pipeline:

```python
ticket = {
    "title": str,          # from Jira summary field
    "description": str,    # from Jira description field
    "images": list[str]    # URLs or base64-encoded image strings
}
```

**Critical:** Images can be either direct URLs or base64-encoded strings prefixed with `data:image/...;base64,`. The `call_llm_api()` function handles both formats via conditional parsing.

### 2. **LLM Integration: Image + Text Combined Prompting**

- **Model:** Claude Sonnet 4 (`claude-sonnet-4-20250514`) for cost-efficiency with multimodal support
- **Max tokens:** 4096 for comprehensive test case generation
- **Message structure:** Images appended first, then text prompt (important for token efficiency)
- **Image handling:** Must convert URL images to base64 before API submission if not already encoded

### 3. **Authentication & Environment Variables**

Three Jira API credentials required as environment variables (no defaults):

```
JIRA_URL      # e.g., https://company.atlassian.net
JIRA_EMAIL    # Basic auth email
JIRA_API_TOKEN # API token (not password)
```

**Setup:** Export before running: `export JIRA_URL=... JIRA_EMAIL=... JIRA_API_TOKEN=...`

### 4. **Prompt Engineering: QA-Focused Structure**

The `build_prompt()` function embeds the QA instruction template that drives Claude's output format:

- **Test organization:** Grouped by test_level (unit/api/ui) + priority (P0/P1/P2)
- **Required fields:** Each test case must include title, steps, expected_result, priority, test_level, automation (yes/no + reasoning)
- **Special detection:** Flag missing ticket information that prevents test case creation
- **Accessibility:** Explicitly requested as validation category (WCAG compliance checks)

### 5. **Error Handling & Edge Cases**

- **Missing images:** Function accepts empty list; Claude proceeds with text-only analysis
- **Image encoding fallback:** URLs without `data:` prefix default to PNG media type
- **API failures:** No retry logic currently—Jira 404s or auth failures surface immediately
- **Large attachments:** 4096-token limit may truncate for complex test suites; consider pagination

## Dependencies & Versions

```
anthropic         # Claude API client (no version pinned—use latest)
requests          # HTTP library for Jira
```

**Important:** The `anthropic` library must be recent enough to support `ImageBlockParam` and `Base64ImageSourceParam` types (v0.28.0+).

## Development Workflows

### Running End-to-End

```bash
export JIRA_URL="https://your-instance.atlassian.net"
export JIRA_EMAIL="your-email@company.com"
export JIRA_API_TOKEN="your-api-token"
python main.py
# > Enter Jira ticket ID: PROJ-123
# > [markdown output with organized test cases]
```

### Testing Individual Modules

```bash
# Test Jira client directly
python -c "from jira_client import get_ticket; print(get_ticket('PROJ-123'))"

# Test LLM prompt generation
python -c "from llm import build_prompt; print(build_prompt({'title': 'Test', 'description': 'Desc'}))"
```

### Debugging

- Add `print()` statements in `llm.py` to inspect the content list before API call (check image encoding)
- Jira errors: Verify token validity and ticket ID format (usually `PROJECT-NUMBER`)
- Claude API errors: Check Anthropic dashboard for rate limits or account issues

## AI Agent Guidance

### When Adding Features

1. **Image handling changes:** Update both URL-to-base64 conversion logic in `call_llm_api()` AND test with various image formats (PNG, JPEG, WebP)
2. **Prompt refinement:** Edit only `build_prompt()` function; test output format consistency before deploying
3. **Jira API extensions:** Add new fields to ticket dict in `get_ticket()` (e.g., `priority`, `labels`); update `build_prompt()` to include them

### When Debugging

- Ticket object structure is the contract between modules—verify `get_ticket()` returns expected keys before suspecting `llm.py`
- Claude response structure follows markdown; if output breaks test case parsing, check prompt template first
- Image encoding errors usually manifest as Claude API 400 errors; inspect `content` list structure

### Conventions to Maintain

- **No external file I/O:** All data flows through function returns (not files/caches)
- **Environment-based config:** Never hardcode credentials or URLs
- **Markdown output assumption:** Downstream tools may parse the markdown format; preserve the structure defined in `build_prompt()`

