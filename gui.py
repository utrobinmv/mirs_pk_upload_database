# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 16:05:59 2020

@author: utrobinmv
"""

# from tkinter import *
import tkinter
from PIL import Image, ImageTk 

from database import db_connect, db_init, db_disconnect

connect = db_connect()

cursor = connect.cursor()

clicks = 0  


def click_button():
    global clicks
    global image
    global photo

    clicks += 1
    window.title("Clicks !!! {}".format(clicks))

    # canvas = tkinter.Canvas(window, height=200, width=200)
    image = Image.open("data/Screenshot_2020-09-13_01-28-54.png")
    photo = ImageTk.PhotoImage(image)
    image = canvas.create_image(1, 2, anchor='nw',image=photo)
    canvas.pack()


def on_select(event):
    global clicks
    clicks += 1
    FROM=lb
    selectIndexes=list(FROM.curselection())
    value_select = FROM.get(selectIndexes)
    window.title("Clicks {}".format(value_select))

window = tkinter.Tk()  
window.title("Прототип фронт Интерфейса")  
# window.geometry("300x250")
# lbl = Label(window, text="Привет")  
# lbl.grid(column=0, row=0)  




lb = tkinter.Listbox()
# for i in acts:
# lb.insert(tkinter.END, "Элемент 1")
# lb.insert(tkinter.END, "Элемент 2")

command = (f"SELECT attrs_cn FROM objects_rosreestr")
cursor.execute(command)
for row in cursor:
    # print("Select: ", row[0])
    lb.insert(tkinter.END, row[0])

command = (f"SELECT attrs_cn FROM map_update ORDER BY date_check DESC LIMIT 50")
cursor.execute(command)
for row in cursor:
    # print("Select: ", row[0])
    lb.insert(tkinter.END, row[0])


lb.bind("<<ListboxSelect>>", on_select)
           
# lb.grid(row=0,column=0)
lb.pack()

#Добавим изображение
canvas = tkinter.Canvas(window, height=200, width=200)
image = Image.open("data/Screenshot_2020-09-12_16-45-45.png")
photo = ImageTk.PhotoImage(image)
image = canvas.create_image(0, 0, anchor='nw',image=photo)
# canvas.grid(row=0,column=1)
canvas.pack()



btn1 = tkinter.Button(text="Подтвердить", background="#555", foreground="#ccc",
             padx="120", pady="8", font="16", command=click_button)
# btn1.grid(row=0,column=1)
btn1.pack()

btn2 = tkinter.Button(text="Отклонить", background="#555", foreground="#ccc",
             padx="120", pady="8", font="16", command=click_button)
# btn2.grid(row=1,column=1)
btn2.pack()

btn3 = tkinter.Button(text="Забраковать", background="#555", foreground="#ccc",
             padx="120", pady="8", font="16", command=click_button)
# btn3.grid(row=2,column=1)
btn3.pack()




window.mainloop()

cursor.close()

db_disconnect(connect)