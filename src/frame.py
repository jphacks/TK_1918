import os, sys, time
import tkinter as tk
import cv2
from PIL import Image,ImageTk
import numpy as np
import math
import json
import base64
import requests
import threading
import queue


## Frame ######################################################################
# メインウィンドウ作成
root = tk.Tk()

#メインウィンドウのタイトルを変更
root.title("Oekaki Hack")

#メインウィンドウを1280x720にする
root.geometry("1280x720")


#カメラ映像用のキャンバス（左上）
canvas = tk.Canvas(root,width = 420, height = 280)
canvas.pack()

#キャンバスの位置を指定
canvas.place(x=0,y=0)


#お絵かき用のキャンバス（右下）
canvas2 = tk.Canvas(root,width = 600, height = 400)

#キャンバスの位置を指定
canvas2.place(x=570,y=330)
###############################################################################


## インカメ表示部分 #############################################################
def capStart():
    print('camera-ON')
    try:
        global c, w, h, img
        c=cv2.VideoCapture(0)
        w, h= c.get(cv2.CAP_PROP_FRAME_WIDTH), c.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print('w:'+str(w)+'px+h:'+str(h)+'px')
    except:
        import sys
        print("error-----")
        print(sys.exec_info()[0])
        print(sys.exec_info()[1])
###############################################################################


## キャプチャを繰り返し表示 #######################################################
def u():#update
    global img
    ret, frame =c.read()
    if ret:
        img=ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        canvas.create_image(210,140,image=img)
    else:
        print("u-Fail")
    root.after(1,u)

capStart()
u()

root.mainloop()