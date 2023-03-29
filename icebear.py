import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import serial

import tkinter as tk
from tkinter import ttk

ser = serial.Serial('COM6',115200)

LARGE_FONT=("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a=f.add_subplot(111)
f1 = Figure(figsize=(5,5), dpi=100)
a1=f1.add_subplot(111)

count1=[]
knee=[]
count2=[]
hip=[]
##def animateData():
##    ser.reset_output_buffer()
##    ser.reset_input_buffer()
##    while True:
##        data = ser.readline()
##        data = data.strip()
##        data = str(data)
##        data= data[2:-1]
##        data = list(map(str.strip, data.split(',')))
##
##        print(data)


def animateKnee(i):
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    data = ser.readline()
    data = data.strip()
    data = str(data)
    data= data[2:-1]
    data = list(map(str.strip, data.split(',')))

    knee.append(float(data[0]))
    count1.append(i)
    i+=1

    
##    pullData=open("SampleData.txt", "r").read()
##    dataList = pullData.split('\n')
##    xList = []
##    yList = []
##    for eachLine in dataList:
##        if len(eachLine)>1:
##            x,y = eachLine.split(',')
##            xList.append(int(x))
##            yList.append(int(y))
    a.clear()
    a.plot(count1,knee)

def animateHip(i1):
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    data = ser.readline()
    data = data.strip()
    data = str(data)
    data= data[2:-1]
    data = list(map(str.strip, data.split(',')))

    hip.append(float(data[2]))
    count2.append(i1)
    i1+=1
    
##    pullData=open("SampleData.txt", "r").read()
##    dataList = pullData.split('\n')
##    xList = []
##    yList = []
##    for eachLine in dataList:
##        if len(eachLine)>1:
##            x,y = eachLine.split(',')
##            xList.append(int(x))
##            yList.append(int(y))
    a1.clear()
    a1.plot(count1,knee)
            

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
        label = ttk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="One", command=lambda:controller.show_frame(PageOne))
        button1.pack()
        button2 = ttk.Button(self, text="Two", command=lambda:controller.show_frame(PageTwo))
        button2.pack()
        button3 = ttk.Button(self, text="Three", command=lambda:controller.show_frame(PageThree))
        button3.pack()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = ttk.Label(self, text="PageOne", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Home", command=lambda:controller.show_frame(StartPage))
        button1.pack()
class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = ttk.Label(self, text="PageTwo", font=LARGE_FONT)
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
        label = ttk.Label(self, text="PageThree", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Home", command=lambda:controller.show_frame(StartPage))
        button1.pack()



        canvas = FigureCanvasTkAgg(f, self)
        ani=animation.FuncAnimation(f, animateKnee, interval=1000)
        canvas.draw()
        
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
    #def displayKnee(self):
        
        
        
app=cerebral()
#animateData()
#ani1=animation.FuncAnimation(f1, animateHip, interval=1000)
app.mainloop()
