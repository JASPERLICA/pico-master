from machine import WDT   #Watch Dog Timer class
from machine import Pin
from time import sleep

Channel0    = machine.Pin(5,machine.Pin.OUT)                       # GP5 as Channel 0 LED panel
Channel1    = machine.Pin(6,machine.Pin.OUT)                       # GP6 as Channel 1 LED panel
Channel2    = machine.Pin(7,machine.Pin.OUT)                       # GP7 as Channel 2 LED panel
Channel3    = machine.Pin(15,machine.Pin.OUT)                      # GP7 as Channel 3 LED panel
LEDindic    = machine.Pin(28,machine.Pin.OUT)                       # GP5 as Channel 0 LED panel
PhotoEyeIn 	= machine.Pin(2,machine.Pin.IN,machine.Pin.PULL_UP)    # GP2 as an INPUT for the photoeye
StallProgram = machine.Pin(17,machine.Pin.IN,machine.Pin.PULL_UP)    # Use GP17 as an INPUT for the switch

def main():
    for x in range(1,5):  #a simple routine just to flash the LED to alert us it rebooted.
        LED.value(1)
        sleep(.5)
        LED.value(0)
        sleep(.5)
        print("initializing")  
    wdt = WDT(timeout=2800)  # enable it with a timeout of 2s - must be feed within 2 seconds constantly!
    wdt.feed()               # must feed it right away!!
    while True:                        # Endless loop
                             # Take a brief nap to mimic work being done
        wdt.feed()                     # Replenish (Feed) the timer to keep it running
        print("Thanks!")
        sleep(2.5) # Always thank someone for feeding you!
        if StallProgram.value() != 1:  # If Button is pressed
            while StallProgram.value() != 1:  #Prevent the timer from being fed while held down
                sleep(.1)
                
if __name__ == "__main__":
    main()


