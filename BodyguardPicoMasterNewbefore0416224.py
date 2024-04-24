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
import json
#define a global variable

TERMINATION_CHAR            = '\n'
SERIAL_TERMINATION_CHAR     = '\r'
NUC_IP = "192.168.20.155"   #server running on my Japer li pc
#NUC_IP = "192.168.0.102"   #server running on my Japer li pc at home network
PORT_NUMBER = 10001

WATCHDOG_PERIOD             = 4000 #was 2800
receiver_disconnected_flag  = False
reset_command_flag          = False
lcd_exist                   = False
time_NUC_alive              = time.time()


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

state_dict['Channel0']  = 'OFF'
state_dict['Channel1']  = 'OFF'
state_dict['Channel2']  = 'OFF'
state_dict['Channel3']  = 'OFF'
state_dict['Computer']  = 'ON'
state_dict['Poe_Sw']    = 'ON'

# Bodyguard Pinout definition

Channel0    =  Pin(5, Pin.OUT)                  # GP5 as Channel 0 LED panel
Channel1    =  Pin(6, Pin.OUT)                  # GP6 as Channel 1 LED panel
Channel2    =  Pin(7, Pin.OUT)                  # GP7 as Channel 2 LED panel
Channel3    =  Pin(15, Pin.OUT)                 # GP15 as Channel 3 LED panel
RelayNuc    =  Pin(4, Pin.OUT)                  # GP4 as Relay for Nuc
RelayPoe    =  Pin(3, Pin.OUT)                  # GP3 as Realy for POE

LED		     =  Pin(22, Pin.OUT)                # GP5 as Channel 0 LED panel
photoeye_npn =  Pin(2, Pin.IN, Pin.PULL_UP)     # GP2 as an INPUT for the photoeye
StallProgram =  Pin(17, Pin.IN, Pin.PULL_UP)    # Use GP17 as an INPUT for the switch
ButtonPageDn =  Pin(21, Pin.IN, Pin.PULL_UP)    # Check the message Down to next
ButtonPageUp =  Pin(20, Pin.IN, Pin.PULL_UP)    # Check the message Up

Channel0.value(False)
Channel1.value(False)
Channel2.value(False)
Channel3.value(False)
RelayNuc.value(False)
RelayPoe.value(False)



# Bodyguard tower DHCP configuration
# def w5100_init():

#     spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
#     nic = network.WIZNET5K(spi,Pin(17),Pin(20)) #spi,cs,reset pin
#     nic.active(True)
#     nic.ifconfig('dhcp')
#     print('IP address :', nic.ifconfig())
#     while not nic.isconnected():
#         time.sleep(1)
#         print(nic.regs())
      
            
def bodyguard_master_receiver(s,):
    global receiver_disconnected_flag,state_dict,reset_command_flag,time_NUC_alive
    full_msg = ''
    while True:
        try:
            # No.A waiting for message from NUC
            msg_data = s.recv(128)
            msg = msg_data.decode("utf-8")
            if msg == " ":
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
            s.send(bytes(f"Master board received from NUC: {msg} ","utf-8"))
            
            # No.B command handle
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
                reset_command_flag = True
                # while True:
                #         time.sleep(1)
                #         print("waiting for self reset by not feeding watchdog")
                #         s.send(bytes("waiting for self reset by not feeding watchdog","utf-8"))
            
            elif msg == "ALIVE"or msg == "alive":
                    time_NUC_alive = time.time()
                    print(f"recevied {msg} at {time_NUC_alive}")
     
        except:
            print("Bodyguard server disconnected,recever thread exit")
            receiver_disconnected_flag = True
            exit()



def lcd_initial():
    #LCD display
    global I2C,lcd,lcd_exist
    i2c = I2C(1, sda=Pin(26), scl=Pin(27), freq=400000)
    devices = i2c.scan()
    lcd_exist = False
    try:
        if devices != []:
            lcd_exist = True
            lcd = I2CLcd(i2c, devices[0], 2, 16)
            lcdFirstLine = "Bodyguard Master"
            lcdSecondLine = "Initialization.."
            lcd_flash(lcdFirstLine,lcdSecondLine)
            
        else:
            lcd_exist = False
            print("No LCD connected")
    except:
        pass


