try:
    import usocket as socket
except:
    import socket
from machine import Pin,SPI,UART,I2C,WDT
from sys import exit
from I2C_LCD import I2CLcd
import urequests
import network
import time
import _thread
TERMINATION_CHAR = '\n'
SERIAL_TERMINATION_CHAR = '\r'

#Command /ALL_ON
#Command /ALL_OFF

WatchDogMax = 4000
#define a global variable
thread_receiver_alive_flag = False
server_IP = "192.168.20.155" #server running on my Japer li pc
#server_IP = "192.168.11.132" # server running on my computer at banalogic
# Bodyguard Pinout definition

state_dict = {'Photoeye': 'OFF', 
            'Computer': 'ON', 
            'Poe_Sw': 'ON',
            'Channel0': 'OFF',
            'Channel1': 'OFF',
            'Channel2': 'OFF',
            'Channel3': 'OFF',
            'Version':'1.0'
            }

page_list = ['Photoeye', 
            'Computer', 
            'Poe_Sw',
            'Channel0',
            'Channel1',
            'Channel2',
            'Channel3',
            'Version'
            ]

Channel0    =  Pin(5, Pin.OUT)                       # GP5 as Channel 0 LED panel
Channel1    =  Pin(6, Pin.OUT)                       # GP6 as Channel 1 LED panel
Channel2    =  Pin(7, Pin.OUT)                       # GP7 as Channel 2 LED panel
Channel3    =  Pin(15, Pin.OUT)                      # GP7 as Channel 3 LED panel
Channel0.value(False)
Channel1.value(False)
Channel2.value(False)
Channel3.value(False)

state_dict['Channel0'] = 'OFF'
state_dict['Channel1'] = 'OFF'
state_dict['Channel2'] = 'OFF'
state_dict['Channel3'] = 'OFF'


RelayNuc    =  Pin(4, Pin.OUT)                       # GP7 as Channel 2 LED panel
RelayPoe    =  Pin(3, Pin.OUT)                      # GP7 as Channel 3 LED panel
RelayNuc.value(False)
RelayPoe.value(False)
state_dict['Computer'] = 'ON'
state_dict['Poe_Sw'] = 'ON'

LED		     =  Pin(22, Pin.OUT)                       # GP5 as Channel 0 LED panel
photoeye_npn =  Pin(2, Pin.IN, Pin.PULL_UP)    # GP2 as an INPUT for the photoeye
StallProgram =  Pin(17, Pin.IN, Pin.PULL_UP)    # Use GP17 as an INPUT for the switch

ButtonPageDn =  Pin(21, Pin.IN, Pin.PULL_UP)    # Check the message Down to next
ButtonPageUp =  Pin(20, Pin.IN, Pin.PULL_UP)    # Check the message Up

portnumber = 10001
reset_command = False
lcd_exist = False
#Data_Key = _thread.allocate_lock()  # create a semaphore locking mechanism
#Data_Key.acquire()   
#Data_Key.release()
time_NUC_alive = time.time()
# Bodyguard tower DHCP configuration
def w5100_init():
    spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
    nic = network.WIZNET5K(spi,Pin(17),Pin(20)) #spi,cs,reset pin
    nic.active(True)
#None DHCP
    #nic.ifconfig(('192.168.11.15','255.255.255.0','192.168.11.1','8.8.8.8'))
#DHCP
    nic.ifconfig('dhcp')
      
    print('IP address :', nic.ifconfig())
    while not nic.isconnected():
        time.sleep(1)
        print(nic.regs())
      
def bodyguard_client():
    s = socket.socket()
    s.connect((server_IP, portnumber))#16653
    print("bodyguard tower connected...")
    full_msg = ''
    while True:
            msg1 = s.recv(1024)
            if len(msg1) <= 0:
                break
            full_msg += msg1.decode("utf-8")
            print(full_msg)
            s.send(bytes(f"bodyguard tower received {full_msg} ","utf-8"))
            
