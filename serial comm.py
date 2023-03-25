import serial
import numpy as np
import csv
import time
import matplotlib.pyplot as pp
import matplotlib.animation as animation
import datetime

def getData(hip, knee, heel, toe, ser):
    

    #time_formatted = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    #filename = time_formatted # + extra argument

    ser.reset_output_buffer()
    ser.reset_input_buffer()
    
    #knee=[]


    t0 = time.time()


    data = ser.readline()
        #data = data.decode("utf-8")
        
    data = data.strip()
    data = str(data)
    data= data[2:-1]
    data = list(map(str.strip, data.split(',')))
    knee.append(float(data[0]))
    hip.append(float(data[1]))
    toe.append(float(data[2]))
    heel.append(float(data[3]))
    return(knee, hip, toe, heel)
    
    


def animate(i):
    knee=[]
    hip=[]
    toe=[]
    heel=[]
    fig = pp.figure()
    ax1=fig.add_subplot(1,1,1)
    ser = serial.Serial('COM6',115200)
    while (1):
        knee, hip, toe, heel = getData(knee, hip, toe, heel, ser)
        ax1.plot(knee, hip)
        ani = animation.FuncAnimation(fig, animate, interval=100)
        pp.show()
#ser.close()
animate(i=0)
