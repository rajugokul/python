import urllib3
import time
http = urllib3.PoolManager(10)

url="http://iot-dhironics.com/pi/light.json"
response = http.request('GET', url)
print(response.data)
f=http.request('GET',"http://iot-dhironics.com/atten/get1.php?id=0")
print(f.data)
