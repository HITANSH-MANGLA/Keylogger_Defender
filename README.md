# 🔐 Keylogger Defender Tool

A full-stack cybersecurity project that simulates, detects, and defends against keylogger-based attacks. This project includes a custom keylogger developed in **C# (.NET Framework)**, a **Flask server** to receive keystroke logs, and a **Python-based GUI with a detection system** to monitor and alert users of potential keylogging activities.

---

## 📌 Project Components

### 1. 🎯 Keylogger Module (C# – .NET Framework)
- Captures all keystrokes from the user's system.
- Stores them in a `.txt` log file.
- Sends logs every **30 seconds** to a remote Flask server using HTTP POST.
- Runs silently in the background.

### 2. 🌐 Remote Server (Flask – Python)
- Receives incoming keystroke logs.
- Automatically organizes them into folders based on the device ID.
- Stores all data securely for analysis.

### 3. 🖥️ Defender GUI (Python)
- Visual interface to view received log files.
- Automatically lists devices and their respective log folders.
- Built using `Tkinter` / `PyQt`.

### 4. 🛡️ Detection System (Python)
- Monitors outgoing network activity for signs of keylogger infection.
- Identifies frequent unknown IP communications.
- Generates alerts if suspicious patterns are detected.

---

## ⚙️ Technologies Used

- `C# (.NET Framework)`
- `Python`
- `Flask`
- `Tkinter / PyQt`
- `Requests`
- `Socket`
- `Threading`
- `OS / File I/O`

---

## 📂 Project Structure

Keylogger-Defender-Tool/
├── keylogger/ # C# code (Keylogger)
├── flask_server/ # Python Flask server
├── detection_gui/ # GUI + detection system
├── requirements.txt
├── README.md
└── documentation/ # Report, PPT, references


---

## 🧠 Challenges Faced

- Ensuring stealth background execution without user disruption.
- Automating consistent file transfers to the server.
- Designing a generic yet effective detection algorithm.
- Managing network behavior analysis and alert system.
- Building a dynamic GUI for real-time file monitoring.

---

## 📊 Features

- 🔑 Keystroke logging and log management
- 📡 Periodic file transmission to server
- 🧩 Real-time network monitoring
- 🚨 Keylogger detection with alert mechanism
- 📁 GUI-based file viewer for analysis

---

## 🧪 Use Cases

> For **educational and research purposes only**

- Cybersecurity awareness and training
- Real-time intrusion simulation and detection
- End-to-end project for ethical hacking demonstrations
- Research tool for malware behavior

---

## 🛠️ Setup Instructions

1. Clone the repository:

2. Set up the Flask server:
```bash
cd flask_server
pip install -r requirements.txt
python app.py
cd detection_gui
python gui.py
Build and run the C# keylogger from Visual Studio.
