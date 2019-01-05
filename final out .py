import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from picamera import PiCamera
camera = PiCamera()
import serial
import pyttsx
from time import sleep
import RPi.GPIO as GPIO
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
engine = pyttsx.init()
ser = serial.Serial("/dev/ttyS0", 9600,timeout=.5)

img_counter = 0
count=0


#GPIO SETUP
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp  = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
pin = 19
TRIG = 20                                #Associate pin 23 to TRIG
ECHO = 21
PIR  = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN)
GPIO.setwarnings(False)
GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHO,GPIO.IN)                   #Set pin as GPIO in
GPIO.setup(PIR,GPIO.IN)
b=0
distance=0
a=0

def my_function():
        print("sending mail....")
        email_user = '1croreprojects.eceteam@gmail.com '
        email_password = 'dlk12345'
        email_send = 'rajugokul1996@gmail.com'

        subject = 'subject'

        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject

        body = 'Hi there, sending this email from Python!'
        msg.attach(MIMEText(body,'plain'))
        data='/home/pi/Desktop/Python-Email-master'
        filename=os.path.join(data,img_name)
        
        attachment  =open(filename,'rb')

        part = MIMEBase('application','octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',"attachment; filename= "+filename)

        msg.attach(part)
        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(email_user,email_password)


        server.sendmail(email_user,email_send,text)
        server.quit()
        print("mail sended")

def move():
       a = GPIO.input(PIR)
       #print("pir value : ")
       print(a)
       if a==1:
          print("Movement occurs")
          ser.write('M1\r\n')
       else:
          ser.write('M0*\r\n')

def dis():
      GPIO.output(TRIG, False)                 #Set TRIG as LOW
      #print "Waitng For Sensor To Settle"
      time.sleep(1)                            #Delay of 2 seconds
      
      GPIO.output(TRIG, True)                  #Set TRIG as HIGH
      time.sleep(0.00001)                      #Delay of 0.00001 seconds
      GPIO.output(TRIG, False)                 #Set TRIG as LOW

      while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
        pulse_start = time.time()              #Saves the last known time of LOW pulse

      while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
        pulse_end = time.time()                #Saves the last known time of HIGH pulse 

      pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

      distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
      distance = round(distance, 2)            #Round to two decimal points

      if distance > 2 and distance < 400:      #Check whether the distance is within range
        print "Distance:",distance - 0.5,"cm"
        ser.write('U'+str(distance - 0.5))
      else:
        print "Out Of Range"                   #display out of range
def sound():
       if GPIO.input(pin) == GPIO.LOW:
         print pin
         print " sound detected!!"
         ser.write('S1')
       else:
         ser.write('S0')

def acc():
       values1 = mcp.read_adc(0)
       values2 = mcp.read_adc(1)
       values3 = mcp.read_adc(2)
       print("position_x:",values1)
       print("position_y:",values2)
       print("position_z:",values3)
       ser.write('A'+str(values1))
       time.sleep(0.5)
       ser.write('B'+str(values2))
       time.sleep(0.5)
       ser.write('C'+str(values3))
       time.sleep(0.5)
def rec():
       incoming = ser.readline().strip()
       print 'Received Data : '+ incoming
       engine.say(' '+incoming)
       engine.runAndWait()

while True:
        img_counter += 1
        print(img_counter)
        img_name = "opencv_frame_{}.png".format(img_counter)
        camera.capture(img_name)
        print("{} written!".format(img_name))
        #my_function()
        #rec()
        ser.write('$')
        sound()
        dis()
        acc()
        move()
       
        
            


