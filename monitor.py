import subprocess
import time
import json
import threading
import re
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

hosts = ["google.com", "github.com", "cisco.com", "abc.fake.server"]
data = {}

# 🔥 EMAIL FUNCTION
def send_email_alert(host):
    sender_email = "gireeshsbhajantri@gmail.com"
    receiver_email = "gireeshsbhajantri@gmail.com"

    # 👇 PASTE YOUR APP PASSWORD HERE (no spaces)
    app_password = "lbmy tqau fxow dvcx"

    subject = f"🚨 ALERT: {host} is DOWN"
    body = f"The host {host} has been DOWN for 3 consecutive checks."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print(f"[EMAIL SENT] Alert for {host}")
    except Exception as e:
        print("Email error:", e)


# 🔥 PING FUNCTION (with regex fix)
def ping_host(host):
    try:
        output = subprocess.check_output(
            ["ping", "-n", "1", host],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        ).lower()

        if "reply from" in output:
            match = re.search(r'time[=<]\s*(\d+)', output)
            latency = match.group(1) if match else "0"
            return "UP", latency

        return "DOWN", None

    except:
        return "DOWN", None


# 🔥 MAIN MONITOR
def monitor():
    global data
    alert_state = {}

    while True:
        for host in hosts:
            status, latency = ping_host(host)

            if host not in data:
                data[host] = {
                    "history": [],
                    "uptime": 0,
                    "checks": 0
                }

            if host not in alert_state:
                alert_state[host] = {
                    "fail_count": 0
                }

            data[host]["checks"] += 1

            if status == "UP":
                data[host]["uptime"] += 1
                alert_state[host]["fail_count"] = 0
            else:
                alert_state[host]["fail_count"] += 1

                # 🚨 ALERT + EMAIL
                if alert_state[host]["fail_count"] == 3:
                    print(f"[CRITICAL ALERT] 🚨 {host} DOWN for 3 consecutive checks!")
                    send_email_alert(host)

            uptime_percent = (data[host]["uptime"] / data[host]["checks"]) * 100

            entry = {
                "time": datetime.now().strftime("%H:%M:%S"),
                "status": status,
                "latency": latency,
                "uptime": round(uptime_percent, 2)
            }

            data[host]["history"].append(entry)

            if len(data[host]["history"]) > 50:
                data[host]["history"].pop(0)

        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)

        time.sleep(5)


def start_monitoring():
    thread = threading.Thread(target=monitor)
    thread.daemon = True
    thread.start()