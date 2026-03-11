from config import client

SYSTEM_PROMPT = (
    "You are JARVIS, a highly intelligent AI assistant. "
    "Be calm, professional, and address the user as 'sir'."
)

def ai_reply(text: str) -> str:

    if client is None:
        return "AI systems offline, sir."

    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("AI ERROR:", e)
        return "Cloud intelligence temporarily unavailable, sir."