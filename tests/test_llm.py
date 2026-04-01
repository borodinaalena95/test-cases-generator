import pytest
from unittest.mock import patch, MagicMock
from src.llm import build_prompt, generate_test_cases, call_llm_api


def test_build_prompt_includes_ticket_info():
    """Test that build_prompt includes ticket title and description"""
    ticket = {
        "title": "Add user login feature",
        "description": "Users should be able to log in with email and password"
    }
    
    prompt = build_prompt(ticket)
    
    assert "Add user login feature" in prompt
    assert "Users should be able to log in with email and password" in prompt
    assert "senior QA engineer" in prompt
    assert "UI validation" in prompt


def test_build_prompt_with_empty_description():
    """Test build_prompt handles empty description"""
    ticket = {
        "title": "Test feature",
        "description": ""
    }
    
    prompt = build_prompt(ticket)
    
    assert "Test feature" in prompt
    assert isinstance(prompt, str)
    assert len(prompt) > 0


@patch('src.llm.call_llm_api')
def test_generate_test_cases_calls_api(mock_api):
    """Test that generate_test_cases calls call_llm_api with correct params"""
    mock_api.return_value = "# Test Cases\n- Test 1"
    
    ticket = {
        "title": "Feature",
        "description": "Description",
        "images": ["image1.png"]
    }
    
    result = generate_test_cases(ticket)
    
    assert mock_api.called
    assert result == "# Test Cases\n- Test 1"


@patch('src.llm.CLAUDE_API_KEY', 'valid-key')
@patch('src.llm.call_claude_api')
def test_call_llm_api_with_valid_key(mock_claude):
    """Test call_llm_api with valid API key"""
    mock_claude.return_value = "Generated test cases"
    
    result = call_llm_api("Test prompt", [])
    
    assert result == "Generated test cases"
    mock_claude.assert_called_once()


@patch('src.llm.CLAUDE_API_KEY', None)
def test_call_llm_api_without_key_raises_error():
    """Test that call_llm_api raises error when API key is missing"""
    with pytest.raises(ValueError, match="No API key found"):
        call_llm_api("Test prompt", [])

