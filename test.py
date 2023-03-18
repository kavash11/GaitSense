import tkinter as tk
from tkinter import filedialog, Text
from tkinter import *
import os
import matplotlib.pyplot as pp
import numpy as np

root = tk.Tk()

root.geometry("400x200")

data = np.loadtxt(fname='test.txt', delimiter=',')
#print(data)
knee=[]
hip=[]
toe=[]

for i in range (len(data)):
    for j in range(3):
        if j==0:
            knee.append(data[i][j])
        elif j == 1:
            hip.append(data[i][j])
        else:
            toe.append(data[i][j])

time =[]
for i in range (len(knee)):
    time.append(i)
    

def graph1():
    pp.plot(time,knee, label = 'Knee Flexion')
    pp.xlabel('Time')
    pp.ylabel('Angle')
    pp.title('Knee Flexion')
    pp.show()

button1 = Button(root, text='Knee Flexion', command=graph1)
button1.pack()

def graph2():
    pp.plot(time,hip, label = 'Hip Flexion')
    pp.xlabel('Time')
    pp.ylabel('Angle')
    pp.title('Hip Flexion')
    pp.show()

button2 = Button(root, text='Hip Flexion', command=graph2)
button2.pack()

def graph3():
    pp.plot(time,toe, label = 'Toe Pressure')
    pp.xlabel('Time')
    pp.ylabel('Volts')
    pp.title('Toe Pressure')
    pp.show()

button3 = Button(root, text='Toe Pressure', command=graph3)
button3.pack()


root.mainloop()