def bodyguard_master_receiver(s,):
    global thread_receiver_alive_flag,state_dict,reset_command,time_NUC_alive
    full_msg = ''
    while True:
        try:
            msg_data = s.recv(128)
            msg = msg_data.decode("utf-8")
            if msg == "":
                break
            elif len(msg) == 0:
                break
            #temp = msg.split("/")
            print(msg)
            temp = msg.split(TERMINATION_CHAR)
            #temp = msg.split()
            print(temp)
            msg = temp[-2]
            
            print(f"after split message : {msg}")
            s.send(bytes(f"Master board confirmed: {msg} ","utf-8"))
            
            if msg == "ALL ON" or msg == "all on":
                Channel0.value(True)    #ON
                state_dict['Channel0'] = 'ON'
                Channel1.value(True)    #ON
                state_dict['Channel1'] = 'ON'
                Channel2.value(True)    #ON
                state_dict['Channel2'] = 'ON'
                Channel3.value(True)    #ON
                state_dict['Channel3'] = 'ON'
            elif msg == "ALL OFF" or msg == "all off":
                Channel0.value(False)   #OFF
                state_dict['Channel0'] = 'OFF'
                Channel1.value(False)   #OFF
                state_dict['Channel1'] = 'OFF'
                Channel2.value(False)   #OFF
                state_dict['Channel2'] = 'OFF'
                Channel3.value(False)   #OFF
                state_dict['Channel3'] = 'OFF'

            elif msg == "CHANNEL0_ON" or msg == "channel0_on":
                Channel0.value(True)    #ON
                state_dict['Channel0'] = 'ON'
            elif msg == "CHANNEL0_OFF"or msg == "channel0_off":
                Channel0.value(False)   #OFF
                state_dict['Channel0'] = 'OFF'
            elif msg == "CHANNEL1_ON" or msg == "channel1_on":
                Channel1.value(True)    #ON
                state_dict['Channel1'] = 'ON'
            elif msg == "CHANNEL1_OFF"or msg == "channel1_off":
                Channel1.value(False)   #OFF
                state_dict['Channel1'] = 'OFF'
            elif msg == "CHANNEL2_ON" or msg == "channel2_on":
                Channel2.value(True)    #ON
                state_dict['Channel2'] = 'ON'
            elif msg == "CHANNEL2_OFF"or msg == "channel2_off":
                Channel2.value(False)   #OFF
                state_dict['Channel2'] = 'OFF'
            elif msg == "CHANNEL3_ON" or msg == "channel3_on":
                Channel3.value(True)    #ON
                state_dict['Channel3'] = 'ON'
            elif msg == "CHANNEL3_OFF"or msg == "channel3_off":
                Channel3.value(False)   #OFF
                state_dict['Channel3'] = 'OFF'
            
            elif msg == "POE RESET"or msg == "poe reset":
                RelayPoe.value(True)
                state_dict['Poe_Sw'] = 'OFF'
                time.sleep(2)
                RelayPoe.value(False)
                state_dict['Poe_Sw'] = 'ON'

            elif msg == "NUC RESET"or msg == "nuc reset":
                RelayNuc.value(True)
                state_dict['Computer'] = 'OFF'
                time.sleep(2)
                RelayNuc.value(False)
                state_dict['Computer'] = 'ON'
    
            elif msg == "RESET"or msg == "reset":
                    reset_command = True
                    while True:
                        time.sleep(1)
                        print("waiting for self reset by not feeding watchdog")
                        s.send(bytes("waiting for self reset by not feeding watchdog","utf-8"))
            
            elif msg == "ALIVE"or msg == "alive":
                    time_NUC_alive = time.time()
                    print(f"recevied {msg} at {time_NUC_alive}")


              
        except:
            print("Bodyguard server disconnected,recever thread exit")
            thread_receiver_alive_flag = True
            exit()
            

def lcd_flash(lcd_exist,lcd,firstLine,sencondLine):
        if len(firstLine) == 0:
            firstLine = "Bodyguard Master"
        if (lcd_exist == True):
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr(firstLine)
            lcd.move_to(0, 1)
            lcd.putstr(sencondLine)

