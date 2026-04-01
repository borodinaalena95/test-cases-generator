def save_markdown(text, filename="test_cases.md"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    return filename