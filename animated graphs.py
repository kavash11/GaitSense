
import serial
import numpy as np
import csv
import time
import matplotlib.pyplot as pp
import matplotlib.animation as animation
import datetime

ser = serial.Serial('COM6',115200)


def getKnee(i):
    
    ser.reset_output_buffer()
    ser.reset_input_buffer()

    t0 = time.time()

    data = ser.readline()

    data = data.strip()
    data = str(data)
    data= data[2:-1]
    data = list(map(str.strip, data.split(',')))
    knee.append(float(data[0]))
    
    count.append(i)
    print (count, knee)
    
    line1.set_data(count, knee)

    #line3.set_data(count, toe)
    #line4.set_data(count, heel)
    
    print("got here3")
    ax1.relim()
    ax1.autoscale_view()
    i +=1


def getHip(i1):
    #ser = serial.Serial('COM6',115200)
    ser.reset_output_buffer()
    ser.reset_input_buffer()

    t0 = time.time()

    data = ser.readline()

    data = data.strip()
    data = str(data)
    data= data[2:-1]
    data = list(map(str.strip, data.split(',')))

    hip.append(float(data[1]))

    
    count.append(i1)
    print (count, hip)
    
    line2.set_data(count, hip)

    #line3.set_data(count, toe)
    #line4.set_data(count, heel)
    
    print("got here3")
    ax2.relim()
    ax2.autoscale_view()
    i1 +=1


def getToe(i2):
    #ser = serial.Serial('COM6',115200)
    ser.reset_output_buffer()
    ser.reset_input_buffer()

    t0 = time.time()

    data = ser.readline()

    data = data.strip()
    data = str(data)
    data= data[2:-1]
    data = list(map(str.strip, data.split(',')))
    knee.append(float(data[0]))
    hip.append(float(data[1]))
    toe.append(float(data[2]))
       # heel.append(float(data[3]))
    
    count.append(i2)
    print (count, toe)
    
    line3.set_data(count, toe)

    #line3.set_data(count, toe)
    #line4.set_data(count, heel)
    
    print("got here3")
    ax3.relim()
    ax3.autoscale_view()
    i2 +=1


def getHeel(i3):
    #ser = serial.Serial('COM6',115200)
    ser.reset_output_buffer()
    ser.reset_input_buffer()

    t0 = time.time()

    data = ser.readline()

    data = data.strip()
    data = str(data)
    data= data[2:-1]
    data = list(map(str.strip, data.split(',')))
    knee.append(float(data[0]))
    hip.append(float(data[1]))
    toe.append(float(data[2]))
    heel.append(float(data[3]))
    
    count.append(i3)
    print (count, heel)
    
    line4.set_data(count, heel)

    #line3.set_data(count, toe)
    #line4.set_data(count, heel)
    
    print("got here3")
    ax4.relim()
    ax4.autoscale_view()
    i3 +=1


##def graph(func):  
##    plotanimation1 = animation.FuncAnimation(fig, func, interval=100)
##    pp.show()
##
##
knee = []
hip = []
toe = []
heel = []
i = 0
i1=0
i2=0
i3=0
count = []
fig, ((ax1, ax2), (ax3, ax4)) =pp.subplots(2,2)
line1 = ax1.plot((0),(0),c='black')[0]
#fig, ax2=pp.subplots()
line2 = ax2.plot((0),(0),c='black')[0]
#fig, ax3=pp.subplots()
line3 = ax3.plot((0),(0),c='black')[0]
#fig, ax4=pp.subplots()
line4 = ax4.plot((0),(0),c='black')[0]


plotanimation1 = animation.FuncAnimation(fig, getKnee, interval=100)
plotanimation2 = animation.FuncAnimation(fig, getHip, interval=100)
plotanimation3 = animation.FuncAnimation(fig, getToe, interval=100)
plotanimation4 = animation.FuncAnimation(fig, getHeel, interval=100)
pp.show()
##def main():
##    root = tk.Tk()
##    root.geometry("400x200")
##
##    button3 = Button(root, text='Toe Pressure', command=graph(getToe)) #buttons raen't working, graphs both sensors on same line on same plot
##    button3.pack()
##    button4 = Button(root, text='Heel Pressure', command=graph(getHeel))
##    button4.pack()
##    
##main()
