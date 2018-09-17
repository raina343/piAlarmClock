import requests
import sqlite3
import datetime
import AlarmClock.functions as ACFunctions
import threading
import LCD
applicationpath = "/home/pi/projects/AlarmClock/"

def DailyForecast():
    threading.Timer(86400.0, DailyForecast).start()
    global applicationpath
    f = open(applicationpath+"application.log", "a")
    f.write("----------------------------------\n"+str(datetime.datetime.now())+"\nAQI Daily Forecase Updated\n-------------------------------------------")


    conn = sqlite3.connect(applicationpath+'AIQ.db')
    c = conn.cursor()
    c.execute("DELETE FROM AQI");
    conn.commit()
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    r = requests.get('http://www.airnowapi.org/aq/forecast/zipCode/?format=application/json&zipCode=95630&date='+today+'&distance=25&API_KEY=0501E66A-1CEE-4C3B-9609-E6BE34B25EF1')
    data = r.json()
    for xx in data:
#	print xx
#        if xx['Category']['Number']>2:
	c.execute("INSERT INTO AQI (DateEntered,ForecastDate,AQI,Comments) VALUES ('"+str(datetime.datetime.now())+"','"+str(ACFunctions.isset(xx,'DateForecast'))+"','"+str(ACFunctions.isset(xx,'AQI'))+"','"+ACFunctions.isset(xx,'Category','Name')+"')")
#        else:
#	c.execute("INSERT INTO AQI (DateEntered,ForecastDate,AQI) VALUES ('"+str(datetime.datetime.now())+"','"+str(ACFunctions.isset(xx,'DateForecast'))+"','"+str(ACFunctions.isset(xx,'AQI'))+"')")
        
        conn.commit()
        
def CurrentConditions():
    threading.Timer(900.0, CurrentConditions).start()
    f = open("application.log", "a")
    f.write("----------------------------------\n"+str(datetime.datetime.now())+"\nAQI Current Conditions Updated\n-------------------------------------------")
    global applicationpath
    conn = sqlite3.connect(applicationpath+'AIQ.db') 
    c = conn.cursor()
    r = requests.get('http://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=95630&distance=25&API_KEY=0501E66A-1CEE-4C3B-9609-E6BE34B25EF1')
    c.execute("DELETE FROM AQICurrentConditions");
    conn.commit()
    data = r.json()   
    for yy in data: 
        dbQuery = "INSERT INTO AQICurrentConditions  (DateEntered, DateObserved, HourObserved, LocalTimeZone,ReportingArea,StateCode,Latitude,Longitude,ParameterName,AQI,CategoryNumber, CategoryName) VALUES "
        dbQuery = dbQuery +"('"+str(datetime.datetime.now())+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(yy,'DateObserved'))+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(yy,'HourObserved'))+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(yy,'LocalTimeZone'))+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(yy,'ReportingArea'))+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(yy,'StateCode'))+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(yy,'Latitude'))+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(yy,'Longitude'))+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(yy,'ParameterName'))+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(yy,'AQI'))+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(yy,'Category','Number'))+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(yy,'Category','Name'))+"'"
        dbQuery = dbQuery +")"
        c.execute( dbQuery)
        conn.commit()   

def DisplayCurrentConditions():
	global applicationpath

	conn = sqlite3.connect(applicationpath+'AIQ.db')
	c = conn.cursor()
	dbQuerya = "SELECT * FROM AQICurrentConditions" #get all the data from the database
	c.execute(dbQuerya)
	rows = c.fetchall()
	conn.close()
	text = ""
	for row in rows:
		date = row[1]
		type = row[8]
		text = text+ date[5:]+''+type[:2]+ ' '+row[9]+ ' '+row[11]+"\n"
	LCD.lcd.clear()
        LCD.lcd.set_color(1,0,1) #purple

	LCD.lcd.message(text)

#	text = 'T: '+str(grandtotal)+' / C:' + str(ServiceData['Critical']['total'])+' \nW: '+ str(ServiceData['Warning']['total'])+' / OK: '+ str(ServiceData['OK']['total'])
#DisplayCurrentConditions()
#CurrentConditions()
#DailyForecast()         
        
