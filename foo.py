import requests
from requests.auth import HTTPBasicAuth
import sqlite3
import datetime
conn = sqlite3.connect('example2.db') #this will create if it doesn't exist
from var_dump import var_dump

def updatedata(conn):

    c = conn.cursor()
    r = requests.get('http://74.205.92.184/nagios/cgi-bin/statusjson.cgi?query=servicelist&formatoptions=whitespace+enumerate+bitmask+duration&contactname=nagiosadmin', auth=HTTPBasicAuth('nagiosadmin', 'P@$$w0rd22'))

    foo = r.json()

    for xx in foo['data']['servicelist']:
        for yy in foo['data']['servicelist'][xx]:
            dbQuerya = "SELECT count(*) FROM Nagios WHERE Server='"+str(xx)+"' AND Service='"+str(yy)+"'"
            result = c.execute(dbQuerya) 
            values = result.fetchone()
            if values[0]<1:
                dbQuery = "INSERT INTO Nagios (DateEntered , Server , Service , Status,State) VALUES"
                dbQuery = dbQuery +"('"+str(datetime.datetime.now())+"',"
                dbQuery = dbQuery +"'"+str(xx)+"',"
                dbQuery = dbQuery +"'"+str(yy)+"',"
                dbQuery = dbQuery +"'"+foo['data']['servicelist'][xx][yy]+"','0'"
                dbQuery = dbQuery +")"
                c.execute( dbQuery)
                conn.commit()
            else:
                dbQuery = "Update Nagios SET Status='"+foo['data']['servicelist'][xx][yy]+"' WHERE Server='"+str(xx)+"' and Service='"+str(yy)+"'"
                c.execute( dbQuery)
                conn.commit()
           
def getData(conn):
    c = conn.cursor()
    dbQuerya = "SELECT * FROM Nagios"
    c.execute(dbQuerya)
    rows = c.fetchall()
    ServiceData = {}
    ok=0
    warning=0
    critical=0
    ServiceData['OK'] = {}
    ServiceData['Warning'] = {}
    ServiceData['Critical'] = {}
    ServiceData['OK']['total'] = 0;
    ServiceData['Warning']['total'] = 0;
    ServiceData['Critical']['total'] = 0;
    for row in rows:
        if row[3]=='ok':
            if row[1] in ServiceData['OK']:
                True
            else:
                ServiceData['OK'][row[1]] = {};
            ServiceData['OK'][row[1]][row[2]] = 'ok'
            ok=ok+1
            #okdata.append(row[3])
            ServiceData['OK']['total'] = ok
        else:
            if row[3]=='warning':
                if row[1] in ServiceData['Warning']:
                    fooxx = ''
                else:
                    ServiceData['Warning'][row[1]] = {};
                ServiceData['Warning'][row[1]][row[2]] = 'warning'
                warning = warning+1;
                ServiceData['Warning']['total'] = warning
            else:
                if row[1] in ServiceData['Critical']:
                    fooxx = ''
                else:
                    ServiceData['Critical'][row[1]] = {};
                ServiceData['Critical'][row[1]][row[2]] = 'critical'
                critical = critical+1
                ServiceData['Critical']['total'] = critical
    print 'Critical ' + str(ServiceData['Critical']['total'])
    print 'Warning '+ str(ServiceData['Warning']['total'])
    print 'OK '+ str(ServiceData['OK']['total'])
    #var_dump(ServiceData['OK'])




getData(conn)
