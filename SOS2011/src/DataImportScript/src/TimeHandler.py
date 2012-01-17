'''
Created on 15 Dec 2011

@author: berg3428
'''
import time

import datetime
class TimeHandler:
    '''
    Class to handling converts of date
    '''


    def __init__(self):
        return
    
    def getTime(self,dateStr):
        dTime = None
        try:
            dTime = dateStr.split('+',1)[0]
            return dTime
        except:
            return dTime
    
    def getEpochTime(self,dateStr):
        result = 0
        try:
            dTime = dateStr.split('+',1)[0]
            try:
                d = datetime.datetime.strptime(dTime,'%Y-%m-%dT%H:%M:%S')
                seconds_since_epoch = time.mktime(d.timetuple()) 
                result = int(round(seconds_since_epoch))
                return result
            except:
                d = datetime.datetime.strptime(dTime,'%Y-%m-%dT%H:%M:%S.%f')
                seconds_since_epoch = time.mktime(d.timetuple())
                result = int(round(seconds_since_epoch))
                return result
        except:
            return result
        
    def getTimeFromEpoch(self,seconds):  
        try:
            return datetime.datetime.fromtimestamp(seconds)
        except:
            return None
        