'''
Created on 24 Nov 2011

@author: berg3428
'''
import shutil
import os
import datetime

class Log:
    
    def __init__(self):
        return
    
    def copyFile(self,fromFilePath,toFilePath):
        try:
            shutil.copy(fromFilePath,toFilePath)
            return 1
        except:
            return 0
        
    def deleteFile(self,filepath):
        try:
            os.remove(filepath)
            return 1
        except:
            return 0
        
    def writeLog(self,logfilepath,message):
        now = datetime.datetime.now()
        logTime = now.strftime("%Y-%m-%d %H:%M")
        try:
            fn = None
            if not os.path.exists(logfilepath):  
                fn = open(logfilepath, "w")
            else:
                fn = open(logfilepath, "a")
                #statinfo = os.stat(logfilepath)
                #print statinfo.st_size 
            fn.write(logTime +" "+ message+"\n")
            fn.close()
            return 1
        except:
            return 0
     
    def getFileSize(self,filePath):
        try:
            statinfo = os.stat(filePath)
            #print statinfo.st_size
            return statinfo.st_size
        except:
            print "ERROR"
            return -1 