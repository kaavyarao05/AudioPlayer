
# UPDATE UI TO SHOW LABELS
from tkinter import *
from tkinter import filedialog
from pytube import YouTube 
import os

from moviepy.editor import *

win=Tk()
win.geometry("400x300")
win.title("YouTube Downloader")

info=Label(win,text="Download")

def MP4ToMP3(mp4, mp3):
    FILETOCONVERT = AudioFileClip(mp4)
    FILETOCONVERT.write_audiofile(mp3)
    FILETOCONVERT.close()

def write(content):
    wl= open("C:/projects/soundthing/FulfilledWishlist.txt","+a")
    wl.write(content)
    wl.close()

def downloadmp3(url,destination='UnderTheTree'):
    yt = YouTube(url=url)
    new_file = yt.title + '.wav'
    if new_file in os.listdir(destination):
        info["text"]="{} found in {}, Skipped".format(new_file,destination)
        return
    video = yt.streams.filter(only_audio=True).first() 
    out_file = video.download(output_path=destination) 
    MP4ToMP3(out_file,new_file)
    os.remove(out_file)
    write("Title: {}\nURL: {}\nPath: {}\n\n".format(yt.title,url,new_file))
    info["text"]="{} Successfully Downloaded".format(yt.title)

def Wishlist():
    with open("C:/projects/soundthing/Wishlist.txt","r+") as fp:
        content=fp.readlines()
        for url in content:
            try:
                downloadmp3(url.rstrip())
                
            except:
                info["text"]="{} was not found".format(url)        
            fp.seek(0)
            fp.write("")
        fp.truncate()

def setUI():
    selectdirButton=Button(win,text="Download Wishlist",command=Wishlist)
    selectdirButton.pack(pady=30)
    info.pack()


def update():
   win.after(1000, update) # run itself again after 1000 ms

if __name__=="__main__":
    setUI()
    update()
    win.mainloop()