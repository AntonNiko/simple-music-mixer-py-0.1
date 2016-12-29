import tkinter as tk
from tkinter import ttk,filedialog
import pygame as pg
import os
from mutagen.mp3 import MP3
from mutagen.flac import FLAC

LARGE_FONT = ("Verdana",12)

class Window(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        tk.Tk.iconbitmap(self,default="icon.ico")
        tk.Tk.wm_title(self,"Music Mixer")
        
        container = tk.Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames = {}
        frame1 = StartPage(container,self)
        frame2 = PageOne(container,self)
        self.frames[StartPage] = frame1
        self.frames[PageOne] = frame2
        frame1.grid(row=0,column=0,sticky="nsew")
        frame2.grid(row=0,column=0,sticky="nsew")
        self.showFrame(StartPage)

    def showFrame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        global label,inputField,button1
        tk.Frame.__init__(self,parent)
        label = ttk.Label(self,text="MP3 Music Mixer",font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self,text="Go to Mixer",
                            command=lambda:controller.showFrame(PageOne))
        button1.pack(pady=10,padx=10)

class PageOne(tk.Frame):
    isPlaying = False
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text="Music Player",font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        self.currentFilename = ttk.Label(self,text="lol")
        self.currentFilename.pack(pady=5,padx=5)
    
        self.button1 = ttk.Button(self,text="Choose audio to play",command=lambda:self.chooseSong())
        self.button1.pack(pady=5,padx=5)

        ## Audio play/pause button
        self.pausePlayButton = ttk.Button(self,text="Pause",command=lambda:self.pauseSong())
        self.pausePlayButton.pack(pady=5,padx=5)
        
        ## Return to Home page
        button2 = ttk.Button(self,text="Return to Original",command=lambda:controller.showFrame(StartPage))
        button2.pack(pady=5,padx=5)

    def chooseSong(self):
        file = filedialog.askopenfilename(filetypes=(("Audio files", "*.mp3;*.flac"),
                                                     ("All files", "*.*")))

        filename,fileExtension = os.path.splitext(file)
        if fileExtension == ".mp3":
            ## .mp3 data fetch
            audioFile = MP3(file)
            sampleRate = audioFile.info.sample_rate
            channels = audioFile.info.channels
        elif fileExtension == ".flac":
            print("lol")
            ## .flac data fetch
            audioFile = FLAC(file)
            sampleRate = audioFile.info.sample_rate
            channels = audioFile.info.channels

        pg.mixer.quit()
        pg.mixer.init(sampleRate,-16,channels,2048)
        pg.mixer.music.set_volume(0.8)
        self.currentFilename.config(text=file)
        try:
            pg.mixer.music.load(file)
            pg.mixer.music.play()
            self.isPlaying = True
        except pg.error:
            print("Unable to open this file, try again")
        
    def pauseSong(self):
        if self.isPlaying:
            pg.mixer.music.pause()
            self.pausePlayButton.configure(text="Play",command=lambda:self.unpauseSong())
            self.isPlaying = False

    def unpauseSong(self):
        if not self.isPlaying:
            pg.mixer.music.unpause()
            self.pausePlayButton.configure(text="Pause",command=lambda:self.pauseSong())
            self.isPlaying = True

app = Window()
app.mainloop()
