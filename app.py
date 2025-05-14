from flask import Flask, request, send_from_directory, jsonify
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

app = Flask(__name__)

# 🟢 Directory to save received log files
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'received_logs')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ✉️ Email Configuration (TEMP — use .env instead for real deployment)
SENDER_EMAIL = "hitanshmangla@gmail.com"
SENDER_PASSWORD = "Mangla#1234"
RECEIVER_EMAIL = "ishanntrahulaag@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(subject, body):
    """Function to send email using Gmail's SMTP server"""
    print("📧 Preparing to send email...")
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("✔️ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

@app.route('/', methods=['GET'])
def server_status():
    return jsonify({"message": "Server is running!"}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        print(f"📁 File saved: {file.filename}")

        # 🧠 Analyze after upload
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        analyze_logs(files)

        return jsonify({"message": f"File '{file.filename}' uploaded & analyzed!"}), 200
    except Exception as e:
        return jsonify({"message": f"Upload failed: {str(e)}"}), 500

@app.route('/files', methods=['GET'])
def list_files():
    try:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return jsonify({"files": files}), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching files: {str(e)}"}), 500

def analyze_logs(files, log_directory="received_logs", time_window_minutes=1, threshold=1):
    print("📊 Running analyze_logs...")
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

    for ft in file_times:
        if now - ft <= timedelta(minutes=time_window_minutes):
            suspicious_count += 1

    print(f"🕒 {suspicious_count} files received in last {time_window_minutes} minute(s)")

    if suspicious_count >= threshold:
        print("⚠️ Suspicious Activity Detected!")
        subject = "⚠️ Suspicious Activity Detected!"
        body = "Multiple log files received in short time. Possible infection detected."

        send_email(subject, body)
    else:
        print("✅ No suspicious activity found.")

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"message": "File not found!"}), 404

if __name__ == '__main__':
    print("🚀 Flask Server starting...")
    app.run(debug=True, host='127.0.0.1', port=5000)
