import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import cv2

cam = cv2.VideoCapture(0)

cv2.namedWindow("live")

img_counter = 0

def my_function():
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
        data='/home/pi/Desktop/Python-Email-master/'
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



while True:
    ret, frame = cam.read()
    cv2.imshow("live", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
        my_function()

cam.release()

cv2.destroyAllWindows()


