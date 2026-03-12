import os
import re
import threading
import queue
import psutil
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime

# Internal Imports
from automation import *
from ai import ai_reply
from memory import touch

app = Flask(__name__)
CORS(app)

# ---------- SPEAK FUNCTION (SERVER SAFE) ----------
def speak(text):
    touch()
    print("Assistant:", text)   # log instead of speaking


# ---------- COMMAND ROUTER ----------
def process_command(text: str) -> str:
    touch()
    text = text.lower().strip()

    # -----------------------------
    # GREETING
    # -----------------------------
    if text in ["hey", "hi", "hello", "jarvis"]:
        return "At your service, boss."

    # -----------------------------
    # TIME
    # -----------------------------
    if "time" in text:
        return f"The time is {datetime.now().strftime('%H:%M')}, boss."

    # -----------------------------
    # SYSTEM STATUS
    # -----------------------------
    if "battery" in text:
        ok, msg = get_battery_info()
        return msg

    if "cpu" in text:
        ok, msg = get_system_info("cpu")
        return msg

    if "memory" in text or "ram" in text:
        ok, msg = get_system_info("memory")
        return msg

    # -----------------------------
    # OPEN APPLICATION
    # -----------------------------
    if text.startswith("open "):

        app_name = text.replace("open ", "").strip()

        if app_name in APP_COMMANDS:
            open_app(app_name)
            return f"Opening {app_name}, boss."

        if app_name == "youtube":
            ok, msg = youtube_control("open")
            return msg

        if app_name == "spotify":
            ok, msg = spotify_control("open")
            return msg

        if app_name in ["github","gmail","google","chatgpt"]:
            ok, msg = open_website(app_name)
            return msg

        return f"I could not find {app_name}, boss."

    # -----------------------------
    # CLOSE APPLICATION
    # -----------------------------
    if text.startswith("close "):

        name = text.replace("close ", "").strip()

        if close_app(name):
            return f"Closing {name}, boss."

        return f"I couldn't close {name}, boss."

    # -----------------------------
    # PLAY MUSIC / YOUTUBE
    # -----------------------------
    if "play" in text and "youtube" in text:

        song = text.replace("play", "").replace("on youtube", "").strip()

        ok, msg = youtube_control("play", song)

        return msg

    if text.startswith("play "):

        song = text.replace("play", "").strip()

        ok, msg = youtube_control("play", song)

        return msg


    # -----------------------------
    # GOOGLE RESEARCH + NOTES
    # -----------------------------
    if "search google for" in text and "notes" in text:

        query = text.replace("search google for","")
        query = query.replace("take necessary notes","")
        query = query.replace("important notes","")
        query = query.replace("save it to notepad","")
        query = query.strip()

        ok,msg = google_research_and_notes(query)

        return msg


    # -----------------------------
    # CREATE FOLDER
    # -----------------------------
    if "create folder" in text:

        words = text.split()

        if "name" in words:
            name = words[words.index("name") + 1]
        else:
            name = "NewFolder"

        ok, msg, _ = create_folder("documents", name)

        return msg


    # -----------------------------
    # CREATE VS CODE PROJECT
    # -----------------------------
    if "create project" in text or ("create folder" in text and "vs code" in text):
        words = text.split()

        if "name" in words:
            project = words[words.index("name") + 1]
        else:
            project = "my_project"

        ok, msg, _ = create_vscode_project(project)

        return msg


    # -----------------------------
    # SCREENSHOT
    # -----------------------------
    if "screenshot" in text:

        ok, msg = take_screenshot()

        return msg


    # -----------------------------
    # WIFI CONTROL
    # -----------------------------
    if "wifi off" in text:

        ok, msg = wifi_control("off")

        return msg

    if "wifi on" in text:

        ok, msg = wifi_control("on")

        return msg


    # -----------------------------
    # BRIGHTNESS
    # -----------------------------
    if "brightness up" in text:

        ok, msg = brightness_control("increase")

        return msg

    if "brightness down" in text:

        ok, msg = brightness_control("decrease")

        return msg


    # -----------------------------
    # LOCK COMPUTER
    # -----------------------------
    if "lock computer" in text:

        ok, msg = lock_pc()

        return msg


    # -----------------------------
    # MATH
    # -----------------------------
    m = re.search(r"(\d+)\s*([\+\-\*/])\s*(\d+)", text)

    if m:
        a, op, b = m.groups()
        try:
            res = eval(f"{a}{op}{b}")
            return f"The result is {res}, boss."
        except:
            return "Calculation error."


    # -----------------------------
    # AI FALLBACK
    # -----------------------------
    response = ai_reply(text)

    return response


# ---------- FLASK ROUTES ----------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/voice/start", methods=["POST"])
def voice_start():
    return {"status": "listening"}


@app.route("/voice/stop", methods=["POST"])
def voice_stop():
    return {"status": "stopped"}


@app.route("/voice/command", methods=["POST"])
def voice_command():

    data = request.json
    command = data.get("text", "")

    print("Voice command:", command)

    reply = process_command(command)

    speak(reply)

    return jsonify({"response": reply})


@app.route("/chat", methods=["POST"])
def chat():

    try:
        data = request.json
        user_text = data.get("message", "")

        reply = process_command(user_text)

        speak(reply)

        return jsonify({"reply": reply})

    except Exception as e:
        print("Server error:", e)

        return jsonify({"reply": "Internal system error, boss."}), 500


# ---------- RUN SERVER ----------
if __name__ == "__main__":
    app.run(port=5001, debug=True)
