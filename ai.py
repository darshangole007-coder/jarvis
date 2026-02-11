from config import client

SYSTEM_PROMPT = (
    "You are JARVIS, a calm, intelligent AI assistant. "
    "Be concise, polite, and helpful."
)

def ai_reply(text: str) -> str:
    if not client:
        return "My knowledge systems are offline, sir."

    try:
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            max_tokens=120
        )
        return r.choices[0].message.content.strip()
    except Exception:
        return "I am unable to answer that right now, sir."
