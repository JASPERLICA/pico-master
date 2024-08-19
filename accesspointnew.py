import network
import time
import socket
from machine import Pin,WDT
import _thread
import json
# import random
reset_request = False

relay = Pin(22, Pin.OUT) #gpio22

led = Pin(23, Pin.OUT) #gpio23
random_value = None
state = None
first_page = True
password_dict = {}
# def webpage():
# def webpage(random_value, state): #09e011c5
#Silver
def webpage_1(state):   
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>vehicle main page</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="icon" href="data:;base64,=">
        </head>
        <body style="background-color: #D0ECE7">
            
            <h1 style="text-align: center">Vehicle Immobilizer</h1>
            <h2 style="text-align: center">Lock Botton</h2>
            <div style="text-align: center">
                <form action="./Lock_up">
                    <input type="submit" value="Lock" style="width:240px;height:60px;background-color:#EC7063;font-size: 40px"/>
                </form>
            </div>
            <br>
            <div style="text-align: center">
                <form action="./unlock">
                    <input type="submit" value="Unlock" style="width:240px;height:60px;background-color:#48C9B0;font-size: 40px"/>
                </form>
            </div>
            <br>
            <div style="text-align: center">
                <form action="./setting">
                    <input type="submit" value="Setting" style="width:240px;height:60px;background-color:#EB984E;font-size: 40px"/>
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

def webpage_2(ssid,password,message):   
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>setting page</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="icon" href="data:;base64,=">
        </head>
        <body style="background-color: powderblue">
            
            <h1 style="text-align: center">Account Setting</h1>
            <br>
            <div style="text-align: center; font-size:20px">
                <form method = 'POST' action="./account">
                    Account:<br>
                    <input type="text" value={ssid} name="ssid" style="height:40px;font-size: 20px"/>
                    <br>
                    Password:<br>
                    *At least 8 characters long<br>
                    <input type="password" name="password_1" style="height:40px;font-size: 20px"/>
                    <br>
                    Confirm:<br>
                    <input type="password" name="password_2" style="height:40px;font-size: 20px"/>
                    <br>
                    <h4 style="text-align: center">{message}</h4>
                    
                    <div style="text-align:center">
                    <input type="submit" value="Submit" style="background-color:#D2691E;width:240px;height:60px;font-size:40px"/>
                    </div>
                    <br>
                </form>

                <div style="text-align: center">
                        <form action="./exit">
                            <input type="submit" value="Exit" style="width:240px;height:60px;background-color:Olive;font-size: 40px"/>
                        </form>
                </div>
            </div>

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
    global reset_request
    global first_page,password_dict
    """
        Description: This is a function to activate AP mode

        Parameters:

        ssid[str]: The name of your internet connection
        password[str]: Password for your internet connection

        Returns: Nada
    """
    # Just making our internet connection
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid,authmode=network.AUTH_WPA_WPA2_PSK,password=password)
    ap.active(True)
    

    while ap.active() == False:
        pass
    print('AP Mode Is Active, You can Now Connect')
    print('IP Address To Connect to:: ' + ap.ifconfig()[0])
    # print(ap.status())
    # print(ap.config())
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
        # s.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', 80))
        s.listen(5)
    except OSError as e:
        print(e)
    except:
        print("something wrong with socket and got to reset")
        reset_request = True
        # machine.reset()
        
        # watchdog()
        while(True):

            time.sleep(1)
            print("trapped here")

    first_page = True

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
                first_page = True
            elif request == '/unlock?':
                print("Unlock")
                relay.value(0)
                led.value(0)
                state = 'Unlocked'
                first_page = True

            elif request == '/setting?':
                print("setting")
                # ssid = "1234"
                
                with open("password.json","r+",encoding='utf-8') as f:
                    password_dict = json.load(f)
                    ssid = password_dict["SSID"]
                    print(f"the ssid is {ssid}")

                f.close()
                password = ""
                message= ""
                first_page = False
            
            elif request == '/account':
            # # elif operator.contains(request, "/account?"):
            # elif "/account?" in request:
                print("account")
                request_post = request_origin.decode()
                temp = request_post.split("\r\n\r\n")
                # temp = temp0[1].decode()
                print(temp[1])
                list_of_post_data = temp[1].split('&')
                print(list_of_post_data)
                
                post_data_dict = {}
                for item in list_of_post_data:
                    variable, value = item.split('=')
                    post_data_dict[variable] = value
                    print(f"post_data_dict[variable]:{post_data_dict[variable]},")

                if len(post_data_dict["ssid"]) <= 30 and bool(post_data_dict["ssid"]):
                    if post_data_dict["password_1"] == post_data_dict["password_2"]:
                        if len(post_data_dict["password_1"]) >=8 and len(post_data_dict["password_1"])<= 30 and bool(post_data_dict["password_1"]):

                            password_dict["SSID"]=post_data_dict["ssid"]
                            password_dict["PASSWORD"]=post_data_dict["password_1"]

                            with open("password.json","w", encoding='utf-8') as file:

                                json.dump(password_dict, file)
                                file.flush()
                                file.close()

                            print("Account updated!")
                            message= "Successfully updated! Please go"
                            reset_request = True
                        else:   
                            print("Invalid password!")
                            message= "Invalid password!"
                    else:
                        print("Wrong password!")
                        message= "Wrong password!"
                else:    
                    print("Invaild ssid name")
                    message= "Invaild SSID!"


            elif request == '/exit?':
                print("exit")  
                first_page = True
                

            # elif request == '/value?':
            #     random_value = random.randint(0, 20)

            # Generate HTML response
            # response = webpage()
           
           # response = webpage(random_value, state)  
            if first_page:
                response = webpage_1(state)
            else:
                response = webpage_2(ssid,password,message)

            # Send the HTTP response and close the connection
            conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            conn.send(response)
            conn.close()

        except OSError as e:    

            print(f'Connection closed:{e}')
            reset_request = True
            conn.close()
           

if __name__ == "__main__":

    
    wdt = WDT(timeout = 5000)
    wdt.feed() 
    

    # password_dict = {"SSID":"picowifi3","PASSWORD":"12345678"}

    # with open("password.json","w", encoding='utf-8') as file:

    #     json.dump(password_dict, file)
    #     file.flush()
    #     file.close()

    with open("password.json","r+",encoding='utf-8') as f:
        password_dict = json.load(f)
        wifi_name = password_dict["SSID"]
        wifi_pas = password_dict["PASSWORD"]

        print(f"this is the wifi{wifi_name} and {wifi_pas}")
        f.close()

    _thread.start_new_thread(ap_mode,(wifi_name, wifi_pas))
    # _thread.start_new_thread(ap_mode,('jasperpi', '12345678'))
    while (True):
        time.sleep(2)
        if not reset_request:
            wdt.feed() 
            print("feed watchdog..")
        

    # ap_mode('jasperpi', '12345678')
