import os
import platform
import subprocess
import shutil
import webbrowser
import psutil
import time
import json
import smtplib
from email.mime.text import MIMEText
import screen_brightness_control as sbc
import pyautogui
import ctypes
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pyautogui
import requests

SYSTEM = platform.system().lower()

pyautogui = None

if os.environ.get("DISPLAY"):
    import pyautogui
    
# -----------------------------
# APP REGISTRY
# -----------------------------

APP_COMMANDS = {
    "chrome": "chrome",
    "google chrome": "chrome",
    "edge": "msedge",
    "firefox": "firefox",
    "notepad": "notepad",
    "calculator": "calc",
    "spotify": "spotify",
    "discord": "discord",
    "vscode": "code",
    "vs code": "code",
    "excel": "excel",
    "word": "winword",
    "cmd": "cmd",
    "task manager": "taskmgr",
    "settings": "ms-settings:",
    "file explorer": "explorer"
}

APP_PROCESS_NAMES = {
    "chrome": "chrome.exe",
    "edge": "msedge.exe",
    "firefox": "firefox.exe",
    "youtube": "chrome.exe",
    "google": "chrome.exe",
    "notepad": "notepad.exe",
    "spotify": "spotify.exe",
    "discord": "discord.exe",
    "vscode": "code.exe",
    "cmd": "cmd.exe",
    "explorer": "explorer.exe"
}

# -----------------------------
# YOUTUBE CONTROL
# -----------------------------

def youtube_control(action, query=None):
    try:
        if action == "play":
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            webbrowser.open(url)
            time.sleep(4)
            pyautogui.press("tab")
            pyautogui.press("tab")
            pyautogui.press("enter")
            return True, f"Playing {query} on YouTube, sir."

        elif action == "search":
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            webbrowser.open(url)
            return True, f"Searching YouTube for {query}, sir."

        elif action == "open":
            webbrowser.open("https://www.youtube.com")
            return True, "Opening YouTube, sir."

    except Exception as e:
        return False, str(e)


# -----------------------------
# GOOGLE SEARCH + NOTE TAKING
# -----------------------------

def google_research_and_notes(query):

    try:

        # ---------- OPEN BROWSER ----------
        driver = webdriver.Chrome(ChromeDriverManager().install())

        search_url = f"https://www.google.com/search?q={query.replace(' ','+')}"

        driver.get(search_url)

        time.sleep(3)

        # ---------- GET FIRST RESULT ----------
        links = driver.find_elements(By.CSS_SELECTOR, "a")

        first_link = None

        for link in links:
            href = link.get_attribute("href")
            if href and "http" in href and "google" not in href:
                first_link = href
                break

        if not first_link:
            return False,"Could not find a result, boss."

        driver.get(first_link)

        time.sleep(4)

        # ---------- SCRAPE PAGE ----------
        soup = BeautifulSoup(driver.page_source,"html.parser")

        paragraphs = soup.find_all("p")

        notes = ""

        for p in paragraphs[:15]:
            notes += p.get_text()+"\n"

        driver.quit()

        if not notes:
            notes = "No useful text found."

        # ---------- OPEN NOTEPAD ----------
        subprocess.Popen("notepad")
        time.sleep(2)

        # ---------- TYPE NOTES ----------
        pyautogui.write(notes[:2000], interval=0.01)

        # ---------- SAVE FILE ----------
        pyautogui.hotkey("ctrl","s")
        time.sleep(1)

        filename = f"research_{int(time.time())}.txt"

        pyautogui.write(filename)

        pyautogui.press("enter")

        return True,"Research completed and notes saved, boss."

    except Exception as e:
        return False,f"Automation failed: {str(e)}"

# -----------------------------
# SCREENSHOT
# -----------------------------

def take_screenshot():
    try:
        filename = f"screenshot_{int(time.time())}.png"
        path = os.path.join(os.path.expanduser("~/Desktop"), filename)
        pyautogui.screenshot(path)
        return True, f"Screenshot saved to {path}, sir."
    except:
        return False, "Screenshot failed."

# -----------------------------
# LOCK COMPUTER
# -----------------------------

def lock_pc():
    if SYSTEM == "windows":
        ctypes.windll.user32.LockWorkStation()
        return True, "Locking computer, sir."

# -----------------------------
# OPEN FOLDER
# -----------------------------

def open_folder(path):
    try:
        subprocess.Popen(f'explorer "{path}"')
        return True, f"Opening folder {path}, sir."
    except:
        return False, "Failed to open folder."

# -----------------------------
# CREATE FILE
# -----------------------------

def create_file(path, name):
    try:
        full = os.path.join(path, name)
        with open(full, "w") as f:
            f.write("")
        return True, f"File {name} created."
    except:
        return False, "File creation failed."

# -----------------------------
# LIST RUNNING APPS
# -----------------------------

def list_running_apps():
    processes = []
    for proc in psutil.process_iter(['name']):
        processes.append(proc.info['name'])
    return True, processes

# -----------------------------
# KILL PROCESS
# -----------------------------

def kill_process(name):
    try:
        subprocess.run(f"taskkill /f /im {name}", shell=True)
        return True, f"{name} terminated."
    except:
        return False, "Failed to kill process."

# -----------------------------
# EMPTY RECYCLE BIN
# -----------------------------

def empty_recycle_bin():
    try:
        if SYSTEM == "windows":
            subprocess.run("PowerShell.exe Clear-RecycleBin -Force", shell=True)
            return True, "Recycle bin emptied."
    except:
        return False, "Failed."

# -----------------------------
# WIFI CONTROL
# -----------------------------

def wifi_control(action):
    try:
        if action == "off":
            subprocess.run("netsh interface set interface Wi-Fi disable", shell=True)
        elif action == "on":
            subprocess.run("netsh interface set interface Wi-Fi enable", shell=True)
        return True, f"WiFi turned {action}, sir."
    except:
        return False, "WiFi control failed."

# -----------------------------
# MEDIA CONTROL
# -----------------------------

def media_control(action):
    try:
        if action == "play":
            pyautogui.press("playpause")
        elif action == "next":
            pyautogui.press("nexttrack")
        elif action == "previous":
            pyautogui.press("prevtrack")
        return True, f"Media {action}, sir."
    except:
        return False, "Media control failed."

# -----------------------------
# TIMER
# -----------------------------

def set_timer(seconds):
    print(f"Timer started for {seconds} seconds.")
    time.sleep(seconds)
    return True, "Timer finished, sir."

# -----------------------------
# CAMERA OPEN
# -----------------------------

def open_camera():
    try:
        subprocess.run("start microsoft.windows.camera:", shell=True)
        return True, "Opening camera, sir."
    except:
        return False, "Camera failed."

# -----------------------------
# SYSTEM INFO
# -----------------------------

def full_system_info():
    info = {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }

    return True, info