def lcd_flash(firstLine,sencondLine):
        global lcd,lcd_exist
        if len(firstLine) == 0:
            firstLine = "Bodyguard Master"
        if (lcd_exist == True):
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr(firstLine)
            lcd.move_to(0, 1)
            lcd.putstr(sencondLine)


def w5100_init():

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
            lcdFirstLine = " "
            lcdSecondLine = "Waiting IP addr"
            print("waiting DHCP address")
            lcd_flash(lcdFirstLine,lcdSecondLine)
      
    print('IP address :', nic.ifconfig())
    while not nic.isconnected():
        time.sleep(1)
        print(nic.regs())

def socket_init():
    global s
    count_connection = 0
    con_flag = True
    while (con_flag):
        try:
            count_connection += 1
            print(f"waiting socket be accpeted  {count_connection} s")

            s = socket.socket()
            s.connect((NUC_IP, PORT_NUMBER))
            print(s)
            con_flag = False
            
        except:
            time.sleep(1)
            lcdFirstLine = f"{NUC_IP}"
            lcdSecondLine = "waiting socket"
            print("connecting PC server")
            lcd_flash(lcdFirstLine,lcdSecondLine)
        
    print("Connection established...")
    lcdFirstLine = f"{NUC_IP}"
    lcdSecondLine = "established.."
    lcd_flash(lcdFirstLine,lcdSecondLine)

def uart_init():

    global uart
    uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
    uart.init(bits=8, parity=None, stop=1)
    uart.write(bytes('Bodyguard Pico start...',"utf-8"))

