import datetime
import AlarmClock.functions as ACFunctions
import threading
import LCD
import platform
applicationpath = "/home/pi/projects/AlarmClock/"
import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


#print get_ip();
from datetime import timedelta

with open('/proc/uptime', 'r') as f:
	uptime_seconds = float(f.readline().split()[0])
	uptime_string = str(timedelta(seconds = uptime_seconds))

#print(uptime_string)



def DisplaySystemInfo():
        text = ""
        date = uptime_string
        type = get_ip()
        text = "IP:"+type+"\n"+"Uptime:"+date
        LCD.lcd.clear()
        LCD.lcd.set_color(0,0,1) #blue

        LCD.lcd.message(text)

#DisplaySystemInfo()
