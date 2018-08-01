import requests
import sqlite3
import datetime
conn = sqlite3.connect('example2.db') #this will create if it doesn't exist


def DailyForecast(conn):
    c = conn.cursor()
    r = requests.get('http://www.airnowapi.org/aq/forecast/zipCode/?format=application/json&zipCode=95630&date=2018-08-01&distance=25&API_KEY=0501E66A-1CEE-4C3B-9609-E6BE34B25EF1')
    data = r.json()
    for xx in data:
        if xx['Category']['Number']>2:
            c.execute("INSERT INTO AQI (DateEntered,ForecastDate,AQI,Comments) VALUES ('"+str(datetime.datetime.now())+"','"+str(xx['DateForecast'])+"','"+str(xx['AQI'])+"','"+xx['Category']['Name']+"')")
        else:
            c.execute("INSERT INTO AQI (DateEntered,ForecastDate,AQI) VALUES ('"+str(datetime.datetime.now())+"','"+str(xx['DateForecast'])+"','"+str(xx['AQI'])+"')")
        
        conn.commit()
        
def CurrentConditions(conn):
    c = conn.cursor()
    r = requests.get('http://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=95630&distance=25&API_KEY=0501E66A-1CEE-4C3B-9609-E6BE34B25EF1')
    c.execute("DELETE FROM AQICurrentConditions");
    conn.commit()
    data = r.json()   
    for yy in data: 
        dbQuery = "INSERT INTO AQICurrentConditions  (DateEntered, DateObserved, HourObserved, LocalTimeZone,ReportingArea,StateCode,Latitude,Longitude,ParameterName,AQI,CategoryNumber, CategoryName) VALUES "
        dbQuery = dbQuery +"('"+str(datetime.datetime.now())+"',"
        dbQuery = dbQuery +"'"+str(yy['DateObserved'])+"',"
        dbQuery = dbQuery +"'"+str(yy['HourObserved'])+"',"
        dbQuery = dbQuery +"'"+str(yy['LocalTimeZone'])+"',"
        dbQuery = dbQuery +"'"+str(yy['ReportingArea'])+"',"
        dbQuery = dbQuery +"'"+str(yy['StateCode'])+"',"
        dbQuery = dbQuery +"'"+str(yy['Latitude'])+"',"
        dbQuery = dbQuery +"'"+str(yy['Longitude'])+"',"
        dbQuery = dbQuery +"'"+str(yy['ParameterName'])+"',"
        dbQuery = dbQuery +"'"+str(yy['AQI'])+"',"
        dbQuery = dbQuery +"'"+str(yy['Category']['Number'])+"',"
        dbQuery = dbQuery +"'"+str(yy['Category']['Name'])+"'"
        dbQuery = dbQuery +")"
        c.execute( dbQuery)
        conn.commit()   

foo = CurrentConditions(conn)         
        