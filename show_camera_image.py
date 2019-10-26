import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

class MyVideoCapture:
    def __init__(self,video_source=0):
        #open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueErro("Unable to open video source",video_source)

        #get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
#        self.window.mainloop()

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                #Return a boolean success flag and the current frame converted to BGR
                return(ret, cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
            else:
                return(ret,None)
        else:
            return(ret,None)


class App:
    def __init__(self,window,window_title,video_source=0):
        self.window = window
        self.window.title=(window_title)
        self.video_source=video_source

        #open video source
        self.vid = MyVideoCapture(video_source)

        #create a canvas that can fit the above 
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay=15
        self.update()

        self.window.mainloop()

    def snapshot(self):
        #get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    def update(self):
        #get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        self.window.after(self.delay,self.update)

App(tkinter.Tk(), "Tkinker and OpenCV")
