from darksky import forecast
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
        conn = sqlite3.connect(applicationpath+'Weather.db')
        c = conn.cursor()
        dbQuerya = "SELECT * FROM weather" #get all the data from the database
        c.execute(dbQuerya)
        rows = c.fetchall()
        conn.close()
        text = ""
        for row in rows:
#		print row
		day =  datetime.datetime.fromtimestamp(row[1]).strftime('%a %d')

		precip = row[12]
		temphi= row[14]
		templo = row[16]
		precipitation = precip.split('.')
		temphigh = temphi.split('.')
		templow = templo.split('.')
		precipitation = precip.split('.')
		text =  day +" "+str(temphigh[0])+"/"+str(templow[0])+"F"+ " "+str(precipitation[0])+"%\n"+row[4]
		LCD.lcd.clear()
		LCD.lcd.set_color(1,1,0) #yellow
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
