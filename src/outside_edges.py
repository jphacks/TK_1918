import os, sys, time
import tkinter as tk
from tkinter import *
from tkinter import ttk


# メインウィンドウ作成
root = tk.Tk()

#メインウィンドウのタイトルを変更
root.title("Oekaki Hack")

#メインウィンドウを1280x720にする
root.geometry("1280x720")

#フレーム（カメラの映像映す用）を左上に描画
frame1 = ttk.Frame(
    root,
    height=200,
    width=300,
    relief='ridge',
    borderwidth=5)
frame1.place(x=150,y=100)

#フレーム（画像の描画用）を右下に描画
frame2 = ttk.Frame(
    root,
    height=400,
    width=600,
    relief='ridge',
    borderwidth=5)
frame2.place(x=530,y=220)

root.mainloop()