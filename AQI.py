from datetime import date, timedelta
import sqlite3
import datetime
import LCD
from time import sleep
#from var_dump import var_dump
import AlarmClock.functions as ACFunctions
import threading
applicationpath = "/home/pi/projects/AlarmClock/"


            


def DisplayForecast():
	global applicationpath
        conn = sqlite3.connect(applicationpath+'AIQ.db')
        c = conn.cursor()
        dbQuerya = "SELECT * FROM AQI" #get all the data from the database
        c.execute(dbQuerya)
        rows = c.fetchall()
        conn.close()
        text = ""
	x=0
        for row in rows:

#		print row
#		day =  datetime.datetime.fromtimestamp(row[1]).strftime('%a %d')

		precip = row[1]
		temphi= row[2]
		templo = row[3]
#		precipitation = precip.split('.')
#		temphigh = temphi.split('.')
#		templow = templo.split('.')
#		precipitation = precip.split('.')
		text = "AQI Forecast\n"+  precip[5:10]+" "+temphi+" "+templo
		LCD.lcd.clear()
		LCD.lcd.set_color(1,0,1) 
		LCD.lcd.message(text)

		sleep(2);
#		print row
#		summary = row[2]
#                date = row[0]
#                temperature = str(row[7])
#		temp = temperature.split('.')
#		print temp[0]
#               type = row[8]

#                text = text+ date[5:10]+' '+str(temp[0])+ "F\n"+summary+"\n"
#	print text


#CurrentConditions()
#DisplayForecast()
