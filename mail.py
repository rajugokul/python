import time
from imapclient import IMAPClient

HOSTNAME = 'imap.gmail.com'
MAILBOX = 'Inbox'
MAIL_CHECK_FREQ = 10        # check mail every 60 seconds

# The following three variables must be customized for this
# script to work
USERNAME = 'dhineshrajan1896@gmail.com'
PASSWORD = 'dhineshrajan1896@'
NEWMAIL_OFFSET = 1          # my unread messages never goes to zero, use this to override

door=16
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(door,GPIO.OUT)
GPIO.output(door,GPIO.LOW)

def mail_check():
    # login to mailserver
    server = IMAPClient(HOSTNAME, use_uid=True, ssl=True)
    server.login(USERNAME, PASSWORD)

    # select our MAILBOX and looked for unread messages
    unseen = server.folder_status(MAILBOX, ['UNSEEN'])

    # number of unread messages
    # print to console to determine NEWMAIL_OFFSET
    newmail_count = (unseen[b'UNSEEN'])
    #print('%d unseen messages' % newmail_count)

    if newmail_count > NEWMAIL_OFFSET:
        global NEWMAIL_OFFSET
        NEWMAIL_OFFSET=newmail_count
        GPIO.output(door,GPIO.HIGH)
    else:
        GPIO.output(door,GPIO.LOW)

    time.sleep(MAIL_CHECK_FREQ)

while True:
    mail_check()
