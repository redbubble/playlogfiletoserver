# By Jorgen Modin jorgen@webworks.se 2012-2014, licensed under the MIT license
import datetime
import time
from generatedrequests import requests as therequests
import pyparallelcurl
import pycurl

server = 'http://localhost:8080'
speedup = 1
maxparallelrequests = 9999

sleepduration = 0.5/speedup
t = datetime.datetime.now()
starttime = time.mktime(t.timetuple())


curloptions = {
    pycurl.SSL_VERIFYPEER: False,
    pycurl.SSL_VERIFYHOST: False,
    pycurl.USERAGENT: 'Play log file to server user agent',
    pycurl.FOLLOWLOCATION: True
}

#c.setopt(c.MAX_RECV_SPEED_LARGE, 10000)

parallel_curl = pyparallelcurl.ParallelCurl(maxparallelrequests, curloptions)

def go(request):
    parallel_curl.startrequest(server + request[1], on_request_done)
    return

   
def on_request_done(content, url, ch, search):
    
    if content is None:
        print "Fetch error for "+url
        return
    
    httpcode = ch.getinfo(2097154) # For some reason pycurl.HTTP_CODE produces error
    transfertime = ch.getinfo(3145731) # ... pycurl.TOTAL_TIME too
    if httpcode != 200:
        print "%0.3f seconds fetch error %s for %s" % (transfertime, str(httpcode),url)
        return
    else:
        print "%0.3f seconds fetch worked %s for %s" % (transfertime, str(httpcode),url)
    print "********"


def timetogo(request):
    reqtime = request[0]
    t = datetime.datetime.now()
    now = time.mktime(t.timetuple())
    return reqtime  <= (now - starttime) * speedup


for request in therequests:
    while True:
        if timetogo(request):
            go(request)
            break
        else:
            time.sleep(sleepduration)
    
    

