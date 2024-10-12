from tkinter import *
from tkinter import filedialog
import pygame
from typing_extensions import Self
import os

class Song:
    data=0
    next:Self
    def __init__(self,data):
        self.data=data
        self.next=None


root =Tk()
root.title('Music Player')
root.geometry("500x300")

pygame.mixer.init()

menubar=Menu(root)
root.config(menu=menubar)

songs=[]
currentsong:str
paused=False

def load_music():
    global currentsong
    root.directory=filedialog.askdirectory()
    for song in os.listdir(root.directory):
        name,ext=os.path.splitext(song)
        if ext==".mp3":
            songs.append(song)
    for song in songs:
        playlist.insert("end",song)
    playlist.selection_set(0)
    currentsong=songs[playlist.curselection()[0]]

def play_music():
    global currentsong,paused
    if not paused:
        pygame.mixer.music.load(os.path.join(root.directory,currentsong))
        pygame.mixer.music.play()
    else:
        pygame.mixer.unpause()
        paused=False

def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused=True

def next_music():
    global paused,currentsong

    try:
        playlist.selection_clear(0,END)
        playlist.selection_set(songs.index(currentsong)+1)
        currentsong=songs[playlist.curselection()[0]]
        play_music()
    except:
        pass

def prev_music():
    global currentsong,paused

    try:
        playlist.select_clear(0,END)
        playlist.selection_set(songs.index(currentsong)-1)
        currentsong=songs[playlist.curselection()[0]]
        play_music()
    except:
        pass


organise_menu=Menu(menubar,tearoff=False)
organise_menu.add_command(label="Select Folder",command=load_music)
menubar.add_cascade(label="Organise",menu=organise_menu)

playlist=Listbox(root,bg="black",fg="white",width=100,height=15)
playlist.pack()

control_frame=Frame(root)
control_frame.pack()

play_btn=Button(control_frame,text="Play",borderwidth=0,command=play_music)
pause_btn=Button(control_frame,text="Pause",borderwidth=0,command=pause_music)

prev_btn=Button(control_frame,text="Prev",borderwidth=0,command=prev_music)
next_btn=Button(control_frame,text="Next",borderwidth=0,command=next_music)

play_btn.grid(row=0,column=1,padx=7,pady=10)
pause_btn.grid(row=0,column=2,padx=7,pady=10)
prev_btn.grid(row=0,column=0,padx=7,pady=10)
next_btn.grid(row=0,column=3,padx=7,pady=10)




root.mainloop()