def main():
    
    global thread_receiver_alive_flag, state_dict,reset_command,lcd_exist,time_NUC_alive

    Channel0.value(False)
    Channel1.value(False)
    Channel2.value(False)
    Channel3.value(False)
    state_dict['Channel0'] = 'OFF'
    state_dict['Channel1'] = 'OFF'
    state_dict['Channel2'] = 'OFF'
    state_dict['Channel3'] = 'OFF'

    #LCD display
    i2c = I2C(1, sda=Pin(26), scl=Pin(27), freq=400000)
    devices = i2c.scan()
    lcd_exist = False
    try:
        if devices != []:
            lcd_exist = True
            lcd = I2CLcd(i2c, devices[0], 2, 16)
            lcdFirstLine = "Bodyguard Master"
            lcdSecondLine = "Initialization.."
            lcd_flash(lcd_exist,lcd,lcdFirstLine,lcdSecondLine)
        else:
            lcd_exist = False
            print("No address found")
    except:
        pass
    
    #Reset Nuc and Switch
    RelayNuc.value(True)
    state_dict['Computer'] = 'OFF'
    time.sleep(2)
    RelayNuc.value(False)
    state_dict['Computer'] = 'ON'

    RelayPoe.value(True)
    state_dict['Poe_Sw'] = 'OFF'
    time.sleep(2)
    RelayPoe.value(False)
    state_dict['Poe_Sw'] = 'ON'
    reset_command = False
    
    #UART Initialaztion
    uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
    uart.init(bits=8, parity=None, stop=1)

    uart.write(bytes('Bodyguard Pico start...',"utf-8"))
    
    #Ethernet initialization
    #w5100_init()

    spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
    nic = network.WIZNET5K(spi,Pin(17),Pin(20)) #spi,cs,reset pin
    nic.active(True)
#None DHCP
    #nic.ifconfig(('192.168.11.15','255.255.255.0','192.168.11.1','8.8.8.8'))
