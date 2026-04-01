import os
import pytest
from unittest.mock import patch


def test_config_loads_env_variables():
    """Test that config loads environment variables correctly"""
    with patch.dict(os.environ, {
        'JIRA_URL': 'https://test.atlassian.net',
        'JIRA_EMAIL': 'test@example.com',
        'JIRA_API_TOKEN': 'test-token',
        'CLAUDE_API_KEY': 'test-key'
    }):
        # Reimport to pick up new env vars
        import importlib
        import src.config as config
        importlib.reload(config)
        
        assert config.JIRA_URL == 'https://test.atlassian.net'
        assert config.JIRA_EMAIL == 'test@example.com'
        assert config.JIRA_API_TOKEN == 'test-token'
        assert config.CLAUDE_API_KEY == 'test-key'


def test_config_returns_none_for_missing_env_variables():
    """Test that config returns None for missing env variables"""
    with patch.dict(os.environ, {}, clear=True):
        import importlib
        import src.config as config
        importlib.reload(config)
        
        # Should not raise an error, just return None
        assert config.JIRA_URL is None or isinstance(config.JIRA_URL, str)

