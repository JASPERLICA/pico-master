#BodyguardPicoMaster
#update date&time : 2024/10/10
VERSION =  '1.00'
# 
try:
    import usocket as socket
except:
    import socket
from machine import Pin,SPI,UART,I2C,WDT,PWM
from sys import exit
from I2C_LCD import I2CLcd
import network
import time
import _thread
import json
import BME280
from time import sleep

#global variable defination
TERMINATION_CHAR            = '\n'
SERIAL_TERMINATION_CHAR     = '\r'
NUC_IP                      = "192.168.30.1"      
PORT_NUMBER                 = 10001
WATCHDOG_PERIOD             = 4000 

#flag 
receiver_disconnected_flag  = False
reset_command_flag          = False
lcd_exist                   = False
IIC_idle                    = True
command_display_mode        = False
temperature_reading_mode    = False
file_update_mode            = False
Run_led_flip            	= False
Fun_remote_on_flag          = False

time_NUC_alive              = time.time()
time_command                = time.time()

lcdFirstLine                = ""
lcdSecondLine               = ""

photoeye_dict = {'Photoeye': 'OFF'
            }

state_dict = {'Photoeye': 'OFF', 
            'Computer': 'ON', 
            'Poe_Sw': 'ON',
            'Fun': 'OFF',
            'Channel0': 'OFF',
            'Channel1': 'OFF',
            'Channel2': 'OFF',
            'Channel3': 'OFF',
            'Temper'  :  '0',
            'Humidity' : '0',
            'Version': VERSION
            }
state_dict_in_bits = 0 # 


page_list = ['Photoeye', 
            'Computer', 
            'Poe_Sw',
            'Fun',
            'Channel0',
            'Channel1',
            'Channel2',
            'Channel3',
            'Temper',
            'Humidity',
            'Version'
            ]

state_dict['Channel0']  = 'OFF'
state_dict['Channel1']  = 'OFF'
state_dict['Channel2']  = 'OFF'
state_dict['Channel3']  = 'OFF'
state_dict['Computer']  = 'ON'
state_dict['Poe_Sw']    = 'ON'

Temperature_for_Fun_start = 33
Temperature_for_Fun_stop  = 27
Command_letters_max       = 24
LCD_IIC_address           = 0x27

# Bodyguard Pinout definition
Channel0        =  Pin(8, Pin.OUT)                  # GP8 as Channel 0 LED panel
Channel1        =  Pin(9, Pin.OUT)                  # GP9 as Channel 1 LED panel
Channel2        =  Pin(10, Pin.OUT)                 # GP10 as Channel 2 LED panel
Channel3        =  Pin(22, Pin.OUT)                 # GP22 as Channel 3 LED panel
RelayNuc        =  Pin(27, Pin.OUT)                 # GP27 as Relay for Nuc
RelayPoe        =  Pin(26, Pin.OUT)                 # GP26 as Realy for POE
LCD_Sensor      =  Pin(2, Pin.OUT)                  # GP2 as Power switch for LCD and sensor
wiznet_reset    =  Pin(20, Pin.OUT)                 # wiznet reset
MCU_reset       =  Pin(3, Pin.OUT)                  # mcu reset
MCU_run_led     =  Pin(11, Pin.OUT)                 # indicator for running properly
Fun             =  Pin(6, Pin.OUT)                  # GP6 as fun
light_pwm       =  Pin(5, Pin.OUT)                  # GP5 as LED panel intensity control
photoeye_npn    =  Pin(28, Pin.IN, Pin.PULL_UP)     # GP28 as an INPUT for the photoeye
ButtonPageDn    =  Pin(4, Pin.IN, Pin.PULL_UP)      # Check the message on LCD
wiznet_mosi     =  Pin(19)
wiznet_miso     =  Pin(16)
wiznet_sck      =  Pin(18)
wiznet_cs       =  Pin(17)
wiznet_reset    =  Pin(20)
uart_tx         =  Pin(0)
uart_rx         =  Pin(1)

#Set up I2C pinout
i2c         = I2C(0, sda=Pin(12), scl=Pin(13), freq=400000)
i2c_sensor  = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)

#UART pinout
uart      = UART(0, baudrate=115200, tx=uart_tx, rx=uart_rx,timeout=1)

# Bodyguard Pinout default value
Channel0.value(False)
Channel1.value(False)
Channel2.value(False)
Channel3.value(False)
RelayNuc.value(False)
RelayPoe.value(False)
LCD_Sensor.value(False)
Fun.value(False)

# Set up PWM Pin
led_panel = Pin(5)
led_pwm = PWM(led_panel)
duty_step = 129 #8192  # Step size for changing the duty cycle

#Set PWM frequency
frequency = 500
led_pwm.freq (frequency)

# master receiver process as one thread
          
def bodyguard_master_receiver(s,):
    global receiver_disconnected_flag,state_dict,reset_command_flag,\
        time_NUC_alive,lcdFirstLine_c,lcdSecondLine_c,time_command,led_pwm,\
            command_display_mode,IIC_idle,Fun_remote_on_flag
    # full_msg = ''
    while True:
        try:
            # No.A waiting for message from NUC
            msg_data = s.recv(128)
            msg = msg_data.decode("utf-8")
            if msg == " ":
                print("msg == empty")
                break
            elif len(msg) == 0:
                print("length of msg == 0")
                break
            #temp = msg.split("/")
            print(msg)
            temp = msg.split(TERMINATION_CHAR)
            #temp = msg.split()
            print(temp)
            msg = temp[-2]
            
            print(f"after split message : {msg}")
            # while global_lock == True:
            #     time.sleep(0.02)
            #     print("waiting for global_lock")

            # s.send(bytes(f"Master board received from NUC: {msg} ","utf-8"))
            
            if msg != "ALIVE":     

                lcdFirstLine_c = "Execute Command"
                lcdSecondLine_c = msg
                lcd_flash(lcdFirstLine_c,lcdSecondLine_c)
                command_display_mode = True
                
                time_command    = time.time()
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

            elif msg == "FUN ON"or msg == "fun on":
                Fun.value(True)
                state_dict['Fun'] = 'ON'
                Fun_remote_on_flag = True
            elif msg == "FUN OFF"or msg == "fun off":
                Fun.value(False)
                state_dict['Fun'] = 'OFF'
                Fun_remote_on_flag = False
            elif msg == "LED_BRIGHTER"or msg == "led_brighter":
                led_pwm.duty_u16(65530)
            
            elif msg == "LED_DIM"or msg == "led_dim":
                led_pwm.duty_u16(200)
    
            elif msg == "RESET"or msg == "reset":
                reset_command_flag = True
                # while True:
                #         time.sleep(1)
                #         print("waiting for self reset by not feeding watchdog")
                #         s.send(bytes("waiting for self reset by not feeding watchdog","utf-8"))
            
            elif msg == "ALIVE"or msg == "alive":
                    time_NUC_alive = time.time()
                    print(f"recevied {msg} at {time_NUC_alive}")

        except Exception as e:
            print(f"Bodyguard server disconnected,recever thread exit:{e}")
            # receiver_disconnected_flag = True #20240827
            # exit()



def lcd_initial():
    #LCD display
    global lcd,lcd_exist,IIC_idle, i2c,LCD_IIC_address
    # LCD_IIC_address = 0x27 #fixed ID
    lcd_exist = False
    devices = i2c.scan()
    try:
        if devices[0] == LCD_IIC_address:
            lcd_exist = True
            # lcd = I2CLcd(i2c, devices[0], 2, 16)
            lcd = I2CLcd(i2c, LCD_IIC_address, 2, 16)
            print("LCD is connected")
            lcdFirstLine = "Bodyguard Master"
            lcdSecondLine = "Initialization.."

            lcd_flash(lcdFirstLine,lcdSecondLine)
            
        else:
            lcd_exist = False
            print("No LCD plugged in")
    except:
        pass