#DHCP

    con_flag = True
    while (con_flag):
        try:
            nic.ifconfig('dhcp')
            print(nic)
            con_flag = False
        except:
            time.sleep(1)
            lcdSecondLine = "waiting DHCP"
            print("waiting DHCP")
            lcd_flash(lcd_exist,lcd,lcdFirstLine,lcdSecondLine)
      
    print('IP address :', nic.ifconfig())
    while not nic.isconnected():
        time.sleep(1)
        print(nic.regs())

    #Socket initialization
    #s = socket.socket()
    #print(s)
    count_connection = 0
    con_flag = True
    while (con_flag):
        try:
            count_connection += 1
            print(count_connection)
            
            s = socket.socket()
            s.connect((server_IP, portnumber))#10001
            print(s)
            con_flag = False
        except:
            time.sleep(1)
            lcdSecondLine = "linking server"
            print("connecting PC server")
            lcd_flash(lcd_exist,lcd,lcdFirstLine,lcdSecondLine)
        
    print("Connection established...")
    time_NUC_alive = time.time() #computer app started
    #Thread for Receiving message from computer
    _thread.start_new_thread(bodyguard_master_receiver,(s,))
    
    #photoeye_npn.irq(trigger=Pin.IRQ_FALLING, handler=callback)
    
    wdt = WDT(timeout=2800)  # enable it with a timeout of 2s - must be feed within 2 seconds constantly!
    wdt.feed()               # must feed it right away!!
    
    time_update_time = time.time()
    time0 = time.time()
    debounce_time = 0
    toggle =  True
    Photoeye_State = False
    state_dict['Photoeye'] = 'OFF'
    time_upper_update_time = time.time()
    upper_unsend = True
    buttonPageDn_hold = False
    page = 0
    max_page = 7
    page_reading_mode = False

    lcdSecondLine   = "Running..."
    lcd_flash(lcd_exist,lcd,lcdFirstLine,lcdSecondLine)

    wdt.feed()
    
    while True:
        
        wdt.feed()               # must feed it right away!!
        
        if reset_command == True:
            while True:
                print("reset command received")
                time.sleep(1)
                
            
        if not photoeye_npn.value(): #Blocked == 0
            if  state_dict['Photoeye'] == 'OFF':
                state_dict['Photoeye'] = 'ON'
                
                Channel0.value(True)    #ON
                state_dict['Channel0'] = 'ON'
                Channel1.value(True)    #ON
                state_dict['Channel1'] = 'ON'
                Channel2.value(True)    #ON
                state_dict['Channel2'] = 'ON'
                Channel3.value(True)    #ON
                state_dict['Channel3'] = 'ON'
                
                s.send(bytes(f"Photoeye:{state_dict['Photoeye']}{TERMINATION_CHAR}","utf-8"))
                uart.write(bytes(f"Photoeye:{state_dict['Photoeye']}{TERMINATION_CHAR}","utf-8"))

                print(f"Photoeye:{state_dict['Photoeye']}")    

                lcdSecondLine   = f"Photoeye:{state_dict['Photoeye']}"
                lcd_flash(lcd_exist,lcd,lcdFirstLine,lcdSecondLine)
                time_update_time = time.time()      
        else:
            if  state_dict['Photoeye'] == 'ON':
                time.sleep(0.2) #Anti disruption
                if photoeye_npn.value(): # == 1
                    state_dict['Photoeye'] = 'OFF'
                    
                    Channel0.value(False)   #OFF
                    state_dict['Channel0'] = 'OFF'
                    Channel1.value(False)   #OFF
                    state_dict['Channel1'] = 'OFF'
                    Channel2.value(False)   #OFF
                    state_dict['Channel2'] = 'OFF'
                    Channel3.value(False)   #OFF
                    state_dict['Channel3'] = 'OFF'
                
                    s.send(bytes(f"Photoeye:{state_dict['Photoeye']}{TERMINATION_CHAR}","utf-8"))
                    uart.write(bytes(f"Photoeye:{state_dict['Photoeye']}{TERMINATION_CHAR}","utf-8"))
                    
                    print(f"Photoeye:{state_dict['Photoeye']}")

                    lcdSecondLine   = f"Photoeye:{state_dict['Photoeye']}"
                    lcd_flash(lcd_exist,lcd,lcdFirstLine,lcdSecondLine)
      
        if thread_receiver_alive_flag == True:
            print("main thread exit....")
            #while True:
                #print("Network disconnected")
                #time.sleep(1)
            exit()

        if (time.time() - time_NUC_alive) >= 20:
            print(time.time())
            print(time_NUC_alive)
            while True:
                    print("NUC restart")
                    time.sleep(1)

            
        if time.time()- time0 >= 2: #Auto report status to computer every 2 seconds
            time0 = time.time() 
            #toggle = not toggle
            #LED.value(toggle)
            
            #print(state_dict.items())
            try:
                s.send(bytes(f"{state_dict.items()} ","utf-8"))
                #if disconnected for some reason, OSError: [Errno 104] ECONNRESET
            except:
                while True:
                    print("Socket connection is dropped, waiting for self reset")
                    time.sleep(1)


            uart.write(bytes(f"{state_dict.items()} ","utf-8"))
            #print("tower is alive...")
            if page_reading_mode == False:
                lcdSecondLine   = f"Photoeye:{state_dict['Photoeye']}"
                lcd_flash(lcd_exist,lcd,lcdFirstLine,lcdSecondLine)
            else:
                if time.time() - readingTime >= 3:
                    page_reading_mode = False
                    page = 0
                    
            
            if uart.any(): 
                data1 = uart.read()
                uart.write(f"uart receiced {data1}")
                try:
                    command_serial = data1.decode('utf-8')
                    temp1 = command_serial.split(TERMINATION_CHAR)
                    print(temp1)              
                    command_serial = temp1[-2]
                except:
                    pass

                lcdSecondLine   =  command_serial
                lcd_flash(lcd_exist,lcd,lcdFirstLine,lcdSecondLine)

                if command_serial == "reset" or command_serial == "RESET": 
                    reset_command = True
                
        if ButtonPageDn.value() == 0:
            if buttonPageDn_hold == False:
                #startTime = time.ticks_ms()
                time.sleep(0.05)
                if ButtonPageDn.value() == 0:
                    buttonPageDn_hold = True
                    
                    toggle = not toggle
                    LED.value(toggle)
                    page_reading_mode = True
                    readingTime = time.time()
                    page += 1
                    if page > max_page:
                        page = 0
                    
                    temppage = page_list[page]
                    str2 = state_dict.get(temppage)
                    str1 = temppage + ":" + str2 
                    print(str1)

                    lcdSecondLine   =  str1
                    lcd_flash(lcd_exist,lcd,lcdFirstLine,lcdSecondLine)
        else:
            if buttonPageDn_hold == True:
                time.sleep(0.01)
                if ButtonPageDn.value() == 1:
                    buttonPageDn_hold = False
  
                

               
                
               #startTime = time.ticks_ms()
               
               
    #bg_receiver_thread.daemon = True
    #bg_receiver_thread.start()
#   button = Pin(14, Pin.IN, Pin.PULL_UP)
# 
# while True:
#     if button.value() == 0:
#         print('Button is pressed')
#     else:
#         print('Button is not pressed')
#     time.sleep(0.1)  
    
if __name__ == "__main__":
    main()