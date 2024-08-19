import time
from machine import I2C, Pin
from I2C_LCD import I2CLcd

i2c = I2C(0, sda=Pin(12), scl=Pin(13), freq=400000)
#GPIO26 GPIO27
#i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
devices = i2c.scan()

try:
    if devices != []:
        lcd = I2CLcd(i2c, devices[0], 2, 16)
        lcd.move_to(0, 0)
        lcd.putstr("Bodyguard Master")
        count = 0
        while True:
            lcd.move_to(0, 1)
            lcd.putstr("Counter:%d" %(count))
            time.sleep(1)
            count += 1
    else:
        print("No address found")
except:
    pass
