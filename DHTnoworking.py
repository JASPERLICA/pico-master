import time
import adafruit_dht
# import board

from machine import Pin

DHt11pin =  Pin(19, Pin.IN, Pin.PULL_UP)    # GP2 as an INPUT for the photoeye

dht_device = adafruit_dht.DHT11(DHt11pin)

while True:
    try:
        temperature_c = dht_device.temperature
        temperature_f = temperature_c * (9 / 5) + 32

        humidity = dht_device.humidity

        print("Temp:{:.1f} C / {:.1f} F    Humidity: {}%".format(temperature_c, temperature_f, humidity))
    except RuntimeError as err:
        print(err.args[0])

    time.sleep(2.0)