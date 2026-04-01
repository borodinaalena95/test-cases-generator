from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_root_endpoint():
    """Test that root endpoint returns ok status"""
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch('src.api.get_ticket')
@patch('src.api.generate_test_cases')
@patch('src.api.save_markdown')
@patch('src.api.upload_attachment')
def test_generate_cases_with_testcases_command(mock_upload, mock_save, mock_generate, mock_get_ticket):
    """Test generate_cases endpoint when /testcases command is present"""
    mock_get_ticket.return_value = {
        "title": "Feature",
        "description": "Desc",
        "images": []
    }
    mock_generate.return_value = "# Test Cases"
    mock_save.return_value = "test_cases.md"
    
    payload = {
        "comment": {"body": "Please generate /testcases"},
        "issue": {"key": "TEST-123"}
    }
    
    response = client.post("/generate-cases", json=payload)
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    
    mock_get_ticket.assert_called_once_with("TEST-123")
    mock_generate.assert_called_once()
    mock_save.assert_called_once_with("# Test Cases")
    mock_upload.assert_called_once()


@patch('src.api.get_ticket')
@patch('src.api.generate_test_cases')
@patch('src.api.save_markdown')
@patch('src.api.upload_attachment')
def test_generate_cases_ignores_requests_without_testcases(mock_upload, mock_save, mock_generate, mock_get_ticket):
    """Test generate_cases endpoint ignores comments without /testcases command"""
    payload = {
        "comment": {"body": "Just a regular comment"},
        "issue": {"key": "TEST-123"}
    }
    
    response = client.post("/generate-cases", json=payload)
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    
    # Functions should not be called if /testcases is not in comment
    mock_get_ticket.assert_not_called()
    mock_generate.assert_not_called()
    mock_save.assert_not_called()
    mock_upload.assert_not_called()

