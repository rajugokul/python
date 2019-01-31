import os, time
from pyfingerprint.pyfingerprint import PyFingerprint
import serial
import RPi.GPIO as gpio
import datetime
from espeak import espeak
import picamera
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from email.mime.image import MIMEImage



# password
password = "4567"
length = len(password)


fromaddr = "dhineshrajan1896@gmail.com"
toaddr = "dhineshtnr1896@gmail.com"
mail = MIMEMultipart()

mail['From'] = fromaddr
mail['To'] = toaddr
mail['Subject'] = "Attachment"
body = "Please find the attachment"

RS =18
EN =23
D4 =24
D5 =25
D6 =8
D7 =7

enrol=5
delet=6
inc=13
dec=19
led=26

motor=17

HIGH=1
LOW=0
ir=2

COL = [11,9,10,22]
ROW = [21, 20, 16, 12]

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(RS, gpio.OUT)
gpio.setup(EN, gpio.OUT)
gpio.setup(D4, gpio.OUT)
gpio.setup(D5, gpio.OUT)
gpio.setup(D6, gpio.OUT)
gpio.setup(D7, gpio.OUT)
gpio.setup(motor, gpio.OUT)
gpio.setup(ir, gpio.IN)

gpio.setup(enrol, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(delet, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(inc, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(dec, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(led, gpio.OUT)
gpio.output(motor, LOW)

for j in range(4):
    gpio.setup(COL[j], gpio.OUT)
    gpio.output(COL[j], 1)

for i in range(4):
    gpio.setup(ROW[i], gpio.IN, pull_up_down = gpio.PUD_UP)

#try:
f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

if ( f.verifyPassword() == False ):
    raise ValueError('The given fingerprint sensor password is wrong!')

#except Exception as e:
 #   print('Exception message: ' + str(e))
    #exit(1)

def check_keypad(length):

    COL = [11,9,10,22]
    ROW = [21, 20, 16, 12]

    MATRIX = [
        ["1", "2", "3", "A"],
        ["4", "5", "6", "B"],
        ["7", "8", "9", "C"],
        ["*", "0", "#", "D"]
]
    result = ""
    while(True):
        for j in range(4):
            gpio.output(COL[j], 0)

            for i in range(4):
                if gpio.input(ROW[i]) == 0:
                    time.sleep(0.02)
                    result = result + MATRIX[i][j]
                    while(gpio.input(ROW[i]) == 0):
                          time.sleep(0.02)

            gpio.output(COL[j], 1)
            if len(result) >= length:
                return result

 
def begin():
  lcdcmd(0x33) 
  lcdcmd(0x32) 
  lcdcmd(0x06)
  lcdcmd(0x0C) 
  lcdcmd(0x28) 
  lcdcmd(0x01) 
  time.sleep(0.0005)
 
def lcdcmd(ch): 
  gpio.output(RS, 0)
  gpio.output(D4, 0)
  gpio.output(D5, 0)
  gpio.output(D6, 0)
  gpio.output(D7, 0)
  if ch&0x10==0x10:
    gpio.output(D4, 1)
  if ch&0x20==0x20:
    gpio.output(D5, 1)
  if ch&0x40==0x40:
    gpio.output(D6, 1)
  if ch&0x80==0x80:
    gpio.output(D7, 1)
  gpio.output(EN, 1)
  time.sleep(0.005)
  gpio.output(EN, 0)
  # Low bits
  gpio.output(D4, 0)
  gpio.output(D5, 0)
  gpio.output(D6, 0)
  gpio.output(D7, 0)
  if ch&0x01==0x01:
    gpio.output(D4, 1)
  if ch&0x02==0x02:
    gpio.output(D5, 1)
  if ch&0x04==0x04:
    gpio.output(D6, 1)
  if ch&0x08==0x08:
    gpio.output(D7, 1)
  gpio.output(EN, 1)
  time.sleep(0.005)
  gpio.output(EN, 0)
  
def lcdwrite(ch): 
  gpio.output(RS, 1)
  gpio.output(D4, 0)
  gpio.output(D5, 0)
  gpio.output(D6, 0)
  gpio.output(D7, 0)
  if ch&0x10==0x10:
    gpio.output(D4, 1)
  if ch&0x20==0x20:
    gpio.output(D5, 1)
  if ch&0x40==0x40:
    gpio.output(D6, 1)
  if ch&0x80==0x80:
    gpio.output(D7, 1)
  gpio.output(EN, 1)
  time.sleep(0.005)
  gpio.output(EN, 0)
  # Low bits
  gpio.output(D4, 0)
  gpio.output(D5, 0)
  gpio.output(D6, 0)
  gpio.output(D7, 0)
  if ch&0x01==0x01:
    gpio.output(D4, 1)
  if ch&0x02==0x02:
    gpio.output(D5, 1)
  if ch&0x04==0x04:
    gpio.output(D6, 1)
  if ch&0x08==0x08:
    gpio.output(D7, 1)
  gpio.output(EN, 1)
  time.sleep(0.005)
  gpio.output(EN, 0)
def lcdclear():
  lcdcmd(0x01)
 
def lcdprint(Str):
  l=0;
  l=len(Str)
  for i in range(l):
    lcdwrite(ord(Str[i]))
    
def setCursor(x,y):
    if y == 0:
        n=128+x
    elif y == 1:
        n=192+x
    lcdcmd(n)
def sendMail(data):
    mail.attach(MIMEText(body, 'plain'))
    print data
    dat='%s.jpg'%data
    print dat
    attachment = open(dat, 'rb')
    image=MIMEImage(attachment.read())
    attachment.close()
    mail.attach(image)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "dhineshrajan1896@")
    text = mail.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def capture_image():
    data= time.strftime("%d_%b_%Y|%H:%M:%S")
    camera.start_preview()
    time.sleep(5)
    print data
    camera.capture('%s.jpg'%data)
    camera.stop_preview()
    time.sleep(1)
    sendMail(data)
    
def enrollFinger():
    lcdcmd(1)
    lcdprint("Enrolling Finger")
    time.sleep(2)
    print('Waiting for finger...')
    lcdcmd(1)
    lcdprint("Place Finger")
    while ( f.readImage() == False ):
        pass
    f.convertImage(0x01)
    result = f.searchTemplate()
    positionNumber = result[0]
    if ( positionNumber >= 0 ):
        print('Template already exists at position #' + str(positionNumber))
        lcdcmd(1)
        lcdprint("Finger ALready")
        lcdcmd(192)
        lcdprint("   Exists     ")
        time.sleep(2)
        return
    print('Remove finger...')
    lcdcmd(1)
    lcdprint("Remove Finger")
    time.sleep(2)
    print('Waiting for same finger again...')
    lcdcmd(1)
    lcdprint("Place Finger")
    lcdcmd(192)
    lcdprint("   Again    ")
    while ( f.readImage() == False ):
        pass
    f.convertImage(0x02)
    if ( f.compareCharacteristics() == 0 ):
        print "Fingers do not match"
        lcdcmd(1)
        lcdprint("Finger Did not")
        lcdcmd(192)
        lcdprint("   Mactched   ")
        time.sleep(2)
        return
    f.createTemplate()
    positionNumber = f.storeTemplate()
    print('Finger enrolled successfully!')
    lcdcmd(1)
    lcdprint("Stored at Pos:")
    lcdprint(str(positionNumber))
    lcdcmd(192)
    lcdprint("successfully")
    print('New template position #' + str(positionNumber))
    time.sleep(2)

def searchFinger():
    try:
        print('Waiting for finger...')
        while( f.readImage() == False ):
            #pass
            time.sleep(.5)
            return
        f.convertImage(0x01)
        result = f.searchTemplate()
        positionNumber = result[0]
        accuracyScore = result[1]
        if positionNumber == -1 :
            print('No match found!')
            espeak.synth("please place your finger again")
            lcdcmd(1)
            lcdprint("No Match Found")
            time.sleep(2)
            return
        else:
            print('Found template at position #' + str(positionNumber))
            lcdcmd(1)
            lcdprint("Found at Pos:")
            lcdprint(str(positionNumber))
            time.sleep(2)
            lcdcmd(1)
            lcdprint("enter password")
            espeak.synth("please enter four digit user password")
            result = check_keypad(length)
            if result == password:
              lcdcmd(1)
              lcdprint("welcome")
              gpio.output(motor, HIGH)
              espeak.synth("welcome")
              time.sleep(2)
              gpio.output(motor, LOW)
            else:
              lcdcmd(1)
              lcdprint("wrong password")
              espeak.synth("your password is wrong")


    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)
    
def deleteFinger():
    positionNumber = 0
    count=0
    lcdcmd(1)
    lcdprint("Delete Finger")
    lcdcmd(192)
    lcdprint("Position: ")
    lcdcmd(0xca)
    lcdprint(str(count))
    while gpio.input(enrol) == True:   # here enrol key means ok
        if gpio.input(inc) == False:
            count=count+1
            if count>1000:
                count=1000
            lcdcmd(0xca)
            lcdprint(str(count))
            time.sleep(0.2)
        elif gpio.input(dec) == False:
            count=count-1
            if count<0:
                count=0
            lcdcmd(0xca)
            lcdprint(str(count))
            time.sleep(0.2)
    positionNumber=count
    if f.deleteTemplate(positionNumber) == True :
        print('Template deleted!')
        lcdcmd(1)
        lcdprint("Finger Deleted");
        time.sleep(2)

begin()
lcdcmd(0x01)
lcdprint("  FingerPrint ")
lcdcmd(0xc0)
lcdprint("Based Door lock")
time.sleep(2)
lcdcmd(0x01)
lcdprint("**** Welcome ***")
lcdcmd(0xc0)
lcdprint("****************")
time.sleep(2)
flag=0
lcdclear()
camera = picamera.PiCamera()
camera.rotation=180
camera.awb_mode= 'auto'
camera.brightness=55


while 1:
    t = str(datetime.datetime.now())
    gpio.output(led, HIGH)
    lcdcmd(1)
    lcdprint("Place Finger")
    if gpio.input(ir) == 0:
        print "send email"
        capture_image()
    if gpio.input(enrol) == 0:
        gpio.output(led, LOW)
        enrollFinger()
    elif gpio.input(delet) == 0:
        gpio.output(led, LOW)
        while gpio.input(delet) == 0:
            time.sleep(0.1)
        deleteFinger()
    else:
        searchFinger()
