import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = None

if OPENROUTER_API_KEY and OPENROUTER_API_KEY.startswith("sk-"):
    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "Jarvis"
        }
    )
print("OPENROUTER KEY:", OPENROUTER_API_KEY)