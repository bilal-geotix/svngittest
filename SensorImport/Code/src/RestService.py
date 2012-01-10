'''
Created on 27 Nov 2011

@author: BERG3428
'''

import urllib
import urllib2
import json
import BuildResturl
import Procedure
import FeatureOfInterest
import Observation


class RestService:
    
    buildInstance = BuildResturl.BuildRestURL() 
    
    def __init__(self):
        return
    
    def callRest(self,url,parameters):
        try:
            req = urllib2.Request(url, urllib.urlencode(parameters))   
            f = urllib2.urlopen(req)
            response = f.read()
            f.close()
            return json.loads(response)
        except:
            return [{"error" : {"code": 400,"meesage" : "CallError:"+url}}]
    
    # Encode spaces
    def encodeStr(self,strToEncode):
        return urllib.quote(strToEncode)
    
    def checkResponse(self,response):
        try:
            response['error']
            return 0
        except:
            return 1
        
    
    def getOffering(self,offeringObj):
        resturl = self.buildInstance.buildUrl(2)
        resturl += "where=OFFERING_NAME='"+self.encodeStr(offeringObj.name)+"'&returnCountOnly=false&returnIdsOnly=false&outFields=*&f=pjson"
        
        jsonResponse = self.callRest(resturl,"")
        if self.checkResponse(jsonResponse) == 0:
            return None
        try:
            return jsonResponse['features'][0]['attributes']['OBJECTID']
        except:
            return None
    
    def getProperty(self,propertyObj):
        resturl = self.buildInstance.buildUrl(6)
        #print propertyObj.prop_desc
        resturl +="where=PROPERTY_DESCRIPTION='"+self.encodeStr(propertyObj.prop_desc)+"'&returnCountOnly=false&returnIdsOnly=false&returnGeometry=true&outSR=&outFields=*&f=pjson" 
        jsonResponse = self.callRest(resturl, "")
        if self.checkResponse(jsonResponse) == 0:
            return None
        try:
            return jsonResponse['features'][0]['attributes']['OBJECTID']
        except:
            return None 
    
    def getProcedure(self,procedureObj):
        resturl = self.buildInstance.buildUrl(3)
        resturl += "where=UNIQUE_ID='"+self.encodeStr(procedureObj.unique_id)+"'&time=&returnCountOnly=false&returnIdsOnly=false&returnGeometry=true&outFields=*&f=pjson"
        jsonResponse = self.callRest(resturl,"")
        if self.checkResponse(jsonResponse) == 0:
            return None
        try:
            temp = Procedure.Procedure()
            temp.procedure_id = jsonResponse['features'][0]['attributes']['OBJECTID']
            temp.x = jsonResponse['features'][0]['geometry']["points"][0][0]
            temp.y = jsonResponse['features'][0]['geometry']["points"][0][1]    
            return temp
        except:
            # TODO handling server down
            return None
        
    def getFeature(self,featureObj):
        resturl = self.buildInstance.buildUrl(5)
        resturl += "where=NAME='"+self.encodeStr(featureObj.name)+"'&returnCountOnly=false&returnIdsOnly=false&returnGeometry=false&outFields=*&f=pjson"
        jsonResponse = self.callRest(resturl,"")
        if self.checkResponse(jsonResponse) == 0:
            return None
        try:
            temp = FeatureOfInterest.FeatureOfInterest()
            temp.featureID = jsonResponse['features'][0]['attributes']['OBJECTID']
            return temp
        except:
            return None
    
    def createNewOffering(self,offeringObj):
        newOffering = [{"attributes":{}}]
        newOffering[0][u'attributes']['OFFERING_NAME'] = str(offeringObj.name)
        newOffering[0][u'attributes']['PROCEDURE_'] = str(offeringObj.procedure_id)
        #newOffering[0][u'attributes']['SERVICE'] = offeringObj.service_id
        resturl = self.buildInstance.buildUrl(16)
        parameters = {'f' : 'json','features': json.dumps(newOffering)}
        jsonResponse = self.callRest(resturl, parameters)
        if self.checkResponse(jsonResponse) == 0:
            return None
        if jsonResponse['addResults'][0]['success'] == True:
            print "New Offering: " + str(jsonResponse['addResults'][0]['objectId'])
            return jsonResponse['addResults'][0]['objectId']
        return None
               
    def createNewFeature(self,featureObj):
        
        newfeature = [{"geometry" : {"x" : featureObj.x, "y" : featureObj.y}, "attributes":{}}]
        newfeature[0][u'attributes']['NAME'] = featureObj.name
        newfeature[0][u'attributes']['CODE_SPACE'] = featureObj.code_space
        newfeature[0][u'attributes']['ID_VALUE'] = featureObj.id_value
        newfeature[0][u'attributes']['DESCRIPTION'] = featureObj.description
        newfeature[0][u'attributes']['SAMPLED_FEATURE_URL'] = featureObj.sampled_feature_url
        resturl = self.buildInstance.buildUrl(1)
        parameters = {'f' : 'json','features': json.dumps(newfeature) }
        
        jsonResponse = self.callRest(resturl, parameters)
        if self.checkResponse(jsonResponse) == 0:
            return None
        if jsonResponse['addResults'][0]['success'] == True:
            print "Newfeature: "+ str(jsonResponse['addResults'][0]['objectId'])
            return jsonResponse['addResults'][0]['objectId']
        else:
            return None
        
    def createNewObservation(self,observationObj):
        newObservation = [{"attributes":{}}]
        newObservation[0][u'attributes']['UNIT_OF_MEASURE'] = str(observationObj.unit_of_measure)
        newObservation[0][u'attributes']['TEXT_VALUE'] = ""
        newObservation[0][u'attributes']['NUMERIC_VALUE'] = str(observationObj.numeric_value)
        #newObservation[0][u'attributes']['TIME_STAMP'] = observationObj.time_stamp
        #newObservation[0][u'attributes']['TIME_STAMP_BEGIN'] = observationObj.time_stamp_begin
        newObservation[0][u'attributes']['TIME_STAMP_TEXT'] = observationObj.time_stamp
        newObservation[0][u'attributes']['TIME_STAMP_BEGIN_TEXT'] = observationObj.time_stamp_begin
        newObservation[0][u'attributes']['PROPERTY'] = observationObj.property_ref.property_id
        newObservation[0][u'attributes']['PROCEDURE_'] = observationObj.procedure_ref.procedure_id
        newObservation[0][u'attributes']['FEATURE'] = observationObj.feature_ref.featureID
        newObservation[0][u'attributes']['OFFERING'] = observationObj.offering_id
        resturl = self.buildInstance.buildUrl(11)
        parameters = {'f' : 'json','features': json.dumps(newObservation)}
        jsonResponse = self.callRest(resturl, parameters)
        if self.checkResponse(jsonResponse) == 0:
            return None
        if jsonResponse['addResults'][0]['success'] == True:
            print "New Observation: " + str(jsonResponse['addResults'][0]['objectId'])
            return jsonResponse['addResults'][0]['objectId']
        return None
    
    def createNewProcedure(self,procedureObj):
        
        newProcedure = [ {"geometry" : {"points": [[procedureObj.x, procedureObj.y]]}, "attributes":{}}]
        newProcedure[0][u'attributes']['UNIQUE_ID'] = procedureObj.unique_id
        newProcedure[0][u'attributes']['LONG_NAME'] = procedureObj.longname
        newProcedure[0][u'attributes']['INTENDED_APPLICATION'] = ""
        newProcedure[0][u'attributes']['CONTACT'] = None
        #newProcedure[0][u'attributes']['SHAPE'] = "Point"
        resturl = self.buildInstance.buildUrl(4)
        parameters = {'f' : 'json','features': json.dumps(newProcedure) }
        
        jsonResponse = self.callRest(resturl, parameters)
        if self.checkResponse(jsonResponse) == 0:
            return None
        if jsonResponse['addResults'][0]['success'] == True:
            print "New Procedure; "+ str(jsonResponse['addResults'][0]['objectId'])
            return jsonResponse['addResults'][0]['objectId']
        else:
            return None
    
    def createNewFoi_Off(self,featureObj):
        resturl = self.buildInstance.buildUrl(15)
        newFoiOff = [{"attributes":{}}]
        newFoiOff[0][u'attributes']['FOI_ID'] = featureObj.featureID
        newFoiOff[0][u'attributes']['OFFERING_ID'] = featureObj.offering_id
        parameters = {'f' : 'json','features': json.dumps(newFoiOff) }
        jsonResponse = self.callRest(resturl, parameters)
        if self.checkResponse(jsonResponse) == 0:
            return None
        if jsonResponse['addResults'][0]['success'] == True:
            print "New foi_off: "+str(jsonResponse['addResults'][0]['objectId'])
            return jsonResponse['addResults'][0]['objectId']
        else:
            return None
    
    def createNewProc_Prop(self,procedureObj):
        resturl = self.buildInstance.buildUrl(14)
        newProcProp = [{"attributes":{}}]
        newProcProp[0][u'attributes']['PROCEDURE_ID'] = str(procedureObj.procedure_id)
        newProcProp[0][u'attributes']['PROPERTY_ID'] = str(procedureObj.property_id)
        parameters = {'f' : 'json','features': json.dumps(newProcProp)}
        jsonResponse = self.callRest(resturl, parameters)
        if self.checkResponse(jsonResponse) == 0:
            return None
        if jsonResponse['addResults'][0]['success'] == True:
            print "New procProp: "+str(jsonResponse['addResults'][0]['objectId'])
            return jsonResponse['addResults'][0]['objectId']
        else:
            return None
        
    def createNewProp_OFF(self,observationObj):
        resturl = self.buildInstance.buildUrl(17)
        newProcProp = [{"attributes":{}}]
        newProcProp[0][u'attributes']['OFFERING_ID'] = str(observationObj.offering_id)
        newProcProp[0][u'attributes']['PROPERTY_ID'] = str(observationObj.property_id)
        parameters = {'f' : 'json','features': json.dumps(newProcProp)}
    
        jsonResponse = self.callRest(resturl, parameters)
        if self.checkResponse(jsonResponse) == 0:
            return None
        if jsonResponse['addResults'][0]['success'] == True:
            print "New prop_OFF: "+str(jsonResponse['addResults'][0]['objectId'])
            return jsonResponse['addResults'][0]['objectId']
        else:
            return None
    
    def checkProp_Proc(self,procedureObj):
        resturl = self.buildInstance.buildUrl(8)
        resturl += "where=PROPERTY_ID="+str(procedureObj.property_id)+"%20and%20PROCEDURE_ID="+str(procedureObj.procedure_id)+"&returnCountOnly=false&returnIdsOnly=true&returnGeometry=false&outFields=*&f=pjson"
        jsonResponse = self.callRest(resturl, "")
        if self.checkResponse(jsonResponse) == 0:
            return None
        try:
            return jsonResponse['objectIds'][0]
        except:
            return None
    
    def checkProp_Off(self,observationObj):
        resturl = self.buildInstance.buildUrl(7)
        resturl += "where=PROPERTY_ID="+str(observationObj.property_id)+"%20and%20OFFERING_ID="+str(observationObj.offering_id)+"&returnCountOnly=false&returnIdsOnly=true&returnGeometry=false&outFields=*&f=pjson"
        jsonResponse = self.callRest(resturl, "")
        if self.checkResponse(jsonResponse) == 0:
            return None
        try:
            return jsonResponse['objectIds'][0]
        except:
            return None
    
    def checkFoi_Off(self,featureObj):
        resturl = self.buildInstance.buildUrl(9)
        resturl += "where=FOI_ID="+str(featureObj.featureID)+"%20and%20OFFERING_ID="+str(featureObj.offering_id)+"&returnCountOnly=false&returnIdsOnly=true&returnGeometry=false&outFields=*&f=pjson"
        jsonResponse = self.callRest(resturl, "")
        if self.checkResponse(jsonResponse) == 0:
            return None
        try:
            return jsonResponse['objectIds'][0]
        except:
            return None
        
    def checkObservation(self,observationObj):
        resturl = self.buildInstance.buildUrl(10)
        resturl += "where=TIME_STAMP='"+observationObj.time_stamp+"'%20and%20PROPERTY="+str(observationObj.property_ref.property_id)+"%20and%20OFFERING="+str(observationObj.offering_id)+"%20and%20TIME_STAMP_BEGIN='"+observationObj.time_stamp_begin+"'%20and%20PROCEDURE_="+str(observationObj.procedure_ref.procedure_id)+"%20and%20FEATURE="+str(observationObj.feature_ref.featureID)+"&returnCountOnly=false&returnIdsOnly=false&returnGeometry=false&outFields=*&f=pjson"
        jsonResponse = self.callRest(resturl,"")
        if self.checkResponse(jsonResponse) == 0:
            return None
        tempObj = Observation.Observation()
        try:
            if len(jsonResponse['features']) == 1:
                tempObj.objectID = jsonResponse['features'][0]['attributes']['OBJECTID']
                tempObj.numeric_value = jsonResponse['features'][0]['attributes']['NUMERIC_VALUE']
                return tempObj
            tempObj.objectID = 0
            return tempObj
        except:
            tempObj.objectID = -1
            return tempObj
        
    def updateObservation(self,observationObj):
        return "todo"