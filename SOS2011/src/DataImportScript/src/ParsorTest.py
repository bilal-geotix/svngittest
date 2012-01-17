import urllib
import urllib2
import json
#import time
#import TimeHandler

#import shutil
import os
import datetime
#import datetime


#import pytz
pathLog = "data/Log/log22.txt"
now = datetime.datetime.now()
logTime = now.strftime("%Y-%m-%d %H:%M")
try:
    statinfo = os.stat(pathLog)
        
    print statinfo.st_size 
    fn = None
    if not os.path.exists(pathLog):  
        print "Not"
        #fn = open(pathLog, "w")
    else:
        #fn = open(pathLog, "a")
        statinfo = os.stat(pathLog)
        
        print statinfo.st_size 
    #fn.write(logTime +"ddd \n")
    #fn.close()
    print "OK"
except:
    print "Error"

#from datetime import datetime
#s = '2010-06-02T01:13:01.001'
#s1 = '2010-06-02T01:00:00.000+2:00'
#ss = '1970-01-01T02:10:00+0:00'
#print s
#print s1 
#print ss 
#print TimeHandler.TimeHandler().getEpochTime(s)
#print TimeHandler.TimeHandler().getEpochTime(s1)
#print TimeHandler.TimeHandler().getEpochTime(ss)
#print TimeHandler.TimeHandler().getTimeFromEpoch(TimeHandler.TimeHandler().getEpochTime(s))
#print TimeHandler.TimeHandler().getTimeFromEpoch(TimeHandler.TimeHandler().getEpochTime(s1))
#print TimeHandler.TimeHandler().getTimeFromEpoch(TimeHandler.TimeHandler().getEpochTime(ss))
#s3 =ss.split('+',1)[0]
#print s3

#d = datetime.datetime.strptime(s3,'%Y-%m-%dT%H:%M:%S')
#seconds_since_epoch = time.mktime(d.timetuple())  
#print seconds_since_epoch
#print int(round(seconds_since_epoch))
#stuctTime = time.localtime(seconds_since_epoch)
#print str(stuctTime.tm_year) +" "+ str(stuctTime.tm_mon) +" "+ str(stuctTime.tm_mday)+" "+ str(stuctTime.tm_hour)+" "+ str(stuctTime.tm_min) +" "+ str(stuctTime.tm_sec)
#print datetime.datetime.fromtimestamp(seconds_since_epoch)

#d2 = d.toordinal()
#print d2
#print datetime.datetime.fromordinal(d2)
#try:
#print datetime.datetime.strptime(s,'%Y-%m-%dT%H:%M:%S.%f') #'%Y-%m-%dT%H:%M:%SZ')
#print  time.mktime(datetime.datetime.strptime(s,'%Y-%m-%dT%H:%M:%S.%f').timetuple())  
#except:
#print "error"

#datetime.datetime(2010, 2, 25, 0, 0)
#dt.strftime('%Y%m%d')
#'20100225'

#import BuildResturl
#import Offering

#objOff = Offering.Offering("Noise")

#objOff =  RestService.RestService().getOffering(objOff) 
#print objOff.name + " "+str(objOff.offering_id)

#str2 = "222.33 4444.333"
#test = str2.split(" ")
#print str(test.len()) + str(test[0])+" : "+str(test[1])

def callRest(url,parameters):
    try:
        req = urllib2.Request(url, urllib.urlencode(parameters))   
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
        return json.loads(response)
    except:
        return [{"error" : {"code": 400,"meesage" : "CallError:"+url}}]
def urlStr(strToEncode):
    return urllib.urlencode(strToEncode)


#tp = '2010-06-02T01:00:00.000+2:00'
#tp1 = '2010-06-02T01:00:00.000'
#time_format = "%Y-%m-%d %H:%M:%S"
#print time.strftime(tp1, time_format)    
#resturl = BuildResturl.BuildRestURL().buildUrl(7)
#test = "PROPERTY_ID="+str(2)+"%20and%20OFFERING_ID="+str(2)+""
#resturl += "where="+test+"&returnCountOnly=false&returnIdsOnly=true&returnGeometry=false&outFields=*&f=pjson"
#print resturl
#parameters = {'f' : 'json','query': json.dumps(test) }
#jsonResponse =  callRest(resturl, "")
#str2 = "hand sss sss ssss"
#print urllib.quote(str2) # .replace(" ", "%20")
#print urlStr(str2)

 
        