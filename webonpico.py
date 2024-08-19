# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-web-server-micropython/

# Import necessary modules
import network
import socket
import time
import random
from machine import Pin,SPI
port = 80
localaddr = ''
# Create an LED object on pin 'LED'
led = Pin('LED', Pin.OUT)

# Wi-Fi credentials
ssid = 'REPLACE_WITH_YOUR_SSID'
password = 'REPLACE_WITH_YOUR_PASSWORD'


def w5100_init():

    global localaddr
    spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
    nic = network.WIZNET5K(spi,Pin(17),Pin(20)) #spi,cs,reset pin
    nic.active(True)

    global lcdFirstLine,lcdSecondLine 
    #None DHCP
    #nic.ifconfig(('192.168.11.15','255.255.255.0','192.168.11.1','8.8.8.8'))
    #DHCP

    con_flag = True
    while (con_flag):
        try:
            nic.ifconfig('dhcp')
            print(nic)
            
            con_flag = False
            localaddr = nic.ifconfig()[0]
            print(localaddr)
            print(type(localaddr))
            
        except:
            time.sleep(1)

            print("waiting DHCP address")

      
    print('IP address :', nic.ifconfig())
    while not nic.isconnected():
        time.sleep(1)
        print(nic.regs())


# HTML template for the webpage
def webpage(random_value, state):
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pico Web Server</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>Raspberry Pi Pico Web Server</h1>
            <h2>Led Control</h2>
            <form action="./lighton">
                <input type="submit" value="Light on" />
            </form>
            <br>
            <form action="./lightoff">
                <input type="submit" value="Light off" />
            </form>
            <p>LED state: {state}</p>
            <h2>Fetch New Value</h2>
            <form action="./value">
                <input type="submit" value="Fetch value" />
            </form>
            <p>Fetched value: {random_value}</p>
        </body>
        </html>
        """
    return str(html)

if __name__ == "__main__":

    #global localaddr
    # Connect to WLAN
    # wlan = network.WLAN(network.STA_IF)
    # wlan.active(True)
    # wlan.connect(ssid, password)

    # Wait for Wi-Fi connection
    # connection_timeout = 10
    # while connection_timeout > 0:
    #     if wlan.status() >= 3:
    #         break
    #     connection_timeout -= 1
    #     print('Waiting for Wi-Fi connection...')
    #     time.sleep(1)

    # Check if connection is successful
    # if wlan.status() != 3:
    #     raise RuntimeError('Failed to establish a network connection')
    # else:
    #     print('Connection successful!')
    #     network_info = wlan.ifconfig()
    #     print('IP address:', network_info[0])

    w5100_init()

    time.sleep(.5)
    # Set up socket and start listening
    # addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    # s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s1.connect(("8.8.8.8", 80))
    # addr = s1.getsockname()[0]
    # s1.shutdown() 
    # s1.close()

    print(localaddr)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((localaddr,port))
    s.listen()

    print('Listening on', localaddr)

    # Initialize variables
    state = "OFF"
    random_value = 0

    # Main loop to listen for connections
    while True:
        try:
            conn, addr = s.accept()
            print('Got a connection from', addr)
            
            # Receive and parse the request
            request = conn.recv(1024)
            request = str(request)
            print('Request content = %s' % request)

            try:
                request = request.split()[1]
                print('Request:', request)
            except IndexError:
                pass
            
            # Process the request and update variables
            if request == '/lighton?':
                print("LED on")
                led.value(1)
                state = "ON"
            elif request == '/lightoff?':
                led.value(0)
                state = 'OFF'
            elif request == '/value?':
                random_value = random.randint(0, 20)

            # Generate HTML response
            response = webpage(random_value, state)  

            # Send the HTTP response and close the connection
            conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            conn.send(response)
            conn.close()

        except OSError as e:
            conn.close()
            print('Connection closed')