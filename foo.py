import requests
from requests.auth import HTTPBasicAuth
r = requests.get('http://74.205.92.184/nagios/cgi-bin/statusjson.cgi?query=servicelist&formatoptions=whitespace+enumerate+bitmask+duration&contactname=nagiosadmin', auth=HTTPBasicAuth('nagiosadmin', 'P@$$w0rd22'))
ServiceData = {}
foo = r.json()
#print foo
#exit
ok=0
warning=0
critical=0
okdata = [];
warningdata = [];
criticaldata = [];
ServiceData['OK'] = {}
ServiceData['Warning'] = {}
ServiceData['Critical'] = {}
ServiceData['OK']['total'] = 0;
ServiceData['Warning']['total'] = 0;
ServiceData['Critical']['total'] = 0;
for xx in foo['data']['servicelist']:
    for yy in foo['data']['servicelist'][xx]:
        if foo['data']['servicelist'][xx][yy]=='ok':
            if xx in ServiceData['OK']:
                fooxx = ''
            else:                
                ServiceData['OK'][xx] = {};
            ServiceData['OK'][xx][yy] = 'ok'
            ok=ok+1
            okdata.append(yy)
            ServiceData['OK']['total'] = ok
        else:
            if foo['data']['servicelist'][xx][yy]=='warning':
                if xx in ServiceData['Warning']:
                    fooxx = ''
                else:
                    ServiceData['Warning'][xx] = {};
                ServiceData['Warning'][xx][yy] = 'warning'
                warning = warning+1;
                ServiceData['Warning']['total'] = warning
            else:
                if xx in ServiceData['Critical']:
                    fooxx = ''
                else:
                    ServiceData['Critical'][xx] = {};
                ServiceData['Critical'][xx][yy] = 'critical'
                critical = critical+1
                ServiceData['Critical']['total'] = critical
# print ServiceData
print 'Critical ' + str(ServiceData['Critical']['total'])
print 'Warning '+ str(ServiceData['Warning']['total'])
print 'OK '+ str(ServiceData['OK']['total'])