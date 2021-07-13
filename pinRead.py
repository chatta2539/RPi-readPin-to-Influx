import RPi.GPIO as GPIO 
import time
from influxdb import InfluxDBClient
import random
from gpiozero import CPUTemperature

GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)
cpu = CPUTemperature()
DRM1 = 13
DRM2 = 19
DRM3 = 26
GPIO.setup(DRM1, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(DRM2, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(DRM3, GPIO.IN, GPIO.PUD_DOWN)

dbClient = InfluxDBClient(host='127.0.0.1', port=8086, database='testDemand')
previous_time = time.time() 

def mainFunction():
    result = [{"measurement": "testDRM",

        "tags": 
            {
            # "unit": xiaomiTemp.units
            },
        "fields":
            {
                "DRM1": GPIO.input(DRM1),
                "DRM2": GPIO.input(DRM2),
                "DRM3": GPIO.input(DRM3),
                "cpu_Temp": cpu.temperature
            }
        }]
    
    dbClient.write_points(result)
    print(result)
    
while True:
    time.sleep(0.1)
    if time.time()-previous_time >= 1:
        mainFunction()
        previous_time = time.time()
        
GPIO.cleanup()
