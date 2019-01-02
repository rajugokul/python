import RPi.GPIO as GPIO
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

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
print "Distance measurement in progress"
def move():
       a = GPIO.input(PIR)
       #print("pir value : ")
       print(a)
       if a==1:
          print("Movement occurs")


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
        print "Distance:",distance - 0.5,"cm"  #Print distance with 0.5 cm calibration
      else:
        print "Out Of Range"                   #display out of range
def sound():
       if GPIO.input(pin) == GPIO.LOW:
         print pin
         print " sound detected!!"

def acc():
       values = mcp.read_adc(1)
       print("position:",values)
     
       time.sleep(0.5)
    
while True:
    # print "sound:",b,"Distance:",distance - 0.5,"cm","pir",a
     
     move()
     sound()
     acc()
     dis()
  
