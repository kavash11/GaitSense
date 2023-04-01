import serial
ser = serial.Serial('COM10',115200)
while True:
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    data = ser.readline()
    data = data.strip()
    data = str(data)
    data= data[2:-1]
    data = list(map(str.strip, data.split(',')))
    print(data)
