import pytest
from unittest.mock import patch, MagicMock, mock_open
from src.jira_client import get_ticket, upload_attachment
import base64


@patch('src.jira_client.requests.get')
def test_get_ticket_returns_correct_structure(mock_get):
    """Test that get_ticket returns a dict with title, description, and images"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "fields": {
            "summary": "Test feature",
            "description": "Test description",
            "attachment": []
        }
    }
    mock_get.return_value = mock_response
    
    result = get_ticket("TEST-123")
    
    assert isinstance(result, dict)
    assert "title" in result
    assert "description" in result
    assert "images" in result
    assert result["title"] == "Test feature"
    assert result["description"] == "Test description"
    assert result["images"] == []


@patch('src.jira_client.requests.get')
def test_get_ticket_with_image_attachments(mock_get):
    """Test that get_ticket processes image attachments"""
    # Mock Jira API response
    jira_response = MagicMock()
    jira_response.json.return_value = {
        "fields": {
            "summary": "Feature with images",
            "description": "Description",
            "attachment": [
                {
                    "mimeType": "image/png",
                    "content": "http://example.com/image.png"
                }
            ]
        }
    }
    
    # Mock image download response
    image_response = MagicMock()
    image_response.content = b"fake-image-data"
    
    # First call returns Jira ticket, second call returns image
    mock_get.side_effect = [jira_response, image_response]
    
    result = get_ticket("TEST-123")
    
    assert len(result["images"]) == 1
    assert result["images"][0].startswith("data:image/png;base64,")


@patch('src.jira_client.requests.get')
def test_get_ticket_skips_non_image_attachments(mock_get):
    """Test that get_ticket ignores non-image attachments"""
    jira_response = MagicMock()
    jira_response.json.return_value = {
        "fields": {
            "summary": "Feature",
            "description": "Description",
            "attachment": [
                {
                    "mimeType": "application/pdf",
                    "content": "http://example.com/file.pdf"
                },
                {
                    "mimeType": "image/jpeg",
                    "content": "http://example.com/image.jpg"
                }
            ]
        }
    }
    
    image_response = MagicMock()
    image_response.content = b"fake-image"
    
    mock_get.side_effect = [jira_response, image_response]
    
    result = get_ticket("TEST-123")
    
    # Only one image (JPEG), PDF should be skipped
    assert len(result["images"]) == 1
    assert "image/jpeg" in result["images"][0]


@patch('src.jira_client.requests.post')
@patch('builtins.open', new_callable=mock_open, read_data=b"test content")
def test_upload_attachment_posts_to_jira(mock_file, mock_post):
    """Test that upload_attachment posts file to Jira"""
    mock_response = MagicMock()
    mock_post.return_value = mock_response
    
    upload_attachment("TEST-123", "test_cases.md")
    
    assert mock_post.called
    call_args = mock_post.call_args
    
    # Verify the URL is correct
    assert "TEST-123" in call_args[0][0]
    assert "/attachments" in call_args[0][0]


@patch('src.jira_client.requests.post')
@patch('builtins.open', new_callable=mock_open)
def test_upload_attachment_raises_on_error(mock_file, mock_post):
    """Test that upload_attachment raises error on failed upload"""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("Upload failed")
    mock_post.return_value = mock_response
    
    with pytest.raises(Exception):
        upload_attachment("TEST-123", "test_cases.md")