def lcd_flash(firstLine,sencondLine):
        global lcd,lcd_exist,IIC_idle
        if IIC_idle:
            # if len(firstLine) == 0 or firstLine == " ":
            #     firstLine = "Bodyguard Master"
            if (lcd_exist == True):
                if len(firstLine) == 0 or firstLine == " ":
                    firstLine = "Bodyguard Master"
                IIC_idle = False
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr(firstLine)
                lcd.move_to(0, 1)
                lcd.putstr(sencondLine)
                IIC_idle = True

def temper_hum_pres_reading():
    global i2c_sensor
    global IIC_idle
    try:
        ambinent = []
        # Initialize BME280 sensor
        if IIC_idle:
            IIC_idle = False
            bme = BME280.BME280(i2c=i2c_sensor)
            
            # Read sensor data
            tempC = bme.temperature
            hum = bme.humidity
            pres = bme.pressure
            ambinent.append(tempC)
            ambinent.append(hum)
            ambinent.append(pres)
            # Convert temperature to fahrenheit
            tempF = (bme.read_temperature()/100) * (9/5) + 32
            tempF = str(round(tempF, 2)) + 'F'
            
            # Print sensor readings
            print('Temperature: ', tempC)
            print('Temperature: ', tempF)
            print('Humidity: ', hum)
            print('Pressure: ', pres)
            IIC_idle = True
        
        return(ambinent)
        
    except Exception as e:
        # Handle any exceptions during sensor reading
        print('An error occurred:', e)
        # LCD_Sensor.value(False)
        # sleep(.6)
        # LCD_Sensor.value(True)
        # sleep(.2)
        # lcd_initial()
        return None

def w5100_init():

    global lcdFirstLine,lcdSecondLine 

    spi       =SPI(0,2_000_000, mosi=wiznet_mosi,miso=wiznet_miso,sck=wiznet_sck)
    nic       = network.WIZNET5K(spi,wiznet_cs,wiznet_reset) #spi,cs,reset pin
    nic.active(True)

    #None DHCP
    #nic.ifconfig(('192.168.30.15','255.255.255.0','192.168.30.1','8.8.8.8'))
    #DHCP

    con_flag = True
    while (con_flag):
        try:
            nic.ifconfig('dhcp')
            print(nic)
            con_flag = False
        except:
            time.sleep(1)
            lcdFirstLine = "Bodyguard Master"
            lcdSecondLine = "Waiting IP addr"
            print("waiting DHCP address")
            
            lcd_flash(lcdFirstLine,lcdSecondLine)
      
    print('IP address :', nic.ifconfig())
    while not nic.isconnected():
        time.sleep(1)
        print(nic.regs())

def socket_init():
    global s
    global lcdFirstLine,lcdSecondLine
    count_connection = 0
    socket_flag = True
    while (socket_flag):
        try:
            count_connection += 1
            print(f"waiting socket be accpeted  {count_connection} s")

            s = socket.socket()
            s.connect((NUC_IP, PORT_NUMBER))
            print(s)
            socket_flag = False
            
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
   
    # uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1),timeout=1)
    uart.init(bits=8, parity=None, stop=1)
    uart.write(bytes('Bodyguard Pico start...',"utf-8"))

def led_boards_all_off():
    global state_dict

    Channel0.value(False)
    Channel1.value(False)
    Channel2.value(False)
    Channel3.value(False)
    state_dict['Channel0'] = 'OFF'
    state_dict['Channel1'] = 'OFF'
    state_dict['Channel2'] = 'OFF'
    state_dict['Channel3'] = 'OFF'

