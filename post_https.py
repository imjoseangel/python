import urllib2
import urllib

url = 'https://10.100.20.94/Sourcing/inspector'
username = 'debug'
password = 'gr1t4nd0_L1br3*'

p = urllib2.HTTPPasswordMgrWithDefaultRealm()

p.add_password(None, url, username, password)

handler = urllib2.HTTPBasicAuthHandler(p)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)

urlaql = 'https://10.100.20.94/Sourcing/inspector/aql'

post_data = {'restrictQueryBy': 'None', 'query': 'SELECT this, Dataloads.TimeScheduled, Name, Dataloads.TimeStarted,Dataloads.TimeCompleted, Dataloads.NodeName FROM ariba.analytics.server.DataloadSchedule include inactive ORDER BY Dataloads.TimeStarted desc,Dataloads.TimeScheduled desc', 'partitionNames': 'Any', 'acrossCommunities': 'off', 'baseDomainVariant': 'off', 'joinType': 3, 'maxRecords': 500, 'userLocale': 'English', 'userPartition': 'Any', 'submit': 'Submit'}

headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'POST': '/Sourcing/inspector/aql HTTP/1.1', 'Host': '10.100.20.94', 'Connection': 'keep-alive'}

data = urllib.urlencode(post_data)
req = urllib2.Request(urlaql, data, headers)
response = urllib2.urlopen(req)
query = response.read()

print query
