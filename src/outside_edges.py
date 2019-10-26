import os, sys, time
import tkinter as tk



# メインウィンドウ作成
root = tk.Tk()

#メインウィンドウのタイトルを変更
root.title("Oekaki Hack")

#メインウィンドウを1280x720にする
root.geometry("1280x720")


#メインウィンドウ全体をキャンバスにする
canvas = tk.Canvas(root,width = 1280, height = 720)

#キャンバスの位置を指定
canvas.place(x=0,y=0)

#カメラ用の部分（左上）を塗りつぶし（目印）
canvas.create_rectangle(200, 100, 420, 280, fill = 'green', stipple = 'gray25')


#お絵かき用の部分（右下）を塗りつぶし（目印）
canvas.create_rectangle(500, 300, 900, 600, fill = 'blue', stipple = 'gray25')


root.mainloop()