#! usr/bin/env python3

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import numpy as np
import cv2
import glfw
import time

#OpenGL.UNSIGNED_BYTE_IMAGES_AS_STRING = False

#Canvas.get_frameで画像とフレームを返す
#return(ret, frame)

class Canvas:
    def __init__(self,width:int=200,height:int=100)->None:
        self.width:int = int(width/2)
        self.height:int = int(height/2)
        #print(self.width)
        #print(self.height)
        self.ps:list=[[]]
        #self.ps:list=[[(-0.8,-0.8),(0.8,0.8),(0.8,-0.8)],[(0.4,0.4),(0.4,-0.4)]]
        #initialize the library
        if not glfw.init():
            return
        #set sinwod hint NOT visible
        glfw.window_hint(glfw.VISIBLE,False)
        # Create a windowed mode window and its OpenGL context
        self.window = glfw.create_window(self.width, self.height, "hidden window", None, None)
        if not self.window:
            glfw.terminate()
            return

        # Make the window's context current
        glfw.make_context_current(self.window)
        #gluPerspective(90, (self.width / self.height), 0.01, 12)
        #glEnable(GL_TEXTURE_2D)
        #glEnable(GL_DEPTH_TEST)
        #glDepthFunc(GL_LEQUAL)

        #glRotatef(-90, 1, 0, 0) # Straight rotation
        glClearColor(1,1,1,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #glRotatef(285, 0, 0, 1) # Rotate yaw
        #glTranslatef(-5, -3, -2) # Move to position
        #glViewport(0,0,self.width,self.height)
        #glMatrixMode(GL_PROJECTION)
        #glLoadIdentity()
        #glOrtho(-self.width,self.width,-self.height,self.height,0.0,1.0) # this creates a canvas you can do 2D drawing on

    def __del__(self)->None:
        #pass
        glfw.destroy_window(self.window)
        glfw.terminate()

    def write_line(self,p_l:list)->None:
        glBegin(GL_LINES)
        #glLineWidth(3)
        for i,p in enumerate(p_l):
            #q = (self.width * p[0],self.height * p[1])
            q=p
            if i!=0 and i!=len(p_l):
                glVertex(q[0],q[1])
            glVertex(q[0],p[1])
        glEnd()

    def draw(self)->None:
        glClearColor(255/255, 246/255, 201/255, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glColor(45/255,33/255,11/255,0)
        #glBegin(GL_TRIANGLES)
        #glVertex3f(-100, -100,0)
        #glVertex3f(100, -100,0)
        #glVertex3f(0, 100,0)
        #glVertex(-1,-1)
        #glVertex(1,-1)
        #glVertex(0,1)
        #glEnd()
        for l in self.ps:
            self.write_line(l)
        #glFlush()
        #glutSwapBuffers()
        glfw.swap_buffers(self.window)

    #add point
    def add_point(self,x:float,y:float)->None:
        self.ps[-1].append((2*x-1,2*y-1))
        #print(self.ps)

    def get_frame(self)->(bool,any):
        #glutDisplayFunc(self.draw)
        self.draw()
        #self.image_buffer = glReadPixels(0, 0, self.width, self.height, GL_RGB, GL_UNSIGNED_BYTE)
        #self.image = np.frombuffer(self.image_buffer,dtype=np.uint8).reshape(self.height,self.width,3)
        #print(self.img)
        #glutMainLoop()
        #glfw.swap_buffers(self.window)
        glfw.poll_events()
        #time.sleep(5)
        glReadBuffer( GL_FRONT )
        self.image_buffer = glReadPixels(0, 0, 2*self.width, 2*self.height, GL_RGB, GL_UNSIGNED_BYTE)
        self.image = np.frombuffer(self.image_buffer,dtype=np.uint8).reshape(2*self.height,2*self.width,3)
        #self.image = self.image[::-1]
        self.image = cv2.flip(self.image, 1)
        #pil_img = Image.fromarray(self.image)
        #pil_img.save('image.png')
        #print(len(self.image))
        #print(len(self.image[0]))
        return((True,self.image))

if __name__=="__main__":
    cv=Canvas()
    ret, img = cv.get_frame()
    if ret:
        #pixelFormat="RGB"
        #out_img = Image.frombytes(pixelFormat,(cv.width,cv.height),data=img)
        #out_img.save("test.jpg",format="jpeg")
        #print(len(img))
        #print(len(img[0]))
        #print(img.shape)
        cv2.imwrite("image.png", img)
        cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        #pass

