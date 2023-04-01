import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import serial
import numpy as np

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

ser = serial.Serial('COM10',115200)

LARGE_FONT=("Arial", 12)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a=f.add_subplot(111)
f1 = Figure(figsize=(5,5), dpi=100)
a1=f1.add_subplot(111)
f2 = Figure(figsize=(5,5), dpi=100)
a2=f2.add_subplot(111)

count1=[]
knee=[]
count2=[]
hip=[]
count3=[]
toe=[]
heel=[]


def animateKnee(i):
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    data = ser.readline()
    data = data.strip()
    data = str(data)
    data= data[2:-1]
    data = list(map(str.strip, data.split(',')))

    if (len(data)==4):
        knee.append(float(data[0]))

    else :
        knee.append(0)

    count1.append(i)
    i+=1
    a.clear()
    a.plot(count1,knee)
    a.set_xlim(left=max(0,i-10),right=i+10) #moves axis
    a.set_ylim([0,50])
    a.set_xlabel("Time (s)")
    a.set_ylabel("Angle (Degrees)")
    a.set_title('Knee Flexion')

def animateHip(i1):
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    data = ser.readline()
    data = data.strip()
    data = str(data)
    data= data[2:-1]
    data = list(map(str.strip, data.split(',')))
    if len(data) == 4:    
        hip.append(float(data[1]))
    elif len(data) == 3:
        hip.append(float(data[0]))
    else:
        hip.append(0)
    count2.append(i1)
    i1+=1
    
    a1.clear()
    a1.plot(count2,hip)
    a1.set_xlim(left=max(0,i1-10),right=i1+10)
    a1.set_ylim([0,50])
    a1.set_xlabel("Time (s)")
    a1.set_ylabel("Angle (Degrees)")
    a1.set_title('Hip Flexion')

def foot(i2):
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    data = ser.readline()
    data = data.strip()
    data = str(data)
    data= data[2:-1]
    data = list(map(str.strip, data.split(',')))
    if len(data) == 4:
        toe.append(float(data[2]))
        heel.append(float(data[3]))
    elif len(data) == 3:
        toe.append(float(data[1]))
        heel.append(float(data[2]))
    elif len(data) == 2:
        toe.append(float(data[0]))
        heel.append(float(data[1]))
    count3.append(i2)
    i2+=1
    
    a2.clear()
    a2.plot(count3,toe, label = "Toe")
    a2.plot(count3,heel, label="Heel")
    a2.set_xlim(left=max(0,i2-10),right=i2+10)
    a2.set_ylim([0,5000])
    a2.set_xlabel("Time (s)")
    a2.set_ylabel("Pressure (V)")
    a2.set_title('Foot Pressure')
    a2.legend()

class cerebral(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0,weight=1)
        self.frames= {}
        for F in (StartPage, PageOne, PageTwo, PageThree):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = ttk.Label(self, text="Home", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Foot Pressure", command=lambda:controller.show_frame(PageOne))
        button1.pack()
        button2 = ttk.Button(self, text="Hip Flexion", command=lambda:controller.show_frame(PageTwo))
        button2.pack()
        button3 = ttk.Button(self, text="Knee Flexion", command=lambda:controller.show_frame(PageThree))
        button3.pack()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = ttk.Label(self, text="Foot Pressure", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Home", command=lambda:controller.show_frame(StartPage))
        button1.pack()
        canvas2 = FigureCanvasTkAgg(f2, self)
        ani2=animation.FuncAnimation(f2, foot, interval=1000)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = ttk.Label(self, text="Hip Flexion", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Home", command=lambda:controller.show_frame(StartPage))
        button1.pack()
        canvas1 = FigureCanvasTkAgg(f1, self)
        ani1=animation.FuncAnimation(f1, animateHip, interval=1000)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        
class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = ttk.Label(self, text="Knee Flexion", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Home", command=lambda:controller.show_frame(StartPage))
        button1.pack()

        canvas = FigureCanvasTkAgg(f, self)
        ani=animation.FuncAnimation(f, animateKnee, interval=1000)
        canvas.draw()
        
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        

    
        
app=cerebral()
app.mainloop()
