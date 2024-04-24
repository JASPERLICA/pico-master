from machine import Pin, I2C
import utime as time
from dht import DHT11 #, InvalidChecksum

while True:
    time.sleep(1)
    pin = Pin(19, Pin.OUT, Pin.PULL_DOWN) 
    sensor = DHT11(pin)
    try:
        t  = (sensor.temperature)
        h = (sensor.humidity)
    except:
        continue
    print("Temperature: {}".format(sensor.temperature))
    print("Humidity: {}".format(sensor.humidity))