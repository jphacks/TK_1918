import os, sys, time
import tkinter as tk



# メインウィンドウ作成
root = tk.Tk()

#メインウィンドウのタイトルを変更
root.title("Oekaki Hack")

#メインウィンドウを1280x720にする
root.geometry("1280x720")


#カメラ映像用のキャンバス（左上）
canvas = tk.Canvas(root,width = 420, height = 280)

#キャンバスの位置を指定
canvas.place(x=0,y=0)


#お絵かき用のキャンバス（右下）
canvas2 = tk.Canvas(root,width = 600, height = 400)

#キャンバスの位置を指定
canvas2.place(x=570,y=330)


root.mainloop()