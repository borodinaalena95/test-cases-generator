import pytest
from unittest.mock import patch, MagicMock
from src.claude_client import call_claude_api


@patch('src.claude_client.anthropic.Anthropic')
def test_call_claude_api_with_base64_image(mock_anthropic_class):
    """Test call_claude_api processes base64-encoded images"""
    mock_client = MagicMock()
    mock_anthropic_class.return_value = mock_client
    
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="Generated test cases")]
    mock_client.messages.create.return_value = mock_message
    
    prompt = "Test prompt"
    images = ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="]
    
    result = call_claude_api(prompt, images)
    
    assert result == "Generated test cases"
    mock_client.messages.create.assert_called_once()


@patch('src.claude_client.anthropic.Anthropic')
def test_call_claude_api_with_plain_base64(mock_anthropic_class):
    """Test call_claude_api handles plain base64 without data: prefix"""
    mock_client = MagicMock()
    mock_anthropic_class.return_value = mock_client
    
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="Generated cases")]
    mock_client.messages.create.return_value = mock_message
    
    prompt = "Test prompt"
    images = ["iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="]
    
    result = call_claude_api(prompt, images)
    
    assert result == "Generated cases"
    
    # Verify that image was processed with default PNG media type
    call_args = mock_client.messages.create.call_args
    messages = call_args[1]["messages"]
    assert "image/png" in str(messages)


@patch('src.claude_client.anthropic.Anthropic')
def test_call_claude_api_with_multiple_images(mock_anthropic_class):
    """Test call_claude_api processes multiple images"""
    mock_client = MagicMock()
    mock_anthropic_class.return_value = mock_client
    
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="Test cases")]
    mock_client.messages.create.return_value = mock_message
    
    prompt = "Analyze these images"
    images = [
        "data:image/png;base64,abc123",
        "data:image/jpeg;base64,def456"
    ]
    
    result = call_claude_api(prompt, images)
    
    assert result == "Test cases"
    
    # Verify both images were included
    call_args = mock_client.messages.create.call_args
    messages = call_args[1]["messages"]
    content = messages[0]["content"]
    
    # Should have 2 image blocks + 1 text block
    image_blocks = [block for block in content if block.get("type") == "image"]
    assert len(image_blocks) == 2


@patch('src.claude_client.anthropic.Anthropic')
def test_call_claude_api_with_empty_images(mock_anthropic_class):
    """Test call_claude_api works with no images"""
    mock_client = MagicMock()
    mock_anthropic_class.return_value = mock_client
    
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="Text-only response")]
    mock_client.messages.create.return_value = mock_message
    
    result = call_claude_api("Just text prompt", [])
    
    assert result == "Text-only response"
    
    call_args = mock_client.messages.create.call_args
    messages = call_args[1]["messages"]
    content = messages[0]["content"]
    
    # Should have only text block
    assert len(content) == 1
    assert content[0]["type"] == "text"


@patch('src.claude_client.anthropic.Anthropic')
def test_call_claude_api_sets_correct_model_and_tokens(mock_anthropic_class):
    """Test that call_claude_api uses correct model and token limits"""
    mock_client = MagicMock()
    mock_anthropic_class.return_value = mock_client
    
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="Result")]
    mock_client.messages.create.return_value = mock_message
    
    call_claude_api("Test", [])
    
    call_args = mock_client.messages.create.call_args
    
    assert call_args[1]["model"] == "claude-sonnet-4-20250514"
    assert call_args[1]["max_tokens"] == 4096

