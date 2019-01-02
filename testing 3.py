import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from picamera import PiCamera
from time import sleep
camera = PiCamera()

img_counter = 0
count=0

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


while True:
        img_counter += 1
        print(img_counter)
        img_name = "opencv_frame_{}.png".format(img_counter)
        camera.capture(img_name)
        print("{} written!".format(img_name))
        my_function()      
               


