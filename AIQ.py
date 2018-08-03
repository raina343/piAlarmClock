import requests
import sqlite3
import datetime
import AlarmClock.functions as ACFunctions
 #this will create if it doesn't exist
import threading

def DailyForecast():
    threading.Timer(86400.0, DailyForecast).start()
    conn = sqlite3.connect('example2.db')
    c = conn.cursor()
    r = requests.get('http://www.airnowapi.org/aq/forecast/zipCode/?format=application/json&zipCode=95630&date=2018-08-01&distance=25&API_KEY=0501E66A-1CEE-4C3B-9609-E6BE34B25EF1')
    data = r.json()
    for xx in data:
        if xx['Category']['Number']>2:
            c.execute("INSERT INTO AQI (DateEntered,ForecastDate,AQI,Comments) VALUES ('"+str(datetime.datetime.now())+"','"+str(ACFunctions.isset(xx,'DateForecast'))+"','"+str(ACFunctions.isset(xx,'AQI'))+"','"+ACFunctions.isset(xx,'Category','Name')+"')")
        else:
            c.execute("INSERT INTO AQI (DateEntered,ForecastDate,AQI) VALUES ('"+str(datetime.datetime.now())+"','"+str(ACFunctions.isset(xx,'DateForecast'))+"','"+str(ACFunctions.isset(xx,'AQI'))+"')")
        
        conn.commit()
        
def CurrentConditions():
    threading.Timer(900.0, CurrentConditions).start()
    conn = sqlite3.connect('example2.db') 
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

CurrentConditions()
DailyForecast()         
        