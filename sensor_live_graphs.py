import tkinter as tk
from tkinter import filedialog, Text
from tkinter import *
import os
import serial
import numpy as np
import csv
import time
import matplotlib.pyplot as pp
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import datetime

ser = serial.Serial('COM6',115200) #Not needed for this version of the code since I don't use the serial port
root = tk.Tk()


def getKnee(i):
    #= 
    ser.reset_output_buffer()
    ser.reset_input_buffer()



    t0 = time.time()



    data = ser.readline()


    data = data.strip()
    data = str(data)
    data= data[2:-1]
    data = list(map(str.strip, data.split(',')))
    knee.append(float(data[0])) #Change np.radom.rand with data[0]
    hip.append(float(data[1])) #Change np.radom.rand with data[1]
    toe.append(float(data[2])) #Change np.radom.rand with data[2]
    heel.append(float(data[3])) #Change np.radom.rand with data[3]

    count1.append(i)
    count2.append(i)
    count3.append(i)
    count4.append(i)
    print (count4, heel) #Delete this eventually
    i+=1

    line1.set_data(count1, knee) #Set each individual line with the appropriate data
    line2.set_data(count2, hip)
    line3.set_data(count3, toe)
    line4.set_data(count4, heel)



    #line3.set_data(count, toe)
    #line4.set_data(count, heel)

    print("got here3")
    ax[0][0].relim() #Resize the viewing box
    ax[0][0].autoscale_view()
    ax[0][1].relim()
    ax[0][1].autoscale_view()
    ax[1][0].relim()
    ax[1][0].autoscale_view()
    ax[1][1].relim()
    ax[1][1].autoscale_view()



#def graph(func):
#    plotanimation1 = animation.FuncAnimation(fig, func, interval=100)
#    pp.show()





fig, ax=pp.subplots(2,2)

#Set the plot equal to the first subplot
pp.subplot(2,2,1)
line1 = pp.plot((0),(0),c='black')[0]

#Set the plot equal to the second subplot
pp.subplot(2,2,2)
line2 = pp.plot((0),(0),c='black')[0]

#Set the plot equal to the third subplot
pp.subplot(2,2,3)
line3 = pp.plot((0),(0),c='black')[0]

#Set the plot equal to the fourth subplot
pp.subplot(2,2,4)
line4 = pp.plot((0),(0),c='black')[0]


knee = []
hip = []
toe = []
heel = []

count1 = []
count2 = []
count3 = []
count4 = []

#Plot the graph with subplots
plotanimation1 = animation.FuncAnimation(fig, getKnee, interval=100)
pp.show()
canvas = FigureCanvasTkAgg(plotanimation1, master=root)
canvas.get_tk_widget().pack()
frame = tk.Frame(root)
frame.pack()
root.mainloop()
##def main():
# root = tk.Tk()
#  root.geometry("400x200")
##
##  button3 = Button(root, text='Toe Pressure', command=graph(getToe)) #buttons raen't working, graphs both sensors on same line on same plot
##  button3.pack()
##  button4 = Button(root, text='Heel Pressure', command=graph(getHeel))
##  button4.pack()
##  root.mainloop()
##main()
