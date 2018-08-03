import sqlite3
import datetime
import nagios
import requests
import AIQ
import weather
from var_dump import var_dump
import AlarmClock.functions as ACFunctions
#####Setup the LCD
#import Adafruit_CharLCD as LCD
#import Adafruit_GPIO.MCP230xx as MCP
#gpio = MCP.MCP23017()
#lcd = LCD.Adafruit_RGBCharLCD(0, 1, 2, 3, 4, 5,16, 2, 6, 7, 8,gpio=gpio)
#####################


ACFunctions.setupTables()
ACFunctions.geolocate()
#lcd.message('Hello\nworld!')
#lcd.set_backlight(0)
#AIQ.CurrentConditions()
#AIQ.DailyForecast()    
nagios.updatedata()
xxx= nagios.getData()
print xxx
#weather.CurrentConditions()