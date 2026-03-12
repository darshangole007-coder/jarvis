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
import ctypes
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

SYSTEM = platform.system().lower()

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

# -----------------------------
# YOUTUBE CONTROL
# -----------------------------

def youtube_control(action, query=None):
    try:
        if action == "play":
            url = f"https://www.youtube.com/results?search_query={query.replace(' ','+')}"
            webbrowser.open(url)
            return True, f"Opening YouTube search for {query}, boss."

        elif action == "search":
            url = f"https://www.youtube.com/results?search_query={query.replace(' ','+')}"
            webbrowser.open(url)
            return True, f"Searching YouTube for {query}, boss."

        elif action == "open":
            webbrowser.open("https://www.youtube.com")
            return True, "Opening YouTube, boss."

    except Exception as e:
        return False, str(e)

# -----------------------------
# GOOGLE RESEARCH + NOTE TAKING
# -----------------------------

def google_research_and_notes(query):

    try:

        driver = webdriver.Chrome(ChromeDriverManager().install())

        search_url = f"https://www.google.com/search?q={query.replace(' ','+')}"

        driver.get(search_url)

        time.sleep(3)

        links = driver.find_elements(By.CSS_SELECTOR,"a")

        first_link = None

        for link in links:
            href = link.get_attribute("href")
            if href and "http" in href and "google" not in href:
                first_link = href
                break

        if not first_link:
            return False,"Could not find result."

        driver.get(first_link)

        time.sleep(4)

        soup = BeautifulSoup(driver.page_source,"html.parser")

        paragraphs = soup.find_all("p")

        notes = ""

        for p in paragraphs[:15]:
            notes += p.get_text()+"\n"

        driver.quit()

        if not notes:
            notes = "No useful text found."

        filename = f"research_{int(time.time())}.txt"

        with open(filename,"w",encoding="utf-8") as f:
            f.write(notes)

        return True,f"Research completed. Notes saved to {filename}, boss."

    except Exception as e:
        return False,f"Automation failed: {str(e)}"

# -----------------------------
# SCREENSHOT (SERVER SAFE)
# -----------------------------

def take_screenshot():
    return False,"Screenshots not supported on cloud servers."

# -----------------------------
# LOCK COMPUTER
# -----------------------------

def lock_pc():
    if SYSTEM == "windows":
        ctypes.windll.user32.LockWorkStation()
        return True,"Locking computer, boss."

# -----------------------------
# OPEN FOLDER
# -----------------------------

def open_folder(path):
    try:
        subprocess.Popen(f'explorer "{path}"')
        return True,f"Opening folder {path}"
    except:
        return False,"Failed to open folder."

# -----------------------------
# CREATE FILE
# -----------------------------

def create_file(path,name):
    try:
        full=os.path.join(path,name)
        with open(full,"w") as f:
            f.write("")
        return True,f"File {name} created."
    except:
        return False,"File creation failed."

# -----------------------------
# LIST RUNNING APPS
# -----------------------------

def list_running_apps():

    processes=[]

    for proc in psutil.process_iter(['name']):
        processes.append(proc.info['name'])

    return True,processes

# -----------------------------
# KILL PROCESS
# -----------------------------

def kill_process(name):

    try:
        subprocess.run(f"taskkill /f /im {name}",shell=True)
        return True,f"{name} terminated."
    except:
        return False,"Failed to kill process."

# -----------------------------
# EMPTY RECYCLE BIN
# -----------------------------

def empty_recycle_bin():

    try:
        if SYSTEM=="windows":
            subprocess.run("PowerShell.exe Clear-RecycleBin -Force",shell=True)
            return True,"Recycle bin emptied."
    except:
        return False,"Failed."

# -----------------------------
# WIFI CONTROL
# -----------------------------

def wifi_control(action):

    try:
        if action=="off":
            subprocess.run("netsh interface set interface Wi-Fi disable",shell=True)
        elif action=="on":
            subprocess.run("netsh interface set interface Wi-Fi enable",shell=True)

        return True,f"WiFi turned {action}"
    except:
        return False,"WiFi control failed."

# -----------------------------
# MEDIA CONTROL
# -----------------------------

def media_control(action):

    return False,"Media control not supported on server."

# -----------------------------
# TIMER
# -----------------------------

def set_timer(seconds):

    print(f"Timer started for {seconds} seconds")

    time.sleep(seconds)

    return True,"Timer finished."

# -----------------------------
# CAMERA
# -----------------------------

def open_camera():

    return False,"Camera access not available on cloud."

# -----------------------------
# SYSTEM INFO
# -----------------------------

def full_system_info():

    info={
        "cpu":psutil.cpu_percent(),
        "ram":psutil.virtual_memory().percent,
        "disk":psutil.disk_usage('/').percent
    }

    return True,info