def main():
    
    global receiver_disconnected_flag, state_dict,reset_command_flag,lcd_exist,lcd,time_NUC_alive

    # No.1 gpio_initial_value
    Channel0.value(False)
    Channel1.value(False)
    Channel2.value(False)
    Channel3.value(False)
    state_dict['Channel0'] = 'OFF'
    state_dict['Channel1'] = 'OFF'
    state_dict['Channel2'] = 'OFF'
    state_dict['Channel3'] = 'OFF'

    # No.2 LCD initialization
    lcd_initial()

    # No.3 Reset NUC
    lcdFirstLine    = ""
    lcdSecondLine   =  "NUC starting"
    lcd_flash(lcdFirstLine,lcdSecondLine)
    RelayNuc.value(True)
    state_dict['Computer'] = 'OFF'
    time.sleep(2)
    RelayNuc.value(False)
    state_dict['Computer'] = 'ON'

    # No.4 Reset SWITCH
    lcdSecondLine   =  "SWITCH starting"
    lcd_flash(lcdFirstLine,lcdSecondLine)
    RelayPoe.value(True)
    state_dict['Poe_Sw'] = 'OFF'
    time.sleep(2)
    RelayPoe.value(False)
    state_dict['Poe_Sw'] = 'ON'
    reset_command_flag = False
    
    # No.5 Ethernet initialation
    lcdSecondLine   =  "Network starting"
    lcd_flash(lcdFirstLine,lcdSecondLine)
    w5100_init()
    time.sleep(.5)

    # No.6 UART Initialaztion
    lcdSecondLine   =  "UART starting"
    lcd_flash(lcdFirstLine,lcdSecondLine)
    uart_init()
    time.sleep(.5)
    # No.7 Socket initialization
    socket_init()

    # No.8 Creating Thread for Receiving message from computer
    time_NUC_alive = time.time() 
    _thread.start_new_thread(bodyguard_master_receiver,(s,)) #No deamon=True option in _thread

    # No.9 start the watch dog
    wdt = WDT(timeout=WATCHDOG_PERIOD)   
    wdt.feed()                         
    
    #local veriable in main
    toggle =  True
    state_dict['Photoeye'] = 'OFF'

    page = 0
    max_page = 7
    page_reading_mode   = False
    buttonPageDn_hold   = False
    last_time_update    = time.time()

    lcdFirstLine    = ""
    lcdSecondLine   = "Running..."
    lcd_flash(lcdFirstLine,lcdSecondLine)

    wdt.feed()
    
    while True:
        
        # No.1  feed watchdog
        wdt.feed()              
        
        # No.2 check reset command from NUC
        if reset_command_flag == True:
            while True:
                time.sleep(1)
                print("Reset command received and will reset within 4s")
                s.send(bytes("waiting for self reset by not feeding watchdog","utf-8"))
                
        # No.3 check photoeye sensor         
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
                
                try :
                    s.send(bytes(f"Photoeye:{state_dict['Photoeye']}{TERMINATION_CHAR}","utf-8"))
                except:
                    while True:
                        print("ethernet disconnected")
                        time.sleep(1)

                uart.write(bytes(f"Photoeye:{state_dict['Photoeye']}{TERMINATION_CHAR}","utf-8"))

                print(f"Photoeye change to :{state_dict['Photoeye']}")    

                lcdFirstLine    = ""
                lcdSecondLine   = f"Photoeye:{state_dict['Photoeye']}"
                lcd_flash(lcdFirstLine,lcdSecondLine)
                # time_update_time = time.time()      
        else:
            if  state_dict['Photoeye'] == 'ON':
                time.sleep(0.2)     #Anti disruption
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
                    lcd_flash(lcdFirstLine,lcdSecondLine)
        # No.4 check if socket disconneted
        if receiver_disconnected_flag == True:
            print("main thread exit....")
            #while True:
                #print("Network disconnected")
                #time.sleep(1)
            exit()

        # No.5 Check if Nuc keep responsing
        if (time.time() - time_NUC_alive) >= 30: #POE switch restarting need 30s
            print(time.time())
            print(time_NUC_alive)
            print("over 30's no response")

            #Network is found disconnected 
            wdt.feed()
            uart.write(bytes("HELLO","utf-8"))
            time.sleep(2)

            # check if NUC run properly
            if uart.any(): 
                data2 = uart.read()
                command_serial = data2.decode('utf-8')
                temp1 = command_serial.split(TERMINATION_CHAR)
                print(f"command_received {temp1}")
                command_serial2 = temp1[-1]
                if command_serial2 == "ALIVE":
                    RelayPoe.value(True)
                    state_dict['Poe_Sw'] = 'OFF'
                    lcdSecondLine   =  "Switch resetting"
                    lcd_flash(lcdFirstLine,lcdSecondLine)
                    wdt.feed()
                    time.sleep(2)
                    RelayPoe.value(False)
                    state_dict['Poe_Sw'] = 'ON'
                    time_NUC_alive = time.time()

            else:
                while True:
                        print("NUC restarting")
                        lcdSecondLine   =  "NUC restarting"
                        lcd_flash(lcdFirstLine,lcdSecondLine)
                        time.sleep(1)

        # No.6 reading data from UART
                
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
            lcd_flash(lcdFirstLine,lcdSecondLine)

            if command_serial == "reset" or command_serial == "RESET": 
                reset_command_flag = True

        # No.7 Button handle       
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
                    lcd_flash(lcdFirstLine,lcdSecondLine)
        else:
            if buttonPageDn_hold == True:
                time.sleep(0.01)
                if ButtonPageDn.value() == 1:
                    buttonPageDn_hold = False

        # No.8 Every other second : Update status to NUC // Uart
        if time.time()- last_time_update >= 2: #Auto report status to computer every 2 seconds
            last_time_update = time.time()   
            #print(state_dict.items())
            # No.A  Update status to NUC
            try:
                # s.send(bytes(f"{state_dict.items()} ","utf-8"))
                s.send(bytes(f"{state_dict} ","utf-8"))

                # data_serialized = json.dumps(state_dict)
                # s.send(data_serialized.encode('utf-8'))
                #if disconnected for some reason, OSError: [Errno 104] ECONNRESET
            except:
                while True:
                    print("Socket connection is dropped, waiting for self reset")
                    time.sleep(1)

            # No.B  Update status to NUC
            uart.write(bytes("ALIVE","utf-8"))
            # uart.write(bytes(f"{state_dict.items()} ","utf-8"))
            # uart.write(bytes(f"{str(state_dict)} ","utf-8"))
            
            # No.C  release LCD 
            if page_reading_mode == False:
                lcdSecondLine   = f"Photoeye:{state_dict['Photoeye']}"
                lcd_flash(lcdFirstLine,lcdSecondLine)
            else:
                if time.time() - readingTime >= 3:
                    page_reading_mode = False
                    page = 0
                    
if __name__ == "__main__":
    main()


# python函数里调用外部变量

# 1、可以直接使用
# 2、但不能直接修改，除非函数里global变量

# 当你在函数外部定义变量时，例如在文件顶部，它具有全局作用域，称为全局变量。

# 可以从程序中的任何位置访问全局变量。

# 你可以在函数体内使用它，也可以从函数外部访问它

