import requests
from requests.auth import HTTPBasicAuth
import sqlite3
import datetime
from var_dump import var_dump
import threading

def updatedata():
    #this is for getting data from the web
    threading.Timer(180.0, updatedata).start() #every 3 minutes we will run this function.  it will also run first when this script is first executed.
    conn = sqlite3.connect('example2.db') #open db file.
    c = conn.cursor()
    r = requests.get('http://74.205.92.184/nagios/cgi-bin/statusjson.cgi?query=servicelist&formatoptions=whitespace+enumerate+bitmask+duration&contactname=nagiosadmin', auth=HTTPBasicAuth('nagiosadmin', 'P@$$w0rd22')) #ge the data from Nagios
    NagiosData = r.json() #parse the json
    now = datetime.datetime.now() #get a current timestamp, so all updates and inserts show the same time.
    for xx in NagiosData['data']['servicelist']: #itterate through the returned data.
        for yy in NagiosData['data']['servicelist'][xx]:
            dbQuerya = "SELECT count(*) FROM Nagios WHERE Server='"+str(xx)+"' AND Service='"+str(yy)+"'" #check to see if the current entry exists already in the database
            result = c.execute(dbQuerya) 
            values = result.fetchone()
            if values[0]<1: #the specified entry doesn't exist already so we'll write a new entry
                dbQuery = "INSERT INTO Nagios (DateEntered , UpdatedDate, Server , Service , Status,State) VALUES"
                dbQuery = dbQuery +"('"+str(now)+"',"
                dbQuery = dbQuery +"'"+str(now)+"',"
                dbQuery = dbQuery +"'"+str(xx)+"',"
                dbQuery = dbQuery +"'"+str(yy)+"',"
                dbQuery = dbQuery +"'"+NagiosData['data']['servicelist'][xx][yy]+"',"
                dbQuery = dbQuery +"'0'"
                dbQuery = dbQuery +")"
                c.execute( dbQuery)
                conn.commit() #write the query to the database
            else: #the specified entry does exist, so now we'll just modify the statuses
                if NagiosData['data']['servicelist'][xx][yy]=='ok': #if the status is ok, we'll reset the state flag, and update the status, and UpdatedDate
                    dbQuery = "Update Nagios SET UpdatedDate='"+str(now)+"', State='0', Status='"+NagiosData['data']['servicelist'][xx][yy]+"' WHERE Server='"+str(xx)+"' and Service='"+str(yy)+"'"
                else: #The Status is not ok, so we don't reset the state flag but do update the status and updateddate
                    dbQuery = "Update Nagios SET UpdatedDate='"+str(now)+"', Status='"+NagiosData['data']['servicelist'][xx][yy]+"' WHERE Server='"+str(xx)+"' and Service='"+str(yy)+"'"
                c.execute( dbQuery)
                conn.commit()
           
def getData():
    #this is what will return the data from the database and update the display
    threading.Timer(60.0, getData).start() #runs every 60 seconds
    conn = sqlite3.connect('example2.db')
    c = conn.cursor()
    dbQuerya = "SELECT * FROM Nagios" #get all the data from the database
    c.execute(dbQuerya)
    rows = c.fetchall()
    ServiceData = {}
    ok=0
    warning=0
    critical=0
    RedAlarm=0;
    YellowAlarm=0
 
    YellowScreen=0
    RedScreen=0

    Alarm = 'None'
    ScreenColour='None'
    ServiceData['OK'] = {}
    ServiceData['Warning'] = {}
    ServiceData['Critical'] = {}
    ServiceData['OK']['total'] = 0;
    ServiceData['Warning']['total'] = 0;
    ServiceData['Critical']['total'] = 0;
    #var_dump(rows)
    for row in rows: #do some very convoluted stuff to figure out what colours to set the display and if to sound an alarm.
        if row[3]=='ok':
            if row[1] in ServiceData['OK']:
                True
            else:
                ServiceData['OK'][row[1]] = {};
            ServiceData['OK'][row[1]][row[2]] = row[4]
            ok=ok+1
            ServiceData['OK']['total'] = ok
        else:
            if row[3]=='warning':
                if row[1] in ServiceData['Warning']:
                    True
                else:
                    ServiceData['Warning'][row[1]] = {};
                if row[4]>0:
                    YellowScreen=1
                else:
                    YellowScreen=1
                    YellowAlarm=YellowAlarm+1
                ServiceData['Warning'][row[1]][row[2]] = row[4]
                warning = warning+1;
                ServiceData['Warning']['total'] = warning
            else:
                if row[1] in ServiceData['Critical']:
                    True
                else:
                    ServiceData['Critical'][row[1]] = {};
                if row[4]>0:
                    RedScreen=1
                else:
                    RedScreen=1
                    RedAlarm=RedAlarm+1
                ServiceData['Critical'][row[1]][row[2]] = row[4]
                critical = critical+1
                ServiceData['Critical']['total'] = critical
    print datetime.datetime.now()
    print 'Critical ' + str(ServiceData['Critical']['total'])
    print 'Warning '+ str(ServiceData['Warning']['total'])
    print 'OK '+ str(ServiceData['OK']['total'])

    if (RedAlarm==1 and YellowAlarm==1):
        Alarm='orange'
    if (RedAlarm==1 and YellowAlarm==0):
        Alarm='red'
    if (RedAlarm==0 and YellowAlarm==1):
        Alarm='yellow'
    if (RedAlarm==0 and YellowAlarm==0):
        Alarm='none'
    if (RedScreen==1 and YellowScreen==1):
        ScreenColour='orange'
    if (RedScreen==1 and YellowScreen==0):
        ScreenColour='red'
    if (RedScreen==0 and YellowScreen==1):
        ScreenColour='yellow'
    if (RedScreen==0 and YellowScreen==0):
        ScreenColour='none'
    
    print 'Screen='+ ScreenColour
    print 'Alarm='+ Alarm

updatedata()
getData()