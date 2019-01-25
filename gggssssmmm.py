import serial
   
import os, time

 
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.5)

while True: 
        port.write('AT+CMGF=1'+'\r\n')  # Select Message format as Text mode 
        time.sleep(2)
         
         
        port.write('AT+CMGS="9788391337"'+'\r\n')
        time.sleep(2)
         
        port.write('mini'+'\r\n')  # Message
        time.sleep(2)
         
        port.write("\x1A") # Enable to send SMS
        time.sleep(2)
