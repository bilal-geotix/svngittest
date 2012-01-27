
#import time
#import TimeHandler

#import shutil
#import datetime
import Offering
import Property
import Procedure
import FeatureOfInterest
import Observation
import SDEService
import Service_API

obj = Offering.Offering("","",1)
obj.name = 'DCC Unit 12'
instanceTest = Service_API.ServiceAPI().getServceInstance()
print instanceTest.getOffering(obj)

obj = Offering.Offering("","",1)
obj.name = 'DCC Unit 12'
result = SDEService.SDEService().getOffering(obj)
print result

obj2 = Property.Property("")
obj2.prop_desc = 'urn:ogc:def:phenomenon:OGC:1.0:30:Noise'
result2 = SDEService.SDEService().getProperty(obj2)
print result2

obj3 = Procedure.Procedure()
obj3.unique_id = "urn:x-eea:object:sensor:noise:IE10001"
result3 = SDEService.SDEService().getProcedure(obj3)
if result3 != None and result3 != -1:
    print str(result3.x)
else:
    print result3
obj3.procedure_id = 1206
obj3.property_id = 6
result4 = SDEService.SDEService().checkProp_Proc(obj3)
print result4

obj4 = FeatureOfInterest.FeatureOfInterest()
obj4.name = "DCC Unit 7"
result5 = SDEService.SDEService().getFeature(obj4)
if result5 != None and result5 != -1:
    print result5.featureID

obj5 = Observation.Observation()
obj5.offering_id = 1630
obj5.property_id = 6
result6 = SDEService.SDEService().checkProp_Off(obj5)
print result6

obj6 = FeatureOfInterest.FeatureOfInterest()
obj6.name = "DCC Unit 7"
obj6.offering_id = 1630
obj6.featureID = 1829
result7 = SDEService.SDEService().checkFoi_Off(obj6)
print result7

obj7 = Observation.Observation()
obj7.time_stamp = "2012-01-17T00:15:00" 
prop = Property.Property("")
prop.property_id = 6
obj7.property_ref = prop   
obj7.offering_id = 1619#1111
obj7.time_stamp_begin = "2012-01-17T00:10:00"
prod = Procedure.Procedure()
prod.procedure_id = 806
obj7.procedure_ref = prod
feat = FeatureOfInterest.FeatureOfInterest()
feat.featureID = 1818
obj7.feature_ref = feat
result8 = SDEService.SDEService().checkObservation(obj7)
if result8 == None:
    print "error"
else:
    print result8.objectID
    print result8.numeric_value
    
#obj9 = Procedure.Procedure()
#obj9.procedure_id = 1216
#obj9.property_id = 6
#result10 = SDEService.SDEService().createNewProc_Prop(obj9)
#print result10

#obj5 = Observation.Observation()
#obj5.offering_id = 1630
#obj5.property_id = 7111 #Change to 6 to test 
#result6 = SDEService.SDEService().createNewProp_OFF(obj5)
#print result6


#obj6 = FeatureOfInterest.FeatureOfInterest()
#obj6.offering_id = 1
#obj6.featureID = 9000
#result7 = SDEService.SDEService().createNewFoi_Off(obj6)
#print result7

#createNewOffering
#obj = Offering.Offering("","",1)
#obj.name = 'DCC Unit Test'
#obj.service_id = 1
#obj.procedure_id = 806
#result = SDEService.SDEService().createNewOffering(obj)
#print result


#createNewProcedure
#obj9 = Procedure.Procedure()
#obj9.x = -4.2477339999999231
#obj9.y =  53.323524000000077
#obj9.longname = "Test"
#obj9.unique_id = "Test"
#result10 = SDEService.SDEService().createNewProcedure(obj9)
#print result10

#createNewFeature
#obj6 = FeatureOfInterest.FeatureOfInterest()
#obj6.name = "Test"
#obj6.description = ""
#obj6.id_value = "Test"
#obj6.code_space = "333ffd"
#obj6.sampled_feature_url = ""
#obj6.x = -4.2477339999999231
#obj6.y = 53.323524000000077
#result7 = SDEService.SDEService().createNewFeature(obj6)
#print result7


#createNewObservation
#obj7 = Observation.Observation()
#obj7.time_stamp = "2012-01-25T00:15:00" 
#prop = Property.Property("")
#prop.property_id = 6
#obj7.property_ref = prop   
#obj7.offering_id = 1619#1111
#obj7.time_stamp_begin = "2012-01-25T00:10:00"
#prod = Procedure.Procedure()
#prod.procedure_id = 806
#obj7.procedure_ref = prod
#feat = FeatureOfInterest.FeatureOfInterest()
#feat.featureID = 1818
#obj7.feature_ref = feat
#result8 = SDEService.SDEService().createNewObservation(obj7)
#if result8 == None:
#    print "error"
#else:
#    print result8

#updateObservation
#obj7 = Observation.Observation()
#obj7.objectID = 4918699
#obj7.time_stamp = "2012-01-25T00:15:00" 
#prop = Property.Property("")
#prop.property_id = 6
#obj7.property_ref = prop   
#obj7.offering_id = 1619#1111
#obj7.time_stamp_begin = "2012-01-25T00:10:00"
#prod = Procedure.Procedure()
#prod.procedure_id = 806
#obj7.procedure_ref = prod
#feat = FeatureOfInterest.FeatureOfInterest()
#feat.featureID = 1818
#obj7.feature_ref = feat
#obj7.numeric_value = 58
#result8 = SDEService.SDEService().updateObservation(obj7)
#if result8 == None:
#    print "error"
#else:
#    print result8


#pathLog = "data/Log/log22.txt"
#now = datetime.datetime.now()
#logTime = now.strftime("%Y-%m-%d %H:%M")


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

 
        