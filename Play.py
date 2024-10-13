from tkinter import *
from tkinter import filedialog
import pygame
from typing_extensions import Self
import os
from enum import Enum

class buttonState(Enum):
    IDLE=0,        #play songs
    TOCLICKPREV=1  #can set the first song
    TOCLICKPOST=2  #can set the song to play after clickedSong
curState:buttonState

class Song:
    button:Button
    next:Self #Self is class, self is object
    prev:Self
    songName:str
    path:str
    def __init__(self,txt,path):
        self.songName=txt
        self.path=path
        self.prev=None
        self.next=None
    def clicked(self):
        match(curState):
            case buttonState.IDLE:
                global currentsong
                currentsong=self
                play_music()
            case buttonState.TOCLICKPREV:
                changeState(buttonState.TOCLICKPOST,self)
            case buttonState.TOCLICKPOST:
                changeState(buttonState.TOCLICKPREV,self)
    def setButton(self):
        self.button=Button(canvasframe,text=self.songName,command=self.clicked)
        fitInGrid(self.button)
    def destroyButton(self):
        self.button.destroy()
        self.button=None

class PlayList:
    PlaylistName:str=""
    path:str=""
    start:Song=None
    def __init__(self,path,name):
        self.path=path
        self.PlaylistName=name

def set_vol(val):
    pygame.mixer.music.set_volume(float(val)/100)

def setNext(song:Song,next:Song):
    song.next=next
    next.prev=song

clickedSong:Song
def changeState(newstate:buttonState,newsong:Song=None):
    global curState
    curState=newstate
    match(curState):
            case buttonState.IDLE:
                unpause_music()
                updateLabel("Select a Song to play")
            case buttonState.TOCLICKPOST:
                global clickedSong
                updateLabel("Click on song to play after "+newsong.songName)
                clickedSong=newsong
            case buttonState.TOCLICKPREV:
                if newsong:
                    setNext(clickedSong,newsong)
                    updateLabel("{songName} will play after {old}".format(songName=newsong.songName,old=clickedSong.songName))
                else:
                    pause_music()
                    updateLabel("Select Song to link")

def updateLabel(newtext:str):
    label.config(text=newtext)

root =Tk()
root.title('Music Player')
root.geometry("500x360")

pygame.mixer.init()

menubar=Menu(root)
root.config(menu=menubar)

playlists:list[PlayList]=[]
currentplaylist:PlayList=None
currentsong:Song=None
paused=False

gridrow=0
gridcol=0

def fitInGrid(songButton:Button):
    global gridcol,gridrow
    songButton.grid(row=gridrow)
    gridrow+=1

def createNode(path,name,playlist):
    if playlist.start:
        new=Song(name,path)
        ptr=playlist.start
        while ptr.next!=None:
            ptr.next.prev=ptr
            ptr=ptr.next
        ptr.next=new
        new.prev=ptr
        new.setButton()
    else:
        playlist.start=Song(name,path)
        playlist.start.setButton()

def clearplaylist():
    if currentplaylist:
        ptr:Song=currentplaylist.start
        while ptr!=None:
            ptr.destroyButton()
            ptr=ptr.next

def changePlaylist(newplaylist:PlayList):
    global currentplaylist
    clearplaylist()
    currentplaylist=newplaylist
    ptr:Song=currentplaylist.start
    while ptr!=None:
        ptr.setButton()
        ptr=ptr.next


def load_playlist():
    global currentsong,currentplaylist
    dir=filedialog.askdirectory()
    if dir:
        clearplaylist()
        playlist=PlayList(dir,"Playlist{}".format(len(playlists)))
        playlists.append(playlist)
        currentplaylist=playlist
        
        for songpath in os.listdir(playlist.path):
            name,ext=os.path.splitext(songpath)
            if ext==".mp3":
                createNode(songpath,name,playlist)
        currentsong=playlist.start
        addPlaylistToMenu(playlist)

def toggleEditList():
    if curState==buttonState.IDLE:
        changeState(buttonState.TOCLICKPREV)
    else:
        changeState(buttonState.IDLE)

def addPlaylistToMenu(playlist:PlayList):
    playlist_menu.add_command(label=playlist.PlaylistName,command=lambda:playlistClicked(playlist))

def playlistClicked(playlist:PlayList):
    changePlaylist(playlist)

def play_music():
        global currentsong,paused
        if not paused:
            updateLabel("Currently playing: {}".format(currentsong.songName))
            pygame.mixer.music.load(os.path.join(currentplaylist.path,currentsong.path))
            pygame.mixer.music.play()
        else:
            unpause_music()

def updateLabelTemporarily(newtext,time=1500):
    oldtext=label['text']
    updateLabel(newtext)
    root.after(time,lambda:updateLabel(oldtext))

def buttoncheck()->bool:
    if curState==buttonState.IDLE:
        if currentsong:
            return True
        else:
            updateLabelTemporarily("Select Playlist in Organise")
            return False
    else:
        updateLabel("In Edit Mode")
        return False

def unpause_music():
        global paused
        if currentsong:updateLabel("Currently playing: {}".format(currentsong.songName))
        pygame.mixer.music.unpause()
        paused=False

def pause_music():
        global paused
        updateLabel("Paused")
        pygame.mixer.music.pause()
        paused=True

def next_music():
        global paused,currentsong
        if currentsong.next:
            currentsong=currentsong.next
            play_music()
        else:
            updateLabelTemporarily("Nothing next")

def prev_music():
        global paused,currentsong
        if currentsong.prev:
            currentsong=currentsong.prev
            play_music()
        else:
            updateLabelTemporarily("Nothing previous")

organise_menu=Menu(menubar,tearoff=False)
organise_menu.add_command(label="Load Playlist",command=load_playlist)
organise_menu.add_command(label="Toggle Edit",command=toggleEditList)

playlist_menu=Menu(menubar,tearoff=False)
for playlist in playlists:
    addPlaylistToMenu(playlist)

menubar.add_cascade(label="Organise",menu=organise_menu)
menubar.add_cascade(label="Playlists",menu=playlist_menu)

label=Label(root)
label.pack()

canvas=Canvas(root,bg="black",width=500,height=250)
canvas.pack()
canvasframe=Frame(root,bg="black")
canvasframe.place(x=250, y=25, anchor=N)
canvasframe.pack_propagate(False)

def play_clicked():
    if buttoncheck():
        play_music()

def pause_clicked():
    if buttoncheck():
        pause_music()

def next_clicked():
    if buttoncheck():
        next_music()

def prev_clicked():
    if buttoncheck():
        prev_music()


control_frame=Frame(root)
control_frame.pack()

play_btn=Button(control_frame,text="Play",borderwidth=0,command=play_clicked)
pause_btn=Button(control_frame,text="Pause",borderwidth=0,command=pause_clicked)

prev_btn=Button(control_frame,text="Prev",borderwidth=0,command=prev_clicked)
next_btn=Button(control_frame,text="Next",borderwidth=0,command=next_clicked)

volslider = Scale(control_frame,from_=1,to=100,orient = HORIZONTAL,command=set_vol)
volslider.set(50)
volslider.grid(row=0,columnspan=4)

play_btn.grid(row=1,column=1)
pause_btn.grid(row=1,column=2)
prev_btn.grid(row=1,column=0)
next_btn.grid(row=1,column=3)

changeState(buttonState.IDLE)

if __name__=="__main__":
    root.mainloop()