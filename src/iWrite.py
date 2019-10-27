import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import video_canvas
import illustration_canvas
import video_canvas
import GazeEstimate

class App:
    def __init__(self,window,window_title,video_source=0):
        v_size = (420,280)
        v_pos = (0,0)
        i_size = (600,400)
        i_pos = (570,330)

        self.window = window
        self.window.title= window_title
        self.window.geometry("1280x720")

        #Camvasを配置
        self.v_can = tkinter.Canvas(self.window,width=v_size[0],height=v_size[1])
        self.i_can = tkinter.Canvas(self.window,width=i_size[0],height=i_size[1])
        #self.v_can.place(x=0,y=0)
        self.v_can.place(x=v_pos[0],y=v_pos[1])
        self.i_can.place(x=i_pos[0],y=i_pos[1])

        #open video source
        video_source=0
        self.vid = video_canvas.MyVideoCapture(video_source)

        #open illust canvas
        self.il = illustration_canvas.Canvas(width = i_size[0],height = i_size[1])
        # Button that lets the user take a snapshot
        #self.btn_snapshot=tk.Button(window, text="Snapshot", width=50, command=self.snapshot)
        #self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.v_delay=15
        self.v_update()

        self.i_delay=500
        self.i_update()

        self.window.mainloop()

    def v_update(self):
        #get a frame from the video source
        ret, v_frame = self.vid.get_frame()

        if ret:
            res = GazeEstimate.estimateGaze(v_frame)
            self.v_photo=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(v_frame))
            self.v_can.create_image(0, 0, image = self.v_photo, anchor = tk.NW)
            self.il.add_point(res)
        self.window.after(self.v_delay,self.v_update)

    def i_update(self):
        ret,frame = self.i_l.get_frame()

        if ret:
            self.i_photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(i_frame))
            self.i_can.create_image(0, 0, image = self.v_photo, anchor = tk.NW)
        self.window.after(self.i_delay,self.i_update)

App(tkinter.Tk(), "Tkinker and OpenCV")
