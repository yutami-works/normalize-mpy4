import os
import tkinter as tk
from tkinter import filedialog
from moviepy.editor import *
from pydub import AudioSegment

def browse_input_file():
    input_file_path.set(filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")]))

def browse_output_file():
    output_file_path.set(filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")]))

def normalize_audio():
    # Load video and extract audio
    video = VideoFileClip(input_file_path.get())
    audio = video.audio
    audio.write_audiofile("temp.wav")

    # Normalize audio
    sound = AudioSegment.from_wav("temp.wav")
    sound = sound.normalize()
    sound.export("normalized_temp.wav", format="wav")

    # Replace audio in video
    normalized_audio = AudioFileClip("normalized_temp.wav")
    normalized_video = video.set_audio(normalized_audio)
    normalized_video.write_videofile(output_file_path.get())

    # Cleanup
    video.close()
    audio.close()
    normalized_audio.close()
    os.remove("temp.wav")
    os.remove("normalized_temp.wav")

# Create GUI
root = tk.Tk()
root.title("NormalizeMPy4")

input_file_path = tk.StringVar()
output_file_path = tk.StringVar()

tk.Label(root, text="Input MP4 File:").grid(row=0, column=0, sticky="e")
tk.Entry(root, textvariable=input_file_path, width=50).grid(row=0, column=1)
tk.Button(root, text="Browse", command=browse_input_file).grid(row=0, column=2)

tk.Label(root, text="Output MP4 File:").grid(row=1, column=0, sticky="e")
tk.Entry(root, textvariable=output_file_path, width=50).grid(row=1, column=1)
tk.Button(root, text="Browse", command=browse_output_file).grid(row=1, column=2)

tk.Button(root, text="Normalize Audio", command=normalize_audio).grid(row=2, column=1)

root.mainloop()