# pip install requests
import base64
from pathlib import Path
import requests
import os
from dotenv import load_dotenv

PAGE=3

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
INPUT_FILE = Path(f"in/page-{PAGE}.png")
OUTPUT_FILE = Path(f"out/page-{PAGE}.md")
MODEL_NAME = 'gemini-2.0-flash'

HEADERS = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"

def encode_image_to_base64(image_path: Path) -> str:
    """Encode image to base64"""
    with image_path.open(mode='rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def main() -> None:
    base64_image = encode_image_to_base64(image_path=INPUT_FILE)
    payload = {
        "contents": [{
            "parts": [
                {"text": 'Extract all text exactly as shown. Remove word breaks ("-") and replace line breaks with space. Thank you!'},
                {
                    "inline_data": {
                        "mime_type": "image/png",
                        "data": base64_image
                    }
                }
            ]
        }]
    }

    response = requests.post(
        API_URL,
        headers=HEADERS,
        params={"key": GEMINI_API_KEY},
        json=payload
    )

    if response.status_code == 200:
        image_text_data = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        with OUTPUT_FILE.open(mode='w', encoding='utf-8') as out_file:
            out_file.write(image_text_data)
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


if __name__ == '__main__':
    main()