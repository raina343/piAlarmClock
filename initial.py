import sqlite3
import datetime
conn = sqlite3.connect('example2.db') #this will create if it doesn't exist
c = conn.cursor()



def checkTableExists(dbcon, tablename):
    c = dbcon.cursor()
    try:
        c.execute("SELECT 1 FROM "+tablename+" LIMIT 1;")
        exists = True
        return True
    except sqlite3.OperationalError as e:
            message = e.args[0]
            if message.startswith("no such table"):
               # print("Table "+tablename+" does not exist")
                return False
                #exists = False
            else:
                raise

if (checkTableExists(conn,'weatherCurrentconditions')):
    True
else:
    c.execute('''CREATE TABLE weatherCurrentconditions (DateEntered date, time text, summary text, icon text, nearestStormDistance text,precipIntensity text,precipProbability text,temperature text,apparentTemperature text,windSpeed text,windGust text,uvIndex text,visibility text)''')
    conn.commit()
    
if (checkTableExists(conn,'weather')):
    True
else:
    c.execute('''CREATE TABLE weather (DateEntered date, time int, uvIndex text,windSpeed text,summary text, icon text, sunriseTime text, sunsetTime text,moonPhase text,precipIntensity text, precipIntensityMax text,precipIntensityMaxTime text,precipProbability text,precipType text,temperatureHigh text,temperatureHighTime text,temperatureLow text )''')
    conn.commit()    
if (checkTableExists(conn,'AQICurrentConditions')):
    True
else:
    c.execute('''CREATE TABLE AQICurrentConditions (DateEntered date, DateObserved date, HourObserved text, LocalTimeZone text,ReportingArea text,StateCode text,Latitude text,Longitude text,ParameterName text,AQI text,CategoryNumber text, CategoryName text)''')
    conn.commit()    
    
if (checkTableExists(conn,'AQI')):
    True
#    c.execute("INSERT INTO AQI VALUES ('"+datetime.datetime.now()+"','BUY','RHATddd',100,35.14)")
#    conn.commit()
else:
    c.execute('''CREATE TABLE AQI (DateEntered date, ForecastDate date, AQI text, Comments text)''')
    conn.commit()
    
if (checkTableExists(conn,'Nagios')):
    c.execute("INSERT INTO Nagios VALUES ('2006-01-05','BUY','RHATddd',100,35.14)")
    conn.commit()
else:
    c.execute('''CREATE TABLE Nagios (DateEntered date, Server text, Service text, Status text,State int)''')
    conn.commit()
    


