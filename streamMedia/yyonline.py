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
def getBaseStream(starttime=None, endtime=None):

    finalStreams = []

    data = [{
        'method': "StreamBaseSearch",
        'version': '2',
        'domains': ["chinacache.upstream.yy.com"],
        'startTime': starttime,
        'endTime':endtime,
    }]

    req = urllib2.Request('http://42.62.25.32/portal_interface?cchost_tag=sms.information.center')
    req.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(req, json.dumps(data))

    allStreams = response.readlines()[0]

    print '1111111'
    a = eval(allStreams)[0]
    print json.dumps(a,indent=2)
    print '2222222'

    result = re.findall('(?sm)"publishUrl":"(.*?)"', str(allStreams))

    finalStreams = re.sub('\\\\', '', str(result))
    print 'finalStreams:', finalStreams
    return finalStreams

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

# Server login
def server_ssh_login(server_ip=None, user_name=None, user_password=None):

    child = pexpect.spawn('ssh %s' % (server_ip))
    child.logfile = sys.stdout

    while True:
        try:
            i = child.expect([pexpect.TIMEOUT, '#', 'yes/no', 'assword:'], timeout=60)
            if i == 0:
                print 'Server login in timeout!'
                return None
            elif i == 1:
                child.sendline('')
                break
            elif i == 2:
                child.sendline('yes')
            else:
                child.sendline('%s' % user_password)
        except:
            print '%s can not login.' % server_ip
            return None

    child.expect(prompt)
    child.expect('.*')
    return child

# Excute send and expect
def excute_send_expect(child=None, commands=None, exp_prompt='root@', type=None, starttime=None, endtime=None, streams=None):

    print 'starttime:', starttime
    print 'endtime:', endtime
    print '....streams:', streams

    for stream in eval(streams):
        print 'stream:', stream

    command_basic = [
      '''curl -i -d "[{\\"method\\":\\"StreamBaseSearch\\",\\"version\\":\\"2\\",\\"domains\\":[\\"chinacache.upstream.yy.com\\"], \\"startTime\\":\\"%s\\", \\"endTime\\":\\"%s\\"}]" "http://42.62.25.32/portal_interface?cchost_tag=sms.information.center"''' % (starttime, endtime),
    ]

    command_status = [
      '''curl -i -d "[{\\"interval\\":\\"1\\",\\"method\\":\\"StreamStatusSearch\\",\\"version\\":\\"2\\",\\"type\\":0, \\"protocols\\":[1,2,3,4,5],\\"urls\\":[\\111\\"], \\"startTime\\":\\"%s\\", \\"endTime\\":\\"%s\\"}]" "http://42.62.25.32/portal_interface?cchost_tag=sms.information.center"''' % (starttime, endtime),
    ]

    command_domain = [
      '''curl -i -d "[{\\"interval\\":\\"1\\",\\"method\\":\\"DomainStatusSearch\\",\\"version\\":\\"2\\",\\"type\\":0, \\"protocols\\":[1,2,3,4,5],\\"domains\\":[\\"chinacache.upstream.yy.com\\"], \\"startTime\\":\\"%s\\", \\"endTime\\":\\"%s\\"}]" "http://42.62.25.32/portal_interface?cchost_tag=sms.information.center"''' % (starttime, endtime)
    ]

    print '.................'
    print command_basic
    print command_status
    print command_domain
    print '.................'
    print ':::Stream baisc search'
    for command in command_basic:
        child.sendline ('%s' % command)
        i = child.expect(['(\[\[\{.*)root@','(\[\[\{.*\}\]\])','\[?\[\]\]?', '500 Internal Server Error'])
        if i == 0 or i == 1:
            result = child.match.group(1)
            result = re.sub(r"(?m)(\r\n\[)", "", result)
            print json.dumps(eval(result),indent=2)
            print ''
        else:
            child.expect('.*')
            print '500 Internal Server Error'

    print ':::Domain status search'
    for command in command_domain:
        child.sendline ('%s' % command)
        i = child.expect(['(\[\[\{.*)root@','(\[\[\{.*\}\]\])','\[\{\}\]', '500 Internal Server Error'])
        if i == 0 or i == 1:
            result = child.match.group(1)
            result = re.sub(r"(?m)(\r\n\[)", "", result)
            print json.dumps(eval(result),indent=2)
            print ''
        else:
            child.expect('.*')
            print '500 Internal Server Error'

    print ':::Stream status search'
    for stream in eval(streams):
        child.sendline ('''curl -i -d "[{\\"interval\\":\\"1\\",\\"method\\":\\"StreamStatusSearch\\",\\"version\\":\\"2\\",\\"type\\":0, \\"protocols\\":[1,2,3,4,5],\\"urls\\":[\\"%s\\"], \\"startTime\\":\\"%s\\", \\"endTime\\":\\"%s\\"}]" "http://42.62.25.32/portal_interface?cchost_tag=sms.information.center"''' % (stream,starttime, endtime))
        i = child.expect(['(\[\[\{.*)root@','(\[\[\{.*\}\]\])','\[\{\}\]', '500 Internal Server Error'])
        if i == 0 or i == 1:
            result = child.match.group(1)
            result = re.sub(r"(?m)(\r\n\[)", "", result)
            print json.dumps(eval(result),indent=2)
            print ''
        else:
            child.expect('.*')
            print '500 Internal Server Error'

# Entrance
print 'You entered: ', len(sys.argv), 'arguments...'
print 'they are: ', str(sys.argv)

if len(sys.argv) != 1:
    print 'Specify starttime and endtime'
    
    starttime = sys.argv[1]
    endtime = sys.argv[2]
    if re.search(',', starttime):
        starttime = totimestampNew(starttime)
        endtime = totimestampNew(endtime)

    streams = getBaseStream(starttime,endtime)    
    if streams is None:
        print 'No streams!'
        sys.exit(0)

    child = server_ssh_login(server_ip='192.168.32.223', user_name='root', user_password='123456')
    excute_send_expect(child=child, starttime=starttime, endtime=endtime, streams=streams)

elif len(sys.argv) == 1:
    print 'Without specify starttime and endtime, starttime=now-360, endtime=now+360'
    currentTs = str(time.time()).split('.')[0]
    print 'currentTs:', currentTs
    starttime = int(currentTs) - 360
    endtime = int(currentTs) + 360

    streams = getBaseStream(starttime,endtime)
    if streams is None:
        print 'No streams!'
        sys.exit(0)

    child = server_ssh_login(server_ip='192.168.32.223', user_name='root', user_password='123456')
    excute_send_expect(child=child, starttime=starttime, endtime=endtime, streams=streams)
