from darksky import forecast
from datetime import date, timedelta
import sqlite3
import datetime

#from var_dump import var_dump
import AlarmClock.functions as ACFunctions
import threading


def CurrentConditions():
    threading.Timer(900.0, CurrentConditions).start()
    SettingsDB = sqlite3.connect('Settings.db')
    Settingsc = SettingsDB.cursor()
    dbQuerya = "SELECT Value FROM Settings where Setting='Latitude'" #get all the data from the database
    Settingsc.execute(dbQuerya)
    Latitude = Settingsc.fetchone()
    dbQueryb = "SELECT Value FROM Settings where Setting='longitude'" #get all the data from the database
    Settingsc.execute(dbQueryb)
    longitude = Settingsc.fetchone()  
    conn = sqlite3.connect('Weather.db')
    c = conn.cursor()
    c.execute("DELETE FROM weatherCurrentconditions");
    conn.commit()  
    c.execute("DELETE FROM weather");
    conn.commit()
  #  weekday = date.today()
    with forecast('7ea6c4099eb2886d284a35a0d0cf15c4', Latitude[0],longitude[0]) as weather:
        current = weather['currently']
        dbQuery = "INSERT INTO weatherCurrentconditions (DateEntered , time , summary , icon , nearestStormDistance ,precipIntensity ,precipProbability ,temperature , apparentTemperature ,windSpeed ,windGust ,uvIndex ,visibility ) VALUES"
        dbQuery = dbQuery +"('"+str(datetime.datetime.now())+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(current,'time'))+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(current,'summary'))+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(current,'icon'))+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(current,'nearestStormDistance'))+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(current,'precipIntensity'))+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(current,'precipProbability'))+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(current,'temperature'))+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(current,'apparentTemperature'))+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(current,'windSpeed'))+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(current,'windGust'))+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(current,'uvIndex'))+"',"
        dbQuery = dbQuery +"'"+str(ACFunctions.isset(current,'visibility'))+"'"
        dbQuery = dbQuery +")"
        c.execute( dbQuery)
        conn.commit()  
        for day in weather.daily:
            dbQuery2 = "INSERT INTO weather (DateEntered, time, summary , uvIndex,windSpeed,icon , sunriseTime , sunsetTime ,moonPhase ,precipIntensity,precipIntensityMaxTime,precipIntensityMax,precipProbability,precipType,temperatureHigh ,temperatureHighTime ,temperatureLow ) VALUES "
            dbQuery2 = dbQuery2 +"('"+str(datetime.datetime.now())+"',"
            dbQuery2 = dbQuery2 +"'"+str(ACFunctions.isset(day,'time'))+"',"
            dbQuery2 = dbQuery2 +"'"+str(ACFunctions.isset(day,'summary'))+"',"
            dbQuery2 = dbQuery2 +"'"+str(ACFunctions.isset(day,'uvIndex'))+"',"
            dbQuery2 = dbQuery2 +"'"+str(ACFunctions.isset(day,'windSpeed'))+"',"
            dbQuery2 = dbQuery2 +"'"+str(ACFunctions.isset(day,'icon'))+"',"
            dbQuery2 = dbQuery2 +"'"+str(ACFunctions.isset(day,'sunriseTime'))+"',"
            dbQuery2 = dbQuery2 +"'"+str(ACFunctions.isset(day,'sunsetTime'))+"',"
            dbQuery2 = dbQuery2 +"'"+str(ACFunctions.isset(day,'moonPhase'))+"',"
            dbQuery2 = dbQuery2 +"'"+str(ACFunctions.isset(day,'precipIntensity'))+"',"
            dbQuery2 = dbQuery2 +"'"+str(ACFunctions.isset(day,'precipIntensityMax'))+"',"
            dbQuery2 = dbQuery2 +"'"+str(ACFunctions.isset(day,'precipIntensityMaxTime'))+"',"
            dbQuery2 = dbQuery2 +"'"+str(ACFunctions.isset(day,'precipProbability'))+"',"
            dbQuery2 = dbQuery2 +"'"+str(ACFunctions.isset(day,'precipType'))+"',"
            dbQuery2 = dbQuery2 +"'"+str(ACFunctions.isset(day,'temperatureHigh'))+"',"
            dbQuery2 = dbQuery2 +"'"+str(ACFunctions.isset(day,'temperatureHighTime'))+"',"
            dbQuery2 = dbQuery2 +"'"+str(ACFunctions.isset(day,'temperatureLow'))+"'"
            dbQuery2 = dbQuery2 +")"
            c.execute( dbQuery2)
            conn.commit()  
            
CurrentConditions()