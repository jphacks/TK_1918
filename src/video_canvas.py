import cv2
import GazeEstimate
import math

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
        self.red_r = 0.2
        self.eyesColor = (255,0,0)
        self.gazeColor = (0,255,0)


    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
#        self.window.mainloop()

    def get_frame(self):
        gazeLen = self.width / 5
        if self.vid.isOpened():
            ret, frame = self.vid.read()

            if ret:
                #Return a boolean success flag and the current frame converted to BGRi
                #mirror
                frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                reye = self.gazeinfo["reye"]
                leye = self.gazeinfo["leye"]
                gaze = self.gazeinfo["gaze"]
                cv2.circle(frame, (int(reye[0]), int(reye[1])), 15, self.eyesColor, thickness=2)
                cv2.circle(frame, (int(leye[0]), int(leye[1])), 15, self.eyesColor, thickness=2)
                center = ((reye[0]+leye[0])/2, (reye[1]+leye[1])/2)
                gazeTop = (center[0] + gazeLen * math.sin(math.radians(gaze[0])), center[1] + gazeLen * math.sin(math.radians(gaze[1])))
                cv2.arrowedLine(frame, (int(center[0]), int(center[1])), (int(gazeTop[0]), int(gazeTop[1])), self.gazeColor, thickness=2)
                frame = frame[:,::-1]
                return(ret, frame)
            else:
                return(ret,None)
        else:
            return(ret,None)

    def get_gaze(self) -> dict:
        ret,frame = self.vid.read()
        if not ret:
            return self.gazeinfo_default
        size = (int(self.width*self.red_r), int(self.height*self.red_r))
        #frame = frame[:,::-1]
        #frame = cv2.resize(frame,dsize=None,fx=self.red_r,fy=self.red_r)
        tmp = GazeEstimate.estimateGaze(frame)
        if len(tmp) >= 1:
            self.gazeinfo = tmp[0]
        #self.gazeinfo = GazeEstimate.estimateGaze(frame)[0]

        #reye = [x/self.red_r for x in self.gazeinfo["reye"]]
        #leye = [x/self.red_r for x in self.gazeinfo["leye"]]
        reye = self.gazeinfo["reye"]
        leye = self.gazeinfo["leye"]
        gaze = self.gazeinfo["gaze"]
        gazeLen=self.width/5
        center = ((reye[0]+leye[0])/2, (reye[1]+leye[1])/2)
        gazeTop = (center[0] + gazeLen * math.sin(math.radians(gaze[0])), center[1] + gazeLen * math.sin(math.radians(gaze[1])))
        return(gazeTop[0]/self.width,gazeTop[1]/self.height)

