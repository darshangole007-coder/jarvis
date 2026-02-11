import webbrowser
import psutil
import pywhatkit
import smtplib
from email.mime.text import MIMEText
import screen_brightness_control as sbc

from config import EMAIL_USER, EMAIL_PASS

# ---------- BROWSER ----------
def open_chrome():
    webbrowser.open("https://www.google.com")
    return "Opening Chrome, sir."

# ---------- SYSTEM INFO ----------
def system_info(kind):
    if kind == "cpu":
        return f"CPU usage is {psutil.cpu_percent()} percent, sir."
    if kind == "ram":
        return f"RAM usage is {psutil.virtual_memory().percent} percent, sir."

# ---------- BRIGHTNESS ----------
def brightness_up():
    cur = sbc.get_brightness()[0]
    sbc.set_brightness(min(cur + 10, 100))
    return "Brightness increased, sir."

def brightness_down():
    cur = sbc.get_brightness()[0]
    sbc.set_brightness(max(cur - 10, 0))
    return "Brightness decreased, sir."

# ---------- EMAIL ----------
def send_email(to, msg):
    if not EMAIL_USER or not EMAIL_PASS:
        return "Email is not configured, sir."

    m = MIMEText(msg)
    m["From"] = EMAIL_USER
    m["To"] = to
    m["Subject"] = "Message from JARVIS"

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.login(EMAIL_USER, EMAIL_PASS)
        s.send_message(m)

    return "Email sent successfully, sir."

# ---------- WHATSAPP ----------
def send_whatsapp(number, msg):
    pywhatkit.sendwhatmsg_instantly(number, msg, wait_time=10)
    return "WhatsApp message sent, sir."
