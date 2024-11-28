# Python code transmits a byte to Arduino /Microcontroller
import serial
import time
SerialObj = serial.Serial('/dev/cu.usbmodem1101') 
SerialObj.baudrate = 9600
SerialObj.bytesize = 8
SerialObj.parity  ='N'
SerialObj.stopbits = 1
time.sleep(3)
SerialObj.print(1)
time.sleep(3)
SerialObj.print(0)
SerialObj.close()