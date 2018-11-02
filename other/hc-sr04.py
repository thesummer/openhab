import json
import sys
import time
import requests
import pigpio
import threading

DEVICE = 0x76 # Default device I2C address
IP = "192.168.178.24"        # The IP of the machine hosting your influxdb instance
DB = "iot"               # The database to write to, has to exist
USER = "openhab"             # The influxdb user to authenticate with
PASSWORD = "qwertz123"  # The password of that user
TIME = 1                  # Delay in seconds between two consecutive updates
STATUS_MOD = 5 

callBackEvent = threading.Event()
startTime = 0.0
stopTime = 0.0

def cbf(gpio, level, tick):
    global callBackEvent
    global startTime
    global stopTime
    print(gpio, level, tick)
    if level == 1: # Rising edge
        startTime = tick
    elif level == 0:
        stopTime = tick
        callBackEvent.set()
    
    


def main():
    
    global callBackEvent
    pi = pigpio.pi()
    pi.set_mode(20, pigpio.OUTPUT)
    pi.set_mode(21, pigpio.INPUT)
    cb = pi.callback(21, pigpio.EITHER_EDGE, cbf)
    
    callBackEvent.clear()
    pi.write(20, 1)
    time.sleep(0.00001)
    pi.write(20, 0)
    
    if callBackEvent.wait(0.5):
        water_level = abs(startTime - stopTime) / 10000.0 * 343.5
        print(water_level)
        #v = 'water_level value=%s' % water_level
        #r = requests.post("http://%s:8086/write?db=%s" %(IP, DB), auth=(USER, PASSWORD), data=v)
        #if r.status_code != 204:
        #print '[ERROR] Failed to add temperature to influxdb (%d)' %r.status_code
        
    
        #time.sleep(5*60)
 
  
if __name__=="__main__":
   main()
