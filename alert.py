import os
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import time

# ✅ Flask server ka base URL
flask_url = "http://127.0.0.1:5000"

# 🔍 Flask server se available log files ka list fetch karo
def fetch_logs():
    try:
        response = requests.get(f"{flask_url}/files")
        if response.status_code == 200:
            return response.json()["files"]
        else:
            print("❌ Error fetching files from server.")
            return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

# 🔐 Suspicious activity analyze karne ka logic
def analyze_logs(files, log_directory="received_logs", time_window_minutes=1, threshold=2):
    file_times = []

    for file in files:
        try:
            file_path = os.path.join(log_directory, file)
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            file_times.append(file_time)
        except Exception as e:
            print(f"❌ Error getting time for {file}: {e}")

    file_times.sort(reverse=True)

    suspicious_count = 0
    now = datetime.now()

    # Check if more than 2 files were generated in the last 1 minute
    for ft in file_times:
        if now - ft <= timedelta(minutes=time_window_minutes):
            suspicious_count += 1

    # If suspicious activity detected, send email alert
    if suspicious_count >= threshold:  # Threshold for suspicious activity (2 files in 1 minute)
        print("⚠️ Suspicious Activity Detected!")
        send_email_alert("Suspicious Activity Detected!", "Multiple logs detected in the last minute.")
    else:
        print("✅ No suspicious activity found.")

# 🔐 Email bhejne ka function
def send_email_alert(subject, body):
    # Sender and receiver email credentials
    sender_email = "your_email@example.com"
    receiver_email = "receiver@example.com"
    password = "your_email_password"  # Use environment variable for security, not hard-coded!

    # Constructing the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject  # Subject of the email

    # Body of the email
    msg.attach(MIMEText(body, 'plain'))  # Email content

    try:
        # Connecting to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Use TLS encryption for security
        server.login(sender_email, password)  # Login to the sender's email account
        server.sendmail(sender_email, receiver_email, msg.as_string())  # Send the email
        print("⚠️ Email alert sent successfully!")  # Print confirmation on success
    except Exception as e:
        print(f"❌ Error sending email: {e}")  # Print error if something goes wrong
    finally:
        server.quit()  # Close the connection to the server

# 🔁 Har 30 sec mein detection check karo
def check_for_suspicious_activity():
    while True:
        print("\n🔍 Checking for suspicious activity...")
        files = fetch_logs()

        if files:
            print(f"📁 Found {len(files)} files. Analyzing...")
            analyze_logs(files)
        else:
            print("📂 No log files found.")

        print("⏳ Waiting 30 seconds for next check...\n")
        time.sleep(30)  # ⏲️ Check every 30 seconds

# ✅ Script ka entry point
if __name__ == "__main__":
    check_for_suspicious_activity()
