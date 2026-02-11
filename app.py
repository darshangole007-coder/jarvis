import re
import time
import random
import threading
import queue

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pyttsx3

from automation import *
from ai import ai_reply
from memory import touch, idle_for

app = Flask(__name__)
CORS(app)

# ---------- SPEECH ENGINE (SAFE QUEUE) ----------
engine = pyttsx3.init()
speech_queue = queue.Queue()

def speaker_loop():
    while True:
        text = speech_queue.get()
        engine.stop()
        engine.say(text)
        engine.runAndWait()
        speech_queue.task_done()

threading.Thread(target=speaker_loop, daemon=True).start()

def speak(text):
    touch()
    speech_queue.put(text)

# ---------- IDLE CHATTER ----------
IDLE_LINES = [
    "I appear to be idle, sir.",
    "Awaiting further instructions.",
    "Shall I run a system check?",
    "Existence without tasks is inefficient."
]

def idle_loop():
    while True:
        if idle_for() > 30:
            speak(random.choice(IDLE_LINES))
        time.sleep(30)

threading.Thread(target=idle_loop, daemon=True).start()

# ---------- COMMAND ROUTER ----------
def process(text: str) -> str:
    touch()
    text = text.lower().strip()

    # ---- BASIC TALK ----
    if text in ["hey", "hi", "hello"]:
        return "Yes, sir?"

    if "who are you" in text:
        return "I am JARVIS, your personal assistant."

    if "tell me a joke" in text:
        return "Why do programmers prefer dark mode? Because light attracts bugs."

    # ---- AUTOMATION ----
    if "open chrome" in text:
        return open_chrome()

    if "cpu" in text:
        return system_info("cpu")

    if "ram" in text:
        return system_info("ram")

    if "brightness up" in text:
        return brightness_up()

    if "brightness down" in text:
        return brightness_down()

    # ---- MATH ----
    m = re.search(r"(\d+)\s*([\+\-\*/])\s*(\d+)", text)
    if m:
        a, op, b = m.groups()
        try:
            return f"The answer is {eval(a+op+b)}, sir."
        except:
            return "That calculation failed, sir."

    # ---- EMAIL ----
    if "send email" in text:
        m = re.search(r"to (.+?) message (.+)", text)
        if m:
            return send_email(m.group(1), m.group(2))

    # ---- WHATSAPP ----
    if "send whatsapp" in text:
        m = re.search(r"to (.+?) (.+)", text)
        if m:
            return send_whatsapp(m.group(1), m.group(2))

    # ---- AI FALLBACK (LAST) ----
    return ai_reply(text)

# ---------- ROUTES ----------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "")
    reply = process(msg)
    speak(reply)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
