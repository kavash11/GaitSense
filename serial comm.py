import serial
import numpy as np
import csv
import time
import matplotlib.pyplot as plt
import datetime

def main():
    serial_port='COM10'
    baud_rate = 115200
    ser = serial.Serial(serial_port, baud_rate)

    #time_formatted = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    #filename = time_formatted # + extra argument

    ser.reset_output_buffer()
    ser.reset_input_buffer()
    
    knee=[]
    hip=[]
    toe=[]

    t0 = time.time()

    while True:
        data = ser.readline()
        #data = data.decode("utf-8")
        
        data = data.strip()
        data = str(data)
        data= data[2:-1]
        data = list(map(str.strip, data.split(',')))
        knee.append[float(data[0])] #CAUSING ERROR
        #data=data.split(",")
        #print(data.split(","))
        #knee.append(data[0])
        #pp.plot(time,knee, label = 'Knee Flexion')
        #pp.xlabel('Time')
        #pp.ylabel('Angle')
        #pp.title('Knee Flexion')
        #pp.show()
        print(knee)
    ser.close()

main()
