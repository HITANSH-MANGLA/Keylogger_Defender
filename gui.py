import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import requests
from datetime import datetime

# 🔹 Configuration
flask_url = "http://127.0.0.1:5000"

# 🔹 Refresh files list from server
def refresh_files():
    listbox.delete(*listbox.get_children())
    status_label.config(text="🔄 Fetching logs...", fg="blue")

    try:
        response = requests.get(f"{flask_url}/files")
        if response.status_code == 200:
            files = response.json().get("files", [])
            if not files:
                messagebox.showinfo("Info", "No log files found on server.")
                status_label.config(text="⚠ No logs available!", fg="orange")
                return
            for file in files:
                listbox.insert("", "end", values=(file,))
            status_label.config(text="✅ Logs loaded!", fg="green")
        else:
            messagebox.showerror("Error", "Failed to fetch files!")
            status_label.config(text="❌ Fetch failed!", fg="red")
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching files: {str(e)}")
        status_label.config(text="❌ Server error!", fg="red")

# 🔹 Upload a file to server
def upload_file():
    file_path = filedialog.askopenfilename(title="Select a log file to upload")
    if not file_path:
        return

    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{flask_url}/upload", files=files)

        if response.status_code == 200:
            messagebox.showinfo("Success", "File uploaded successfully!")
            refresh_files()
        else:
            messagebox.showerror("Error", f"Upload failed: {response.text}")
    except Exception as e:
        messagebox.showerror("Error", f"Upload error: {e}")

# 🔹 Download selected file
def download_file():
    selected = listbox.focus()
    if not selected:
        messagebox.showwarning("Warning", "Please select a file!")
        return

    filename = listbox.item(selected)['values'][0]

    try:
        response = requests.get(f"{flask_url}/download/{filename}")
        if response.status_code == 200:
            save_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=filename)
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                messagebox.showinfo("Success", f"File saved at: {save_path}")
        else:
            messagebox.showerror("Error", f"Download failed: {response.text}")
    except Exception as e:
        messagebox.showerror("Error", f"Download error: {e}")

# 🔹 Check Flask server status
def check_server_status():
    try:
        response = requests.get(flask_url)
        if response.status_code == 200:
            server_status.config(text="🟢 Flask Server: RUNNING", fg="green")
        else:
            server_status.config(text="🔴 Flask Server: ERROR", fg="red")
    except:
        server_status.config(text="🔴 Flask Server: NOT RUNNING", fg="red")

# 🏠 Main GUI Window
root = tk.Tk()
root.title("Keylogger Log Manager")
root.geometry("700x500")
root.configure(bg="#E8F0F2")

# 🔹 Title
title_label = tk.Label(root, text="🔐 Keylogger Log Manager", font=("Helvetica", 20, "bold"), bg="#E8F0F2", fg="#333")
title_label.pack(pady=20)

# 🔹 Server Status Label
server_status = tk.Label(root, text="Checking Flask Server...", font=("Helvetica", 12), bg="#E8F0F2")
server_status.pack()

# 🔹 Logs Treeview
tree_frame = tk.Frame(root, bg="#E8F0F2")
tree_frame.pack(pady=20)

columns = ("Filename",)
listbox = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)

for col in columns:
    listbox.heading(col, text=col)
    listbox.column(col, anchor=tk.CENTER, width=400)

listbox.pack(side=tk.LEFT)

# Scrollbar
scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)

# 🔹 Buttons
btn_frame = tk.Frame(root, bg="#E8F0F2")
btn_frame.pack(pady=10)

refresh_btn = ttk.Button(btn_frame, text="🔄 Refresh", command=refresh_files)
refresh_btn.grid(row=0, column=0, padx=10)

upload_btn = ttk.Button(btn_frame, text="⬆ Upload", command=upload_file)
upload_btn.grid(row=0, column=1, padx=10)

download_btn = ttk.Button(btn_frame, text="⬇ Download", command=download_file)
download_btn.grid(row=0, column=2, padx=10)

exit_btn = ttk.Button(btn_frame, text="❌ Exit", command=root.quit)
exit_btn.grid(row=0, column=3, padx=10)

# 🔹 Status Label
status_label = tk.Label(root, text="🔍 Loading...", font=("Helvetica", 12), bg="#E8F0F2", fg="blue")
status_label.pack(pady=10)

# 🔹 Initialize
check_server_status()
refresh_files()

# 🏁 Run GUI
root.mainloop()

