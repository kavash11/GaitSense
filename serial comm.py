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
    
    data_array = []
    time_array = []

    t0 = time.time()

    while True:
        data = ser.readline()
        #data = data.decode("utf-8")
        data = data.strip()
        print(data)
    ser.close()

main()