def main():
    
    global receiver_disconnected_flag, state_dict,reset_command_flag,\
        lcd_exist,lcd,IIC_idle,time_NUC_alive,time_command,I2C,Run_led_flip,\
            command_display_mode,lcdFirstLine_c,lcdSecondLine_c,uart,\
            state_dict_in_bits
    
            # temperature_reading_mode,global_lock

    # No.1 gpio_initial_value
    led_boards_all_off()
 
    # No.2 LCD initializationc
    LCD_Sensor.value(True)
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
    lcdSecondLine   =  "Wiznet starting"  
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

    # No.8 Creating secondary Thread for Receiving message from computer
    time_NUC_alive = time.time() 
    _thread.start_new_thread(bodyguard_master_receiver,(s,)) #No deamon=True option in _thread

    # No.9 View defult settiing
    page = 0
    max_page = 10
    page_reading_mode   = False
    buttonPageDn_hold   = False
    last_time_update    = time.time()

    lcdFirstLine    = " "
    lcdSecondLine   = "Running..."   
    lcd_flash(lcdFirstLine,lcdSecondLine)

    # No.10 start the watch dog
    wdt = WDT(timeout=WATCHDOG_PERIOD)   
    wdt.feed()  

    # main thread
    while True:
        
        # No.1  feed watchdog
        wdt.feed()              
        
        # No.2 check reset command from NUC
        if reset_command_flag == True:
            while True:
                led_boards_all_off()
                time.sleep(1)
                print("Reset command received and will reset within 4s")
                s.send(bytes("waiting for self reset by not feeding watchdog","utf-8"))
                
        # No.3 check photoeye sensor         
        if not photoeye_npn.value(): #Blocked == 0
            if  state_dict['Photoeye'] == 'OFF':
                state_dict['Photoeye'] = 'ON'
                
                photoeye_dict['Photoeye'] = 'ON'
                Channel0.value(True)    #ON
                state_dict['Channel0'] = 'ON'
                Channel1.value(True)    #ON
                state_dict['Channel1'] = 'ON'
                Channel2.value(True)    #ON
                state_dict['Channel2'] = 'ON'
                Channel3.value(True)    #ON
                state_dict['Channel3'] = 'ON'
                
                try :
                    data_json1 = json.dumps(photoeye_dict)
                    s.send(data_json1.encode('utf-8'))
                    #s.send(bytes(f"Photoeye:{state_dict['Photoeye']}{TERMINATION_CHAR}","utf-8"))
                except:
                    while True:
                        print("ethernet disconnected")
                        lcdFirstLine    = "Ethernet"
                        lcdSecondLine   = "Unreachable"
                        lcd_flash(lcdFirstLine,lcdSecondLine)

                        led_boards_all_off()
                        time.sleep(1)

                uart.write(bytes(f"Photoeye:{state_dict['Photoeye']}{TERMINATION_CHAR}","utf-8"))

                print(f"Photoeye change to :{state_dict['Photoeye']}")    

                lcdFirstLine    = ""
                lcdSecondLine   = f"Photoeye:{state_dict['Photoeye']}"
                
                lcd_flash(lcdFirstLine,lcdSecondLine)
                # time_update_time = time.time()      
        else:
            if  state_dict['Photoeye'] == 'ON':
                time.sleep(0.05)     #Anti disruption
                if photoeye_npn.value(): # == 1
                    state_dict['Photoeye'] = 'OFF'
                    photoeye_dict['Photoeye'] = 'OFF'
                    
                    Channel0.value(False)   #OFF
                    state_dict['Channel0'] = 'OFF'
                    Channel1.value(False)   #OFF
                    state_dict['Channel1'] = 'OFF'
                    Channel2.value(False)   #OFF
                    state_dict['Channel2'] = 'OFF'
                    Channel3.value(False)   #OFF
                    state_dict['Channel3'] = 'OFF'

                    # data_json = json.dumps(photoeye_dict)
                    # s.send(data_json.encode('utf-8'))

                    try :
                        data_json2 = json.dumps(photoeye_dict)
                        s.send(data_json2.encode('utf-8'))
                        #s.send(bytes(f"Photoeye:{state_dict['Photoeye']}{TERMINATION_CHAR}","utf-8"))
                    except:
                        while True:
                            print("ethernet disconnected")
                            lcdFirstLine    = "Ethernet"
                            lcdSecondLine   = "Unreachable"
                            lcd_flash(lcdFirstLine,lcdSecondLine)

                            led_boards_all_off()
                            time.sleep(1)

                    # s.send(bytes(f"Photoeye:{state_dict['Photoeye']}{TERMINATION_CHAR}","utf-8"))
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
            print("over 30's no responding")

            #Network is found disconnected 
            wdt.feed()
            uart.write(bytes("HELLO","utf-8"))
            time.sleep(3) # if no reply within 3s

            # check if NUC run properly
            if uart.any(): 
                data2 = uart.read()
                command_serial = data2.decode('utf-8')
                serial_data = command_serial.split(TERMINATION_CHAR)
                print(f"command_received {serial_data}")
                command_serial2 = serial_data[-1]
                if command_serial2 == "ALIVE":
                    RelayPoe.value(True)
                    state_dict['Poe_Sw'] = 'OFF'
                    lcdSecondLine   =  "POE restarting"
                    
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
                        led_boards_all_off()
                        time.sleep(1)

        # No.6 reading data from UART
                
        if uart.any(): 
            raw_data = uart.read()
            if len(raw_data) <= Command_letters_max: #command should less than 24 bytes
            # if not file_update_mode:
                uart.write(f"uart receiced {raw_data}")
                try:
                    command_serial = raw_data.decode('utf-8')
                    serial_data = command_serial.split(TERMINATION_CHAR)
                    print(serial_data)              
                    command_serial = serial_data[-2]
                
                    lcdSecondLine   =  command_serial[0:15] # Maximum 16 charactes                   
                    lcd_flash(lcdFirstLine,lcdSecondLine)

                    if command_serial == "reset" or command_serial == "RESET": 
                        reset_command_flag = True
                    
                    if command_serial == "serial_test" or command_serial == "SERIAL_TEST":
                        print("serial receive serial test")
                        lcdFirstLine    =  "FROM SERIAL"
                        lcdSecondLine   =  "SERAIL TESTING"
                        
                        lcd_flash(lcdFirstLine,lcdSecondLine)
                        file_update_mode = True
                except:
                    pass
            else: #it is file
                try:
                    file_data = raw_data.decode('utf-8')
                except:
                    print("wrong data from UART")
                if file_data.find("#BodyguardPicoMaster") == 0:
                    with open("newBodyguardPicoMaster.py","w") as f:
                        f.write(file_data)
                        f.flush()
                        f.close()

                    with open("version.txt","a") as f:
                            f.write("newBodyguardPicoMaster.py")
                            f.flush()
                            f.close()
                    while(True):

                        lcdFirstLine    = "Firmware Updated"
                        lcdSecondLine   = "Restarting..."
                        lcd_flash(lcdFirstLine,lcdSecondLine)
                        led_boards_all_off()
                        time.sleep(1)
                    

        # No.7 Button handle       
        if ButtonPageDn.value() == 0:
            if buttonPageDn_hold == False:
                #startTime = time.ticks_ms()
                time.sleep(0.05)
                if ButtonPageDn.value() == 0:
                    buttonPageDn_hold = True
                    
                    # toggle = not toggle
                    # LED.value(toggle)
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
            Run_led_flip = (not Run_led_flip)
            if Run_led_flip == True:
                MCU_run_led.value(True)
            else:
                MCU_run_led.value(False)
            
            # No.A  Update status to NUC
            # interval += 1 #update the new data to computer every 20 second 
            # if interval >= 10:
            #     interval =0

            # No.A  Update status to NUC
            state_dict_in_bits = 0  
            if state_dict['Photoeye'] == 'ON':
                state_dict_in_bits = (1 << 7)
            if state_dict['Computer'] == 'ON':
                state_dict_in_bits = state_dict_in_bits | (1 << 6)
            if state_dict['Poe_Sw'] == 'ON':
                state_dict_in_bits = state_dict_in_bits | (1 << 5)
            if state_dict['Fun'] == 'ON':
                state_dict_in_bits = state_dict_in_bits | (1 << 4)
            if state_dict['Channel0'] == 'ON':
                state_dict_in_bits = state_dict_in_bits | (1 << 3)
            if state_dict['Channel1'] == 'ON':
                state_dict_in_bits = state_dict_in_bits | (1 << 2)
            if state_dict['Channel2'] == 'ON':
                state_dict_in_bits = state_dict_in_bits | (1 << 1)
            if state_dict['Channel3'] == 'ON':
                state_dict_in_bits = state_dict_in_bits | (1 << 0)
            print(f"state dict in bit is {state_dict_in_bits}")
            # checksum = 0xaa ^ state_dict_in_bits
            # state_dict_in_bits_array = [0xaa, state_dict_in_bits, checksum]
            # data_dict = bytearray(state_dict_in_bits_array)

            try:
                data_json = json.dumps(state_dict)
                s.send(data_json.encode('utf-8'))
                data_json_state_dict_in_bits = json.dumps({"Status":state_dict_in_bits})
                s.send(data_json_state_dict_in_bits.encode('utf-8'))
                #if disconnected for some reason, OSError: [Errno 104] ECONNRESET
            except:
                while True:
                    print("Socket connection is dropped, waiting for self reset")
                    led_boards_all_off()
                    time.sleep(1)

            # No.B  Update status to NUC over serial
            uart.write(bytes("Linked","utf-8"))
            # uart.write(bytes(f"{state_dict.items()} ","utf-8"))
            # uart.write(bytes(f"{str(state_dict)} ","utf-8"))
            
            # No.C  release LCD 

            # if page_reading_mode == False:
            #     lcdSecondLine   = f"Photoeye:{state_dict['Photoeye']}"
            #     if IIC_idle:
            #         lcd_flash(lcdFirstLine,lcdSecondLine)
            # else:
            #     if time.time() - readingTime >= 3:
            #         page_reading_mode = False
            #         page = 0

            if page_reading_mode == True:
                if time.time() - readingTime >= 4:
                    page_reading_mode = False
                    page = 0
                    lcdSecondLine   = f"Photoeye:{state_dict['Photoeye']}"
                    
                    lcd_flash(lcdFirstLine,lcdSecondLine)
            
            # No.D release lcd
            if command_display_mode == True:

                if time.time() - time_command >= 3:
                    lcdFirstLine = " "
                    lcdSecondLine   = f"Photoeye:{state_dict['Photoeye']}"
                    
                    lcd_flash(lcdFirstLine,lcdSecondLine)
                    command_display_mode = False
            
            #No.E temperture reading
            
            ambinent_TAP = temper_hum_pres_reading()
            if ambinent_TAP is not None:
                try:
                    state_dict['Temper'] = ambinent_TAP[0]
                    state_dict['Humidity'] = ambinent_TAP[1]
                    print(f"the tempture is {state_dict['Temper']}")
                    
                    temp0 = state_dict['Temper'].split("C", 1)

                    # temp0 = state_dict['Temper'][:4]
                    print(temp0[0])
                    temperature = float(temp0[0])
                    if temperature >= Temperature_for_Fun_start :
                        Fun.value(True)
                        state_dict['Fun'] = 'ON'
                    elif temperature <= Temperature_for_Fun_stop and not Fun_remote_on_flag:        
                        Fun.value(False)
                        state_dict['Fun'] = 'OFF'
                except:
                    print("ambient_TAP reading error")
            else:
                state_dict['Temper'] = "0.0"
                state_dict['Humidity'] = "0.0%"
                
if __name__ == "__main__":
    main()




