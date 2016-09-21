#! /usr/bin/python

"""
The script is used to query yy online stream

./yyonline.py [starttime] [endtime]
"""

# import
import sys
import os
import pexpect
import time
import re
import simplejson as json
import urllib2 
from datetime import datetime

# Define glboal parameter
user_name = 'root'
user_password = '123456'
prompt = 'root@'

# Get the base stream
def getBaseStream(queryUrl=None, starttime=None, endtime=None, domains=None):

    print '*******baseStream************'
    print domains
    baseUrl = '''curl -i -d "[{\\"method\\":\\"StreamBaseSearch\\",\\"version\\":\\"2\\",\\"domains\\":%s, \\"startTime\\":\\"%s\\", \\"endTime\\":\\"%s\\"}]" "%s"''' % (re.sub('(?sm)"', r'\\"', str(domains)), starttime, endtime, queryUrl)
    print baseUrl
    print '*****************************' 
    finalStreams = []

    data = [{
        'method': "StreamBaseSearch",
        'version': '2',
        'domains': domains,
        'startTime': starttime,
        'endTime':endtime,
    }]

    req = urllib2.Request(queryUrl)
    req.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(req, json.dumps(data))

    allStreams = response.readlines()

    result = re.findall('(?sm)"publishUrl":"(.*?)"', str(allStreams))

    finalStreams = re.sub('\\\\', '', str(result))
    print 'finalStreams:', finalStreams
    return finalStreams

# Get the domain stream
def getDomainStream(starttime=None, endtime=None, domain=None, queryUrl=None):

    print '*******domainStream***********'
    domainUrl = '''curl -i -d "[{\\"interval\\":\\"5\\",\\"method\\":\\"DomainStatusSearch\\",\\"version\\":\\"2\\",\\"type\\":0, \\"protocols\\":[1,2,3,4,5],\\"domains\\":[\\"%s\\"], \\"startTime\\":\\"%s\\", \\"endTime\\":\\"%s\\"}]" "%s"''' % (domain, starttime, endtime, queryUrl)
    print domainUrl
    print '******************************'

    data = [{
        'method': "DomainStatusSearch",
        'version': '2',
        'interval': '5',
        'type': 0,
        'protocols': [1,2,3,4,5],
        'domains': [domain],
        'startTime': starttime,
        'endTime':endtime,
    }]  
    
    req = urllib2.Request(queryUrl)
    req.add_header('Content-Type', 'application/json')
    
    response = urllib2.urlopen(req, json.dumps(data))
    
    allStreams = response.readlines()[0]
    
    print 'aaaaaa'
    domains = eval(allStreams)[0]
    print json.dumps(domains,indent=2)
    print 'bbbbbb'
    
    return allStreams


# Get the stream status
def getStreamStatus(starttime=None, endtime=None, stream=None, queryUrl=None):

    print '*******StreamStatus***********'
    streamUrl = '''curl -i -d "[{\\"interval\\":\\"5\\",\\"method\\":\\"StreamStatusSearch\\",\\"version\\":\\"2\\",\\"type\\":0, \\"protocols\\":[1,2,3,4,5],\\"urls\\":[\\%s\\"], \\"startTime\\":\\"%s\\", \\"endTime\\":\\"%s\\"}]" "%s"''' % (stream, starttime, endtime, queryUrl)

    print streamUrl
    print '******************************'

    data = [{
        'method': "StreamStatusSearch",
        'version': '2',
        'interval': '5',
        'type': 0,
        'protocols': [1,2,3,4,5],
        'urls': [stream],
        'startTime': starttime,
        'endTime':endtime,
    }]
    
    req = urllib2.Request('http://192.168.32.220:8081/qk_dw?cchost_tag=newisscenter')
    req.add_header('Content-Type', 'application/json')
    
    response = urllib2.urlopen(req, json.dumps(data))
    
    allStreams = response.readlines()[0]
    
    print 'cccccc'
    streams = eval(allStreams)[0]
    print json.dumps(streams,indent=2)
    print 'dddddd'
    
    return allStreams

# date to timestamp
def totimestampNew(dt, epoch=datetime(1970,1,1)):

    '''
    The script can be run at Python2.4
    '''
    tmpList = dt.split(",")
    if len(tmpList) == 5:
        year,month,day,hour,minute = tmpList
        second = 0
    else:
        year,month,day,hour,minute,second = tmpList
    dt = datetime(int(year),int(month),int(day),int(hour),int(minute),int(second))

    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10.0**6 - 60*60*8

# Usage
def exit_with_usage():
    print globals()['__doc__']
    os._exit(1)

# Entrance
print 'You entered: ', len(sys.argv), 'arguments...'
print 'they are: ', str(sys.argv)

localUrl = "http://192.168.32.220:8081/qk_dw?cchost_tag=newisscenter"
localDomain = ["newissupper","newnewupper"]

remoteUrl = "http://42.62.25.32/portal_interface?cchost_tag=sms.information.center"
remoteDomain = ["chinacache.upstream.yy.com"]

if len(sys.argv) == 1:
    
    queryUrl = localUrl
    pridomains = localDomain

    print 'Without specify starttime and endtime, starttime=now-360, endtime=now+360'
    currentTs = str(time.time()).split('.')[0]
    print 'currentTs:', currentTs
    starttime = int(currentTs) - 2400
    endtime = int(currentTs) + 2400 - 100

elif len(sys.argv) == 3:

    queryUrl = localUrl
    pridomains = localDomain

    starttime = sys.argv[1]
    endtime = sys.argv[2]
    if re.search(',', starttime):
        starttime = totimestampNew(starttime)
        endtime = totimestampNew(endtime)

elif len(sys.argv) == 4:

    starttime = sys.argv[1]
    endtime = sys.argv[2]
    type = sys.argv[3]

    if int(type) == 0:
   
        queryUrl = localUrl
        pridomains = localDomain

    else:
        queryUrl = remoteUrl
        pridomains = remoteDomain

    if re.search(',', starttime):
        starttime = totimestampNew(starttime)
        endtime = totimestampNew(endtime)

if True:
    print '==============Base stream'
    streams = getBaseStream(queryUrl, starttime,endtime, pridomains)    
    if not re.search('rtmp', streams):
        print 'No streams!'
        sys.exit(0)

    print '==============Domain stream'
    domains = []
    for stream in eval(streams):
        temp = re.split('/', stream)
        domain = temp[2]        
        domain_streams = getDomainStream(starttime,endtime,domain,queryUrl)

    print '==============Stream status'
    for stream in eval(streams):
        getStreamStatus(starttime,endtime,stream,queryUrl)

