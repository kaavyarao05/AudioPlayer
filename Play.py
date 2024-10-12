from tkinter import *
from tkinter import filedialog
import pygame
from typing_extensions import Self
import os
from enum import Enum

class buttonState(Enum):
    IDLE=0,  #pass
    TOCLICKPREV=1  #can set the first song
    TOCLICKPOST=2  #can set the song to play after clickedSong
curState=buttonState.IDLE

class Song:
    button:Button
    next:Self #Self is class, self is object
    prev:Self
    songName:str
    path:str
    def __init__(self,root,txt,path):
        self.songName=txt
        self.path=path
        self.button=Button(root,text=txt,command=self.clicked)
        self.prev=None
        self.next=None
    def clicked(self):
        match(curState):
            case buttonState.IDLE:
                pass
            case buttonState.TOCLICKPREV:
                changeState(buttonState.TOCLICKPOST,self)
            case buttonState.TOCLICKPOST:
                changeState(buttonState.TOCLICKPREV,self)

def changeState(newstate:buttonState,newsong:Song=None):
    global curState
    curState=newstate
    match(curState):
            case buttonState.IDLE:
                updateLabel("Select a Song to play")
            case buttonState.TOCLICKPOST:
                global clickedSong
                updateLabel("Click on song to play after "+newsong.songName)
                clickedSong=newsong
            case buttonState.TOCLICKPREV:
                if newsong:
                    updateLabel("{songName} will play after {old}".format(songName=newsong.songName,old=clickedSong.songName))
                else:
                    updateLabel("Select Song to link")

def updateLabel(newtext:str):
    global txt
    txt=newtext

clickedSong:Song

root =Tk()
root.title('Music Player')
root.geometry("500x320")

pygame.mixer.init()

menubar=Menu(root)
root.config(menu=menubar)

start:Song=None
songs=[]
currentsong:Song
paused=False

def createNode(path,name):
    global start
    if start:
        new=Song(playlist,name,path)
        ptr=start
        while ptr.next!=None:
            ptr.next.prev=ptr
            ptr=ptr.next
        ptr.next=new
        new.prev=ptr
    else:
        start=Song(playlist,name,path)

def load():
    global currentsong
    root.directory=filedialog.askdirectory()
    for song in os.listdir(root.directory):
        name,ext=os.path.splitext(song)
        if ext==".mp3":
            createNode(song,name)
    currentsong=start

def toggleEditList():
    if curState==buttonState.IDLE:
        changeState(buttonState.TOCLICKPREV)
    else:
        changeState(buttonState.IDLE)
    

def play_music():
    global currentsong,paused
    if not paused:
        pygame.mixer.music.load(os.path.join(root.directory,currentsong.path))
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
    if currentsong:
        currentsong=currentsong.next
        play_music()

def prev_music():
    global paused,currentsong
    if currentsong:
        currentsong=currentsong.prev
        play_music()

organise_menu=Menu(menubar,tearoff=False)
organise_menu.add_command(label="Select Folder",command=load)
organise_menu.add_command(label="Toggle Edit",command=toggleEditList)
menubar.add_cascade(label="Organise",menu=organise_menu)

playlist=Listbox(root,bg="black",fg="white",width=100,height=15)
playlist.pack()

control_frame=Frame(root)
control_frame.pack()

play_btn=Button(control_frame,text="Play",borderwidth=0,command=play_music)
pause_btn=Button(control_frame,text="Pause",borderwidth=0,command=pause_music)

prev_btn=Button(control_frame,text="Prev",borderwidth=0,command=prev_music)
next_btn=Button(control_frame,text="Next",borderwidth=0,command=next_music)



play_btn.grid(row=1,column=1,padx=7,pady=10)
pause_btn.grid(row=1,column=2,padx=7,pady=10)
prev_btn.grid(row=1,column=0,padx=7,pady=10)
next_btn.grid(row=1,column=3,padx=7,pady=10)


txt=""
label=Label(control_frame,text=txt)
label.grid(row=0,columnspan=4)

#s1=Song(control_frame,"s1")
#s1.button.grid(row=2)

def update():
    global txt
    label.config(text=txt)
    root.after(500,update)

changeState(buttonState.IDLE)
update()
root.mainloop()