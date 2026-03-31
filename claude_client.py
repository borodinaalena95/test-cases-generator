import anthropic
from anthropic.types import ImageBlockParam, TextBlockParam, MessageParam, Base64ImageSourceParam

from config import CLAUDE_API_KEY

def call_claude_api(prompt: str, images: list[str]) -> str:
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

    content: list[ImageBlockParam | TextBlockParam] = []

    for image in images:
        if image.startswith("data:"):
            media_type, base64_data = image.split(";base64,", 1)
            media_type = media_type.replace("data:", "")
        else:
            # Assuming it's a base64 string without the "data:" prefix
            base64_data = image
            media_type = "image/png"  # Default to PNG if not specified

        source: Base64ImageSourceParam = {
            "type": "base64",
            "media_type": media_type,
            "data": base64_data,
        }
        image_block: ImageBlockParam = {
            "type": "image",
            "source": source,
        }
        content.append(image_block)

    text_block: TextBlockParam = {
        "type": "text",
        "text": prompt
    }
    content.append(text_block)

    messages: list[MessageParam] = [
        {"role": "user", "content": content}
    ]

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=messages
    )

    return message.content[0].text