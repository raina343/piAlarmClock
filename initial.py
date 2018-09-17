applicationpath = "/home/pi/projects/AlarmClock/"
import sqlite3
import datetime
import nagios
import requests
import AIQ
import AQI
import weather
import weatherforecast
import systeminfo
#from var_dump import var_dump
import AlarmClock.functions as ACFunctions
import DigitalClock
import threading
import time

screen = "none"

def button_callback(channel):
        print("Button was pushed!")
	global screen
	exec('my_func_'+screen+'(1, 2)')
	print screen

def snooze_button_callback(channel):
        print("Snooze Button was pushed!")
	global screen
	exec('snooze_my_func_'+screen+'(1, 2)')
	print screen



def snooze_my_func_nagios(channel,value):
#	nagios.show
	print 'running nagios snooze button function' + str(channel) + ' ' +str(value)
def my_func_nagios(channel,value):
	print 'running nagios button function' + str(channel) + ' ' +str(value)

def my_func_AQI(channel,value):
	print 'running nagios button function' + str(channel) + ' ' +str(value)

def my_func_Weather(channel,value):
	print 'running nagios button function' + str(channel) + ' ' +str(value)



import RPi.GPIO as GPIO
GPIO.setwarnings(False) # Ignore warning for now

GPIO.setmode(GPIO.BCM) # Use physical pin numbering

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

GPIO.add_event_detect(18,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge

GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

GPIO.add_event_detect(25,GPIO.RISING,callback=snooze_button_callback) # Setup event on pin 10 rising edge

#message = input("Press enter to quit\n\n") # Run until someone presses enter

#GPIO.cleanup() # Clean up



#from repeattimer import every
#####Setup the LCD
#import Adafruit_CharLCD as LCD
#import Adafruit_GPIO.MCP230xx as MCP
#gpio = MCP.MCP23017()
#lcd = LCD.Adafruit_RGBCharLCD(0, 1, 2, 3, 4, 5,16, 2, 6, 7, 8,gpio=gpio)
#####################
#GPIO.setmode(GPIO.BCM)
#18
#19
screensections = ["","nagios","AQI","AQIForecast","Weather","weatherforecast","SysInfo"]
ACFunctions.setupTables()
ACFunctions.geolocate()
AIQ.CurrentConditions()
#AIQ.DailyForecast()    
nagios.updatedata()
weather.CurrentConditions()
#nagios.getData()
#print xxx
#if xxx['Color']=="red":
#lcd.clear()
#lcd.set_color(1,1,0) #yellow
#lcd.message(xxx['text'])

#print xxx
#weather.CurrentConditions()
def cyclescreen(value,screensections):
	value = value+1;
#	print 'screen cycle'
#	print value;
	print screensections[value]
	global screen
	screen = screensections[value]

	if (screen=="nagios"):
		nagios.getData()
	if (screen=="AQI"):
		AIQ.DisplayCurrentConditions()
	if (screen=="AQIForecast"):
		AQI.DisplayForecast()
	if (screen=="Weather"):
		weather.DisplayCurrentConditions()
	if (screen=="weatherforecast"):
		weatherforecast.DisplayForecast()
	if (screen=="SysInfo"):
		systeminfo.DisplaySystemInfo()

	if (value==6):
		value=0
	threading.Timer(10.0, cyclescreen,[value,screensections]).start() 


cyclescreen(0,screensections)

DigitalClock.RunClock()
