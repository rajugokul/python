import serial
import pyttsx
from time import sleep
engine = pyttsx.init()
# Enable USB Communication
ser = serial.Serial("/dev/ttyS0", 9600,timeout=.5)
 
while True:
    ser.write('Hello User \r\n')         # write a Data
    incoming = ser.readline().strip()
    print 'Received Data : '+ incoming
    engine.say(' '+incoming)
    engine.runAndWait()
    
    
