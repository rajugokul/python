# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

import Adafruit_DHT
sensor = Adafruit_DHT.DHT22
# Software SPI configuration:

#database.................................
import urllib2
import threading

CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp  = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
pin  = 26
count=0
# Hardware SPI configuration:
# SPI_PORT   = 0
# SPI_DEVICE = 0
# mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
#print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
#print('-' * 57)
# Main program loop.

while True:

     #values = [0]*1
     #for i in range(1):
        # The read_adc function will get the value of the specified channel (0-7).
     values = mcp.read_adc(1)
     print(values)
    # Print the ADC values.
     #print('heart beat :{0:>4} '.format(*values))
    # Pause for half a second.
     time.sleep(0.5)
     count=1
     while(count == 1):
          humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
          count=0  
          if humidity is not None and temperature is not None:
           print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
          else:
           print('Failed to get reading. Try again!')
     print("--------------------------------------------------------")
     #print(values,temperature,humidity
     threading.Timer(600,1).start()
     print("Sensing...")
     temp= "%.1f" %temperature
     hum ="%.1f" %humidity
     val = "%.1f"%values
     urllib2.urlopen("http://www.1croreads.com/hospital-iot/hms/get.php?&s1="+val+"&s2="+temp+"&s3="+hum).read()
        

