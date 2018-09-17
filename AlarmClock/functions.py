import requests
import sqlite3
import datetime
def isset(object,key,secondary=None):
    if (secondary):
        try:
            return object[key][secondary]
        except KeyError:
            return ""
    else:
        
        try:
            return object[key]
        except KeyError:
            return ""
                
applicationpath = "/home/pi/projects/AlarmClock/"

def geolocate():
    global applicationpath
    #we need the Lat and Long for weather, so we can do that first using ipstack.
    f = requests.request('GET', 'http://myip.dnsomatic.com')
    ip = f.text
    #print ip
    r = requests.get('http://api.ipstack.com/'+ip+'?access_key=b0989d6350cb67ee47ab771912b8d123')
    data = r.json()
    #print data['latitude']
    #print data['longitude']
    conn = sqlite3.connect(applicationpath+'Settings.db') #this will create if it doesn't exist
    c = conn.cursor()
    dbQuery1 = "Delete from Settings WHERE Setting='Latitude'";
    c.execute(dbQuery1)
    dbQuery2 = "Delete from Settings WHERE Setting='longitude'";
    c.execute(dbQuery2)
    conn.commit()
    dbQuery3 = "INSERT into Settings ( DateEntered , Setting , Value , Enabled ) VALUES";
    dbQuery3 = dbQuery3 +"('"+str(datetime.datetime.now())+"',"
    dbQuery3 = dbQuery3 +"'Latitude',"
    dbQuery3 = dbQuery3 +"'"+str(data['latitude'])+"',"
    dbQuery3 = dbQuery3 +"'1'"
    dbQuery3 = dbQuery3 +")"
    #print dbQuery3
    c.execute(dbQuery3)
    dbQuery4 = "INSERT into Settings ( DateEntered , Setting , Value , Enabled ) VALUES";
    dbQuery4 = dbQuery4 +"('"+str(datetime.datetime.now())+"',"
    dbQuery4 = dbQuery4 +"'longitude',"
    dbQuery4 = dbQuery4 +"'"+str(data['longitude'])+"',"
    dbQuery4 = dbQuery4 +"'1'"
    dbQuery4 = dbQuery4 +")"
    #print dbQuery4
    c.execute(dbQuery4)
    conn.commit()


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

def setupTables():
    global applicationpath
    conn = sqlite3.connect(applicationpath+'Settings.db') #this will create if it doesn't exist
    c = conn.cursor()
    AIQdb = sqlite3.connect(applicationpath+'AIQ.db') #this will create if it doesn't exist
    AIQc = AIQdb.cursor()
    Weatherdb = sqlite3.connect(applicationpath+'Weather.db') #this will create if it doesn't exist
    Weatherc = Weatherdb.cursor()
    Nagiosconn = sqlite3.connect(applicationpath+'Nagios.db') #this will create if it doesn't exist
    Nagiosc = Nagiosconn.cursor()
    conn = sqlite3.connect(applicationpath+'Settings.db') #this will create if it doesn't exist
    c = conn.cursor()
    if (checkTableExists(conn,'Settings')):
        True
    else:
        c.execute('''CREATE TABLE Settings (DateEntered date, Setting text, Value text, Enabled text)''')
        conn.commit()
    
    if (checkTableExists(Weatherdb,'weatherCurrentconditions')):
        True
    else:
        Weatherc.execute('''CREATE TABLE weatherCurrentconditions (DateEntered date, time text, summary text, icon text, nearestStormDistance text,precipIntensity text,precipProbability text,temperature text,apparentTemperature text,windSpeed text,windGust text,uvIndex text,visibility text)''')
        Weatherdb.commit()
    
    if (checkTableExists(Weatherdb,'weather')):
        True
    else:
        Weatherc.execute('''CREATE TABLE weather (DateEntered date, time int, uvIndex text,windSpeed text,summary text, icon text, sunriseTime text, sunsetTime text,moonPhase text,precipIntensity text, precipIntensityMax text,precipIntensityMaxTime text,precipProbability text,precipType text,temperatureHigh text,temperatureHighTime text,temperatureLow text )''')
        Weatherdb.commit()  
          
    if (checkTableExists(AIQdb,'AQICurrentConditions')):
        True
    else:
        AIQc.execute('''CREATE TABLE AQICurrentConditions (DateEntered date, DateObserved date, HourObserved text, LocalTimeZone text,ReportingArea text,StateCode text,Latitude text,Longitude text,ParameterName text,AQI text,CategoryNumber text, CategoryName text)''')
        AIQdb.commit()    
    
    if (checkTableExists(AIQdb,'AQI')):
        True
    else:
        AIQc.execute('''CREATE TABLE AQI (DateEntered date, ForecastDate date, AQI text, Comments text)''')
        AIQdb.commit()
    
    if (checkTableExists(Nagiosconn,'Nagios')):
        True
    else:
        Nagiosc.execute('''CREATE TABLE Nagios (DateEntered date, Server text, Service text, Status text,State int,UpdatedDate date)''')
        Nagiosconn.commit()
    
