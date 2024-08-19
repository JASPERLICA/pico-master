import network
import time
import socket
from machine import Pin
import random

led = Pin(5, Pin.OUT)
random_value = None
state = None
# def webpage():
def webpage(random_value, state):

    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pico Web Server</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            
        </head>
        <body>
            <h1 style="text-align: center">Vehicle Immobilizer</h1>
            <h2 style="text-align: center">Lock Status</h2>
            <form action="./Lock On">
                <input type="submit" value="Light on" style="width:200px;height:60px;font-size: 40px;text-align: center"/>
            </form>
            <br>
            <form action="./Lock off">
                <input type="submit" value="Light off" style="width:200px;height:60px;font-size: 40px;text-align: center"/>
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
        # html = "Raspberry Pi Pico Web Server"
        # return (html)
    return str(html)

# if you do not see the network you may have to power cycle
# unplug your pico w for 10 seconds and plug it in again
def ap_mode(ssid, password):
    global random_value, state
    """
        Description: This is a function to activate AP mode

        Parameters:

        ssid[str]: The name of your internet connection
        password[str]: Password for your internet connection

        Returns: Nada
    """
    # Just making our internet connection
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)

    while ap.active() == False:
        pass
    print('AP Mode Is Active, You can Now Connect')
    print('IP Address To Connect to:: ' + ap.ifconfig()[0])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
    s.bind(('', 80))
    s.listen(5)

    while True:
        try:
            conn, addr = s.accept()
            print('Got a connection from %s' % str(addr))
            request = conn.recv(1024)
            print('Content = %s' % str(request))

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
            # response = webpage()
            response = webpage(random_value, state)  

            # Send the HTTP response and close the connection
            conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            conn.send(response)
            conn.close()

        except OSError as e:
            conn.close()
            print('Connection closed')


if __name__ == "__main__":
    ap_mode('jasperpi', '12345678')
