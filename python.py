import urllib.request, json
import urllib3
http=urllib3.PoolManager()
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16,GPIO.OUT)
count=0


while True:
    with urllib.request.urlopen("http://iot-dhironics.com/pi/light.json") as url:
        data = json.loads(url.read().decode())
        if data["light"] == "on":
            print(data)
            GPIO.output(16,GPIO.HIGH)
       



