import network
import time
import socket
from machine import Pin,WDT


# wdt = WDT(timeout = 5000)
# wdt.feed() 
# import random

relay = Pin(22, Pin.OUT) #gpio22

led = Pin(23, Pin.OUT) #gpio23
random_value = None
state = None
# def webpage():
# def webpage(random_value, state):
def webpage(state):   
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pico Web Server</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="icon" href="data:;base64,=">
        </head>
        <body style="background-color: #09e011c5">
            
            <h1 style="text-align: center">Vehicle Immobilizer</h1>
            <h2 style="text-align: center">Lock Botton</h2>
            <div style="text-align: center">
                <form action="./Lock_up">
                    <input type="submit" value="Lock" style="width:240px;height:60px;font-size: 40px"/>
                </form>
            </div>
            <br>
            <div style="text-align: center">
                <form action="./unlock">
                    <input type="submit" value="Unlock" style="width:240px;height:60px;font-size: 40px"/>
                </form>
            </div>
            <h2 style="text-align: center">Lock State: {state}</h2>
            <br>
            <br>
            <p>This is the demo presenting to LOCKDOWN SECURITY </p>
            <p>For more information,please contact Jasper Li:</p>
            <p>Jasperlica@gmail.com</p>
            
        </body>
        </html>
        """
        # html = "Raspberry Pi Pico Web Server"
    return (html)
    #     str1 = headers + html
    # return str(str1)

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

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
        # s.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', 80))
        s.listen(5)
    except OSError as e:
        print(e)
    except:
        print("something wrong with socket?")
        # machine.reset()
        
        # watchdog()
        while(True):
            time.sleep(1)
            print("trapped here")

    while True:
        try:
            conn, addr = s.accept()
            print('Got a connection from %s' % str(addr))
            request_origin = conn.recv(1024)
            print('Content = %s' % str(request_origin))

            try:
                request_byte = request_origin.split()[1]
                print('Request:', request_byte)
            except IndexError:
                pass
        
            # Process the request and update variables
            request = request_byte.decode()
            if request == '/Lock_up?':
                print("Lock up")
                relay.value(1)
                led.value(1)
                state = "Locked"
            elif request == '/unlock?':
                print("Unlock")
                relay.value(0)
                led.value(0)
                state = 'Unlocked'
            # elif request == '/value?':
            #     random_value = random.randint(0, 20)

            # Generate HTML response
            # response = webpage()
           
           # response = webpage(random_value, state)  
            response = webpage(state) 

            # Send the HTTP response and close the connection
            conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            conn.send(response)
            conn.close()

        except OSError as e:
            conn.close()
            print('Connection closed')


if __name__ == "__main__":
    ap_mode('jasperpi', '12345678')
