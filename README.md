# Test Cases Generator

An AI-powered API that automatically generates test cases from Jira tickets using Claude AI. When triggered via a Jira comment, it analyzes the ticket content and attached images, generates structured test cases, and uploads them back to the ticket as a markdown attachment.

## How It Works

1. A user adds a comment containing `/testcases` to a Jira ticket
2. Jira automation triggers a webhook to this API
3. The API fetches the ticket details and any attached images
4. Claude AI analyzes the ticket and generates test cases
5. The test cases are uploaded as a markdown attachment to the ticket

## Local Development

### Prerequisites

- Python 3.12+
- A Jira account with API access
- A Claude API key

### Setup

1. Clone the repository

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Copy the environment example file and fill in your values:
   ```bash
   cp .env.example .env
   ```

4. Edit `.env` with your actual credentials:
   - `JIRA_URL` - Your Jira instance URL (e.g., `https://your-domain.atlassian.net`)
   - `JIRA_EMAIL` - Your Jira account email
   - `JIRA_API_TOKEN` - Your Jira API token ([Generate one here](https://id.atlassian.com/manage-profile/security/api-tokens))
   - `CLAUDE_API_KEY` - Your Claude API key

5. Run the server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

   You should see:
   ```
   Uvicorn running on http://127.0.0.1:8000
   ```

## Deployment

This is an API service that needs to be deployed to a publicly accessible server for Jira to send webhooks to it. You can deploy it to platforms like:

- [Railway](https://railway.app)
- Heroku
- AWS
- Any server with a public URL

Make sure to set the environment variables in your deployment platform.

## Jira Automation Setup

To use this service with Jira, you need to create a Jira automation rule:

1. Go to your Jira project settings
2. Navigate to **Automation**
3. Create a new rule with:
   - **Trigger**: "Issue commented"
   - **Condition**: Comment contains `/testcases`
   - **Action**: "Send web request"
     - URL: `https://your-deployed-url.com/generate-cases`
     - Method: POST
     - Body: Use the issue and comment data (Jira provides smart values like `{{issue.key}}`)

When the automation runs, it will call your API, which will generate test cases and upload them as an attachment to the Jira ticket.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check - returns `{"status": "ok"}` |
| POST | `/generate-cases` | Generates test cases from a Jira webhook payload |
