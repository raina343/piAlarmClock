from darksky import forecast
from datetime import date, timedelta
import sqlite3
import datetime
conn = sqlite3.connect('example2.db') #this will create if it doesn't exist


#BOSTON = 38.6767, -121.1461


def CurrentConditions(conn,lat,long):
   
    conn.commit()
    c = conn.cursor()
    c.execute("DELETE FROM weatherCurrentconditions");
    conn.commit()  
    c.execute("DELETE FROM weather");
    conn.commit()  
    weekday = date.today()
    with forecast('7ea6c4099eb2886d284a35a0d0cf15c4', lat,long) as weather:
        current = weather['currently']
        dbQuery = "INSERT INTO weatherCurrentconditions (DateEntered , time , summary , icon , nearestStormDistance ,precipIntensity ,precipProbability ,temperature , apparentTemperature ,windSpeed ,windGust ,uvIndex ,visibility ) VALUES"
        dbQuery = dbQuery +"('"+str(datetime.datetime.now())+"',"
        dbQuery = dbQuery +"'"+str(current['time'])+"',"
        dbQuery = dbQuery +"'"+str(current['summary'])+"',"
        dbQuery = dbQuery +"'"+str(current['icon'])+"',"
        dbQuery = dbQuery +"'"+str(current['nearestStormDistance'])+"',"
        dbQuery = dbQuery +"'"+str(current['precipIntensity'])+"',"
        dbQuery = dbQuery +"'"+str(current['precipProbability'])+"',"
        dbQuery = dbQuery +"'"+str(current['temperature'])+"',"
        dbQuery = dbQuery +"'"+str(current['apparentTemperature'])+"',"
        dbQuery = dbQuery +"'"+str(current['windSpeed'])+"',"
        dbQuery = dbQuery +"'"+str(current['windGust'])+"',"
        dbQuery = dbQuery +"'"+str(current['uvIndex'])+"',"
        dbQuery = dbQuery +"'"+str(current['visibility'])+"'"
        dbQuery = dbQuery +")"
        c.execute( dbQuery)
        conn.commit()  
        for day in weather.daily:
            print str(day)
            dbQuery2 = "INSERT INTO weather (DateEntered, summary , icon , sunriseTime , sunsetTime ,moonPhase ,precipIntensity,precipIntensityMax,precipProbability,precipType,temperatureHigh ,temperatureHighTime ,temperatureLow ) VALUES "
            #  ,  ) VALUES "
            dbQuery2 = dbQuery2 +"('"+str(datetime.datetime.now())+"',"
            dbQuery2 = dbQuery2 +"'"+str(day['summary'])+"',"
            dbQuery2 = dbQuery2 +"'"+str(day['icon'])+"',"
            dbQuery2 = dbQuery2 +"'"+str(day['sunriseTime'])+"',"
            dbQuery2 = dbQuery2 +"'"+str(day['sunsetTime'])+"',"
            dbQuery2 = dbQuery2 +"'"+str(day['moonPhase'])+"',"
            dbQuery2 = dbQuery2 +"'"+str(day['precipIntensity'])+"',"
            dbQuery2 = dbQuery2 +"'"+str(day['precipIntensityMax'])+"',"
            #dbQuery2 = dbQuery2 +"'"+str(day['precipIntensityMaxTime'])+"'"
            dbQuery2 = dbQuery2 +"'"+str(day['precipProbability'])+"',"
            dbQuery2 = dbQuery2 +"'"+str(day['precipType'])+"',"
            dbQuery2 = dbQuery2 +"'"+str(day['temperatureHigh'])+"',"
            dbQuery2 = dbQuery2 +"'"+str(day['temperatureHighTime'])+"',"
            dbQuery2 = dbQuery2 +"'"+str(day['temperatureLow'])+"'"
            dbQuery2 = dbQuery2 +")"
            c.execute( dbQuery2)
            conn.commit()  
            
foo = CurrentConditions(conn,"38.6767", "-121.1461")