from fileinput import filename
from tkinter import*
import tkinter as tk
from tkinter.filedialog import askopenfile
from turtle import forward
from tkVideoPlayer import TkinterVideo
from math import *
from PIL import ImageTk, Image
import datetime
import string

#create root
root  = tk.Tk()
root.title("TKinter Videoplayer")
root.geometry("1000x600")
root.configure(bg = "black")

#Load images
forwardImg=ImageTk.PhotoImage(Image.open("img/forward.png"))
backImg=ImageTk.PhotoImage(Image.open("img/back.png"))
openImg = ImageTk.PhotoImage(Image.open("img/open.png"))
closeImg = ImageTk.PhotoImage(Image.open("img/close.png"))

playImg = ImageTk.PhotoImage(Image.open("img/play.png"))
pauseImg = ImageTk.PhotoImage(Image.open("img/pause.png"))


playing = False

#video player
player = TkinterVideo(master = root, scaled = True, bg = "black")
video_length = 0


#load file from user's device
def openFile():
    file = askopenfile(mode="r", filetypes=[('Video Files', ['*.mp4', '*.mov'])])
    
    if file is not None:
        global filename 
        global playing
        playing = False
        filename = file.name
        global player
        #player = TkinterVideo(master=root, bg = "black")
        player.set_size((1000, 800), False)
        player.load(r"{}".format(filename))
        player.pack(expand = True, fill = "both")
        slider.config(to=0, from_=0)
        #virtual event binding to the video player
        player.bind("<<SecondChanged>>", update_slider)
        player.bind("<<Duration>>", update_elapse)
        player.bind("<<Ended>>", close_vid)
        current_time.set(-1)
#pack player to fill max width
player.pack(expand=True, fill="both", side=TOP)


def playVid():
    #global
    global playing
    
    #change image in button and player's play/pause
    if playing:
        playing = False
        player.pause()
        startBtn["image"] = playImg
    else:
        player.play()
        playing=True
        startBtn["image"] = pauseImg

#delete videoframe 
def termVid():
    global playing
    player.destroy()
    playing = False

#seek till user's value on scale
def seek(value):
    player.seek(int(value))
    
def set_volume(value):
    volume = int(value)/100
    

controls = Frame(root, width=1000, height = 90, bg ="black")
controls.pack_propagate(False)
controls.pack(fill=X, side=BOTTOM, padx=0)

current_time= tk.IntVar(player)
slider = Scale(controls,variable=current_time, from_=0, to=0, orient=HORIZONTAL,bg ="black", fg = "white", command = seek)
slider.pack(fill=X)

#change slider position to reflect video progress
def update_slider(event):
    current_time.set(player.current_duration())
    #the +0.5 acts as rounding
    vid_progress["text"] = str(datetime.timedelta(seconds=(player.current_duration())+0.5)).split(".")[0]

    
#set total length of loaded video
def update_elapse(event):
    duration = player.video_info()["duration"]
    slider["to"] = duration
    video_length["text"] = ("/"+str(datetime.timedelta(seconds=duration+0.5)).split(".")[0])

#skip time 
def jump(time):
    player.seek(int(slider.get())+time)
    current_time.set(slider.get() + time)

#reset player at end of vid
def close_vid(event):
    global playing
    playing = False
    slider.set(slider["to"])
    startBtn["image"] = playImg
    slider.set(0)

#button container grid-------------------------------------
buttonParent = Frame(controls, width=500, height = 200, bg ="black")
buttonParent.pack_propagate(False)
buttonParent.grid_columnconfigure(0, weight=(1))
buttonParent.grid_columnconfigure(1, weight=(1))
buttonParent.grid_columnconfigure(2, weight=(5))
buttonParent.grid_columnconfigure(3, weight=(1))
buttonParent.grid_columnconfigure(4, weight=(1))
buttonParent.place(relx=0.25, rely = 0.5, relwidth=0.5, relheight=1)


#Buttons---------------------------------------------
openVideo = tk.Button(buttonParent,image = openImg, fg = "black", font =("Arial", 10), bg = "white", command = lambda:openFile()).grid(column=0, row=1, padx = 5)
b5 = tk.Button(buttonParent, image = backImg, fg = "black", font =("Arial", 10), bg = "white", command = lambda:jump(-5)).grid(column=1, padx = 5,row=1)
startBtn = tk.Button(buttonParent, image = playImg, fg = "black", font =("Arial", 15), bg = "white", command =playVid)
startBtn.grid(column=2, padx = 5,row=1)
f5 = tk.Button(buttonParent, image=forwardImg, fg = "black", font =("Arial", 20), bg = "white", command = lambda:jump(5)).grid(column=3, padx = 5,row=1)
terminateBtn = tk.Button(buttonParent, image = closeImg, fg = "black", font =("Arial", 10), command = lambda:termVid()).grid(column=4, padx = 5, row=1)


#video time elapse
vid_progress = tk.Label(controls, bg ="black",fg = "white",text=str(datetime.timedelta(seconds=0)))
vid_progress.pack(side=LEFT)

#total length of vid
video_length = Label(controls, bg ="black",fg = "white",text=("/"+str(datetime.timedelta(seconds=0))))
video_length.pack(side=LEFT)

#main loop
root.mainloop()