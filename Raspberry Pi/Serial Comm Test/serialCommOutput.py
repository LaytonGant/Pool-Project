import serial
import time

ser = serial.Serial("/dev/ttyACM0",9600)
ser.baudrate = 9600
msg = "Hello from Pi!"

while True:
    ser.write(msg.encode("utf-8"))
    time.sleep(3)