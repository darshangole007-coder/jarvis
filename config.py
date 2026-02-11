import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

if not OPENAI_API_KEY:
    print("⚠ OpenAI key missing – AI fallback disabled")

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

WAKE_WORD = "jarvis"
