# Unit Tests

Unit tests for the Test Cases Generator project using pytest and mocking.

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run tests for a specific module
python -m pytest tests/test_jira_client.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

```

## Test Patterns

- Uses `unittest.mock` for external API mocking (Jira, Claude, file I/O)
- Uses `tmp_path` fixture for temporary file operations


