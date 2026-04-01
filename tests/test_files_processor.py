import os
import pytest
from src.files_processor import save_markdown


def test_save_markdown_creates_file(tmp_path):
    """Test that save_markdown creates a file with correct content"""
    test_content = "# Test Cases\n\n- Test 1\n- Test 2"
    file_path = str(tmp_path / "test_output.md")
    
    result = save_markdown(test_content, file_path)
    
    assert os.path.exists(result)
    assert result == file_path
    
    with open(result, "r", encoding="utf-8") as f:
        content = f.read()
    
    assert content == test_content


def test_save_markdown_default_filename(tmp_path, monkeypatch):
    """Test save_markdown with default filename"""
    monkeypatch.chdir(tmp_path)
    test_content = "# Default Test"
    
    result = save_markdown(test_content)
    
    assert result == "test_cases.md"
    assert os.path.exists(result)
    
    with open(result, "r", encoding="utf-8") as f:
        content = f.read()
    
    assert content == test_content


def test_save_markdown_overwrites_existing_file(tmp_path):
    """Test that save_markdown overwrites existing files"""
    file_path = str(tmp_path / "test.md")
    
    save_markdown("Original content", file_path)
    save_markdown("New content", file_path)
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    assert content == "New content"

