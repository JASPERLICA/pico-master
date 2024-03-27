
import time

LED		     =  Pin(22, Pin.OUT)                       # GP5 as Channel 0 LED panel
photoeye_npn =  Pin(2, Pin.IN, Pin.PULL_UP)    # GP2 as an INPUT for the photoeye
StallProgram =  Pin(17, Pin.IN, Pin.PULL_UP)    # Use GP17 as an INPUT for the switch

ButtonPageDn =  Pin(21, Pin.IN, Pin.PULL_UP)    # Check the message Down to next
ButtonPageUp =  Pin(20, Pin.IN, Pin.PULL_UP)    # Check the message Up


buttonPageDn_hold = False
toggle = True

while True:
   if ButtonPageDn.value() == 0:
        if buttonPageDn_hold == False:
            #startTime = time.ticks_ms()
            time.sleep(0.05)
            if ButtonPageDn.value() == 0:
                buttonPageDn_hold = True
                
                toggle = not toggle
                LED.value(toggle)
    else:
        if buttonPageDn_hold == True:
            time.sleep(0.01)
            if ButtonPageDn.value() == 1:
                buttonPageDn_hold = False
