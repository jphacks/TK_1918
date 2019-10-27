#!/usr/bin/env python3
import tkinter
from tkinter import *
import cv2
import PIL.Image, PIL.ImageTk
import time
import video_canvas
import illustration_canvas
import video_canvas
import GazeEstimate

class App:
    def __init__(self,window,window_title,video_source=0):
        self.v_size = (420,280)
        self.v_pos = (0,0)
        self.i_size = (600,400)
        self.i_pos = (570,330)

        self.window = window
        self.window.title= window_title
        self.window.geometry("1280x720")

        #Camvasを配置
        self.v_can = tkinter.Canvas(self.window,width=self.v_size[0],height=self.v_size[1])
        self.i_can = tkinter.Canvas(self.window,width=self.i_size[0],height=self.i_size[1])
        #self.v_can.place(x=0,y=0)
        self.v_can.place(x=self.v_pos[0],y=self.v_pos[1])
        self.i_can.place(x=self.i_pos[0],y=self.i_pos[1])

        #open video source
        video_source=0
        #video_source = "http://10.10.0.200:8081/"
        self.vid = video_canvas.MyVideoCapture(video_source)

        #open illust canvas
        self.il = illustration_canvas.Canvas(width = self.i_size[0],height = self.i_size[1])
        # Button that lets the user take a snapshot
        #self.btn_snapshot=tk.Button(window, text="Snapshot", width=50, command=self.snapshot)
        #self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

        logofile=PhotoImage(file="logo_min.png")
        self.logo_can=Canvas(width=400,height=200)
        self.logo_can.place(x=self.v_pos[0], y=self.v_pos[1] + self.v_size[1])
        self.logo_can.create_image(0,0,image=logofile,anchor=NW)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.v_video_delay=15
        self.v_video_update()

        self.v_gaze_delay = 300
        self.v_gaze_update()

        self.i_delay=200
        self.i_update()

        self.window.mainloop()

    def v_video_update(self):
        #get a frame from the video source
        ret, v_frame = self.vid.get_frame()
        #vid_size = (self.vid.get(cv2.CAP_PROP_FRAME_WIDTH),self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

        if ret:
            v_frame = cv2.resize(v_frame,self.v_size,fx=self.v_size[0]/v_frame.shape[0],fy=self.v_size[1]/v_frame.shape[1])
            self.v_photo=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(v_frame))
            #self.v_can.create_image(self.v_pos[0],self.v_pos[1], image = self.v_photo, anchor = tkinter.NW)
            #self.v_can.create_image(self.v_size[0]/2,self.v_size[1]/2, image = self.v_photo, anchor = tkinter.NW)
            self.v_can.create_image(0,0, image = self.v_photo, anchor = tkinter.NW)
        self.window.after(self.v_video_delay,self.v_video_update)

    def v_gaze_update(self):
        res = self.vid.get_gaze()
        self.il.add_point(x=res[0],y=res[1])
        self.window.after(self.v_gaze_delay,self.v_gaze_update)

    def i_update(self):
        ret,i_frame = self.il.get_frame()

        if ret:
            i_frame = cv2.resize(i_frame,self.i_size,fx=self.i_size[0]/i_frame.shape[0],fy=self.i_size[1]/i_frame.shape[1])
            self.i_photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(i_frame))
            self.i_can.create_image(0, 0, image = self.i_photo, anchor = tkinter.NW)
        self.window.after(self.i_delay,self.i_update)

App(tkinter.Tk(), "Oekaki Hack")

