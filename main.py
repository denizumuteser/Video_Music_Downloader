import tkinter as tk
from tkinter import scrolledtext
import youtube_dl
import os
import threading

def callable_hook(d):
    if d['status'] == 'finished':
        text_area.insert(tk.END, f"Done: {d['filename']}\n")
    
    #if d['status'] == 'downloading':
    #    print(f"Downloading: {d['filename']} {d['_percent_str']}")
    
    if d['status'] == 'error':
         text_area.insert(tk.END, f"Failed: {d['filename']}\n")

def downloadVideo(videourl, path):
    print("started downloading")
    ydl = youtube_dl.YoutubeDL({
        'outtmpl': '/y-dl/%(title)s.%(ext)s',
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4',
        'progress_hooks':[callable_hook]})
    ydl.download([videourl])

def downloadMusic(videourl, path):
    ydl = youtube_dl.YoutubeDL({
    'outtmpl': '/y-dl/%(title)s.%(ext)s',
    'format': 'bestaudio/best',
    'ffmpeg_location': './ffmpeg/bin/ffmpeg.exe',
    'progress_hooks':[callable_hook],
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192', }]})
    ydl.download([videourl])

def is_supported(url):
    extractors = youtube_dl.extractor.gen_extractors()
    for e in extractors:
        if e.suitable(url) and e.IE_NAME != 'generic':
            return True
    return False

def caller(link1, path, type1):
    type1 = str(type1.get())
    url = str(link1.get())
    
    if is_supported(url):
        if type1 == "v":
            t = threading.Thread(target=downloadVideo, args=(url,path))
        elif type1 == "m":
            t = threading.Thread(target=downloadMusic, args=(url,path))
        t.start()
    else:
        text_area.insert(tk.END, f'URL: "{url}" is not supported.\n')
    link.set("")
        
path = './y-dl'

# Window
window = tk.Tk()
window.geometry("600x400")
window.config(bg="#99ccff")
window.resizable(width=False,height=False)
window.title("By BodosLama")

# variables
link = tk.StringVar()
dtype = tk.StringVar(value="v")

# Title
tk.Label(window,text = '                   Video & Music Downloader                    ', font ='arial 20 bold',fg="White",bg="Black").pack()

# Link
tk.Label(window, text = 'Paste Your Link Here:', font = 'arial 20 bold',fg="Black",bg="#99ccff").place(x= 5 , y = 60) 
link_enter = tk.Entry(window, width = 52,textvariable = link,font = 'arial 15 bold',bg="white")
link_enter.place(x = 10, y = 100)
link_enter.focus_set()

# music or video checkboxes
c1 = tk.Checkbutton(window, text="Video", variable=dtype, onvalue="v", offvalue="m").place(x = 10, y = 150)
c2 = tk.Checkbutton(window, text="Music", variable=dtype, onvalue="m", offvalue="v").place(x = 80, y = 150)

# download button
tk.Button(window,text = 'DOWNLOAD', font = 'arial 15 bold' ,fg="white",bg = 'black', padx = 2,command= lambda: caller(link, path, dtype)).place(x=450 ,y = 140)
window.bind('<Return>', lambda x: caller(link, path, dtype))

# info
text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=70, height=10)
text_area.place(x=10, y=200)

# loop
window.mainloop()
