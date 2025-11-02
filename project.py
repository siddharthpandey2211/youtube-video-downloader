from pytubefix import YouTube
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent = bytes_downloaded / total_size * 100
    progress_label.config(text=f"Progress: {percent:.1f}%")
    progress_label.update()

def start_download():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Warning", "Please enter a YouTube URL.")
        return
    save_path = filedialog.askdirectory(title="Select Download Folder")
    if not save_path:
        return
    status_label.config(text="Starting download...", fg="blue")
    threading.Thread(target=download_video, args=(url, save_path)).start()

def download_video(url, save_path):
    try:
        yt = YouTube(url, on_progress_callback=progress_function)
        stream = yt.streams.get_highest_resolution()
        status_label.config(text=f"Downloading: {yt.title}", fg="blue")
        stream.download(output_path=save_path)
        status_label.config(text=f"✅ Download Complete!\nSaved in: {save_path}", fg="green")
        progress_label.config(text="")
    except Exception as e:
        status_label.config(text=f"❌ Error: {e}", fg="red")
        progress_label.config(text="")

root = tk.Tk()
root.title("🎬 YouTube Downloader")
root.geometry("520x260")
root.resizable(False, False)

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

tk.Label(frame, text="Enter YouTube URL:", font=("Arial", 12)).pack(pady=10)
url_entry = tk.Entry(frame, width=60)
url_entry.pack(pady=5)

tk.Button(frame, text="⬇️ Download", command=start_download, font=("Arial", 11, "bold"), bg="#4CAF50", fg="white").pack(pady=10)

status_label = tk.Label(frame, text="", fg="gray")
status_label.pack(pady=5)
progress_label = tk.Label(frame, text="", fg="gray")
progress_label.pack(pady=5)
tk.Label(frame, text="Note: Downloads highest quality available.", fg="gray").pack(pady=5)

root.mainloop()
