from machine import WDT   #Watch Dog Timer class
from machine import I2C, Pin
from machine import UART
from time import sleep
from I2C_LCD import I2CLcd



Channel0    = machine.Pin(5,machine.Pin.OUT)                       # GP5 as Channel 0 LED panel
Channel1    = machine.Pin(6,machine.Pin.OUT)                       # GP6 as Channel 1 LED panel
Channel2    = machine.Pin(7,machine.Pin.OUT)                       # GP7 as Channel 2 LED panel
Channel3    = machine.Pin(15,machine.Pin.OUT)                      # GP7 as Channel 3 LED panel
RelayNuc    = machine.Pin(4,machine.Pin.OUT)                       # GP7 as Channel 2 LED panel
RelayPoe    = machine.Pin(3,machine.Pin.OUT)                      # GP7 as Channel 3 LED panel
LED		    = machine.Pin(22,machine.Pin.OUT)                       # GP5 as Channel 0 LED panel
PhotoEyeIn 	= machine.Pin(2,machine.Pin.IN,machine.Pin.PULL_UP)    # GP2 as an INPUT for the photoeye
StallProgram = machine.Pin(17,machine.Pin.IN,machine.Pin.PULL_UP)    # Use GP17 as an INPUT for the switch

def main():
    
    for x in range(1,3):  #a simple routine just to flash the LED to alert us it rebooted.
        LED.value(1)
        sleep(.5)
        LED.value(0)
        sleep(.5)
        print("initializing")
    
    i2c = I2C(1, sda=Pin(26), scl=Pin(27), freq=400000)
    devices = i2c.scan()
    try:
        if devices != []:
            lcd_exist = True
            lcd = I2CLcd(i2c, devices[0], 2, 16)
            lcd.move_to(0, 0)
            lcd.putstr("Bodyguard Master")
            count = 0
            lcd_exist = True
        else:
            print("No address found")
    except:
        pass
    
    uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
    uart.init(bits=8, parity=None, stop=2)

    uart.write('Bodyguard Pico start...')
    


    
    wdt = WDT(timeout=2800)  # enable it with a timeout of 2s - must be feed within 2 seconds constantly!
    wdt.feed()               # must feed it right away!!
    
    while True:                        # Endless loop
                             # Take a brief nap to mimic work being done
        wdt.feed()                     # Replenish (Feed) the timer to keep it running
        print("Thanks!")
        #sleep(2.5) # Always thank someone for feeding you!
        '''
        Channel0.value(1)
        sleep(2)
        wdt.feed()
        Channel0.value(0)
        '''
        Channel0.value(1)
        Channel1.value(1)
        Channel2.value(1)
        Channel3.value(1)
        RelayNuc.value(1)
        RelayPoe.value(1)
        sleep(2)
        wdt.feed()
        sleep(2)
        wdt.feed()
        Channel0.value(0)
        Channel1.value(0)
        Channel2.value(0)
        Channel3.value(0)
        RelayNuc.value(0)
        RelayPoe.value(0)
        sleep(2)
        wdt.feed()
        sleep(2)
        wdt.feed()
        '''
        Channel2.value(1)
        sleep(2)
        wdt.feed()
        Channel2.value(0)
        Channel3.value(1)
        sleep(2)
        wdt.feed()
        Channel3.value(0)
        RelayNuc.value(1)
        sleep(1)
        wdt.feed()
        RelayNuc.value(0)
        RelayPoe.value(1)
        sleep(1)
        wdt.feed()
        RelayPoe.value(0)
        '''
        if (lcd_exist == True):
            count += 1
            lcd.move_to(0, 0)
            lcd.putstr("Bodyguard Master")
            lcd.move_to(0, 1)
            lcd.putstr("Counter:%d" %(count))
            
        if uart.any(): 
            data = uart.read()
            uart.write(data)
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("Received as:")
            lcd.move_to(0, 1)
            lcd.putstr(data.decode('utf-8'))
            
        if StallProgram.value() != 1:  # If Button is pressed
            while StallProgram.value() != 1:  #Prevent the timer from being fed while held down
                sleep(.1)
if __name__ == "__main__":
    main()