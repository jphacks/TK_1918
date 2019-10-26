#! usr/bin/env python3

from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image
import numpy as np
import cv2
import glfw

#OpenGL.UNSIGNED_BYTE_IMAGES_AS_STRING = False

#Canvas.get_frameで画像とフレームを返す
#return(ret, frame)

class Canvas:
    def __init__(self,width:int=200,height:int=100)->None:
        self.width = width
        self.height = height
        #print(self.width)
        #print(self.height)
        #self.ps:list=[[]]
        self.ps:list=[[(-0.8,-0.8),(0.8,0.8),(0.8,-0.8)],[(0.4,0.4),(0.4,-0.4)]]
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(self.width,self.height)
        glutCreateWindow("PyOpenGL 1")

    def __del__(self)->None:
        #pass
        #glutLeaveMainLoop()
        glutDestroyWindow()

    def write_line(self,p_l:list)->None:
        glBegin(GL_LINES)
        for i,p in enumerate(p_l):
            if i!=0 and i!=len(p_l):
                glVertex(p[0],p[1])
            glVertex(p[0],p[1])
        glEnd()

    def draw(self)->None:
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glColor(0,0,0,0)
        glBegin(GL_TRIANGLES)
        glVertex(-1, -1)
        glVertex(1, -1)
        glVertex(0, 1)
        glEnd()
        for l in self.ps:
            self.write_line(l)
        #glFlush()
        #glutSwapBuffers()

    #add point
    def add_point(self,x:float,y:float)->None:
        self.ps[-1].append((2*x-1,2*y-1))

    def get_frame(self)->(bool,any):
        glutDisplayFunc(self.draw)
        #glReadBuffer(GL_FRONT)
        self.image_buffer = glReadPixels(0, 0, self.width, self.height, GL_RGB, GL_UNSIGNED_BYTE)
        self.image = np.frombuffer(self.image_buffer,dtype=np.uint8).reshape(self.width,self.height,3)
        #print(self.img)
        #glutMainLoop()
        return((True,self.image))

if __name__=="__main__":
    cv=Canvas()
    ret, img = cv.get_frame()
    if ret:
        #pixelFormat="RGB"
        #out_img = Image.frombytes(pixelFormat,(cv.width,cv.height),data=img)
        #out_img.save("test.jpg",format="jpeg")

        cv2.imwrite("image.png", img)

