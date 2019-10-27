import cv2
import GazeEstimate

class MyVideoCapture:
    def __init__(self,video_source):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source",video_source)

        #get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

        #set default value to gazeinfo
        self.gazeinfo_default = {"reye":[self.width/2,self.height/2],
                "leye":[self.width/2,self.height/2],
                "gaze":[0,0]
                }
        self.gazeinfo = self.gazeinfo_default
        #reduction rate for computing the gaze
        self.red_r = 0.3

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
#        self.window.mainloop()

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                #Return a boolean success flag and the current frame converted to BGR
                frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                reye = self.gazeinfo["reye"]
                leye = self.gazeinfo["leye"]
                gaze = self.gazeinfo["gaze"]
                cv2.circle(frame, (int(reye[0]), int(reye[1])), 15, eyesColor, thickness=2)
                cv2.circle(frame, (int(leye[0]), int(leye[1])), 15, eyesColor, thickness=2)
                center = ((reye[0]+leye[0])/2, (reye[1]+leye[1])/2)
                gazeTop = (center[0] + gazeLen * math.sin(math.radians(gaze[0])), center[1] + gazeLen * math.sin(math.radians(gaze[1])))
                return(ret, frame)
            else:
                return(ret,None)
        else:
            return(ret,None)

    def get_gaze(self,frame) -> dict:
        ret,frame = self.vid.read()
        if not ret:
            return self.gazeinfo_default
        size = (self.width*self.red_r, self.height*self_red_r)
        cv2.resize(frame,size)
        self.gazeinfo = GazeEstimate.estimateGaze(frame)
