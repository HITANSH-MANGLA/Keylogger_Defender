import requests
import time
import os
from datetime import datetime, timedelta

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
def analyze_logs(files, log_directory="received_logs", time_window_minutes=1, threshold=1):
    file_times = []

    for file in files:
        try:
            file_path = os.path.join(log_directory, file)
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            file_times.append(file_time)
        except Exception as e:
            print(f"❌ Error getting time for {file}: {e}")

    # 📌 Recent files ko sort karo (latest pehle)
    file_times.sort(reverse=True)

    # 🔍 Check karo kitni files recent X minutes mein bani hain
    suspicious_count = 0
    now = datetime.now()

    for ft in file_times:
        if now - ft <= timedelta(minutes=time_window_minutes):
            suspicious_count += 1

    # 🚨 Threshold cross kiya to suspicious
    if suspicious_count >= threshold:
        print("⚠️ Suspicious Activity Detected! Multiple logs in short time.")
    else:
        print("✅ No suspicious activity found.")

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
