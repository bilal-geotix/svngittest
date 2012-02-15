'''
Created on 21 Nov 2011

@author: berg3428
'''


import xml.dom.minidom
import glob
import os
import FeatureOfInterest
import Offering
import Observation
import Property
import Procedure
import Log
import TimeHandler
import sys
import traceback

pathPickup = "data/Test"
pathInserted = "data/Inserted"
pathError = "data/Failed"
pathErrorLog = "data/Log/logError.txt"
pathLog = "data/Log/log.txt"
maxSize = 1024 * 1024 * 20 # 20 MB
debug_onoff = 1


# Getobservation files from xml folder
def getXML(path):
    obj = xml.dom.minidom;
    xmlTemp = obj.parse(path)
    return xmlTemp    


Log.Log().ConsoleOutput("---Started - looking for files to process---")   

for xmlfilepath in glob.glob(os.path.join(pathPickup, "*.xml")):
    message = ""
    observationList = []
    filename = os.path.basename(xmlfilepath)
    Log.Log().ConsoleOutput("Starting processing: " + filename)
    try:
        
        if Log.Log().getFileSize(xmlfilepath) > maxSize:
            Log.Log().writeLog(pathErrorLog, "File to big to be processed: "+filename)
            errorFilePath = os.path.join(pathError, filename)
            Log.Log().copyFile(xmlfilepath, errorFilePath)
            Log.Log().deleteFile(xmlfilepath)
            continue
        
        xmlParsed = getXML(xmlfilepath)
        for node in xmlParsed.getElementsByTagName("sos:GetObservationResponse"):# ("sos:InsertObservation"):
            
            # Get observations
            for ov in node.getElementsByTagName("sos:observationData"): #("sos:observation"):
                featureOfInterest = ov.getElementsByTagName("om:featureOfInterest")[0]
                nameNode = featureOfInterest.getElementsByTagName("gml:name")
                
                # Observation instance
                observationObj = Observation.Observation()
                  
                # Get procedure info 
                procedureObj = Procedure.Procedure()
                procedureNode = ov.getElementsByTagName("om:procedure")[0]
                procedureObj.unique_id = procedureNode.attributes['xlink:href'].nodeValue
                
                observPropNode = ov.getElementsByTagName("om:observedProperty")[0]
                obserPropDesc = observPropNode.attributes['xlink:href'].nodeValue 
                propertyObj = Property.Property(obserPropDesc)
               
                # Property handling checks if it exist
                if propertyObj.handlingProperty() == 0:
                    observationObj.valid = 0
                    Log.Log().writeLog(pathErrorLog, "Property doesn't exist "+ obserPropDesc +" : "+filename)
                    raise StopIteration()
                observationObj.property_ref = propertyObj
                observationObj.property_id = propertyObj.property_id
                
                # Test if contain name
                if nameNode.length == 1:
                    
                    # Sensor point
                    point = featureOfInterest.getElementsByTagName("gml:pos")[0].firstChild.data.strip()
                    points = point.split(" ")
                    
                    # Sensor name
                    sensor_name = nameNode[0].firstChild.data.strip()
                    
                    # Create new procedure and Proc_prop
                    procedureObj.x = points[1]
                    procedureObj.y = points[0]
                    procedureObj.property_id = observationObj.property_id
                    if procedureObj.handlingProcedure() == 0:
                        observationObj.valid = 0
                        Log.Log().writeLog(pathErrorLog, "Procedure could be created or found: "+filename)
                        raise StopIteration() 
                    observationObj.procedure_ref = procedureObj
                    
                    # Create new offering
                    off_obj = Offering.Offering(sensor_name,procedureObj.procedure_id,1) #PCK: the service is hardcoded, to be changed
                    if off_obj.handlingOffering() == 0:
                        Log.Log().writeLog(pathErrorLog, "Offering: "+off_obj.name+" couldn't be created: "+filename)
                        raise StopIteration()
                                        
                    observationObj.procedure_ref.offering_id = off_obj.offering_id
                    observationObj.offering_id = off_obj.offering_id
                    codespaceNode = featureOfInterest.getElementsByTagName("gml:identifier")
                    codespace = codespaceNode[0].attributes['codeSpace'].nodeValue
                    featureGMLid = ov.getElementsByTagName("sams:SF_SpatialSamplingFeature")[0].attributes["gml:id"].nodeValue 
                    
                    feature = FeatureOfInterest.FeatureOfInterest()
                    feature.name = sensor_name
                    feature.code_space = codespace
                    feature.id_value = sensor_name #PCK: should propably be gml:id of sams:SF_SpatialSamplingFeature
                    feature.feature_type = None
                    feature.description = None
                    feature.x = points[1]
                    feature.y = points[0]
                    feature.offering_id = off_obj.offering_id
                   
                    # Create feature and reference FOI_OFF
                    if feature.handling_feature() == 0:
                        observationObj.valid = 0
                        Log.Log().writeLog(pathErrorLog, "Feature couldn't be created or found: "+filename)
                                       
                    observationObj.feature_gml_id = featureGMLid
                    observationObj.feature_ref = feature
                else:
                    observationObj.feature_gml_id = ov.getElementsByTagName("om:featureOfInterest")[0].attributes["xlink:href"].nodeValue
                
                # Get result values for observation
                #TimeHandler.TimeHandler().getEpochTime(ov.getElementsByTagName("gml:TimePeriod")[0].getElementsByTagName("gml:beginPosition")[0].firstChild.data.strip())
                startVal = ov.getElementsByTagName("gml:TimePeriod")[0].getElementsByTagName("gml:beginPosition")[0].firstChild.data.strip()
                observationObj.time_stamp_begin = TimeHandler.TimeHandler().getTime(startVal)
                observationObj.time_stamp_seconds_begin = TimeHandler.TimeHandler().getEpochTime(startVal)
                endVal = ov.getElementsByTagName("gml:TimePeriod")[0].getElementsByTagName("gml:endPosition")[0].firstChild.data.strip()
                observationObj.time_stamp = TimeHandler.TimeHandler().getTime(endVal)
                observationObj.time_stamp_seconds = TimeHandler.TimeHandler().getEpochTime(endVal)
                
                observationObj.numeric_value = ov.getElementsByTagName("om:result")[0].firstChild.data.strip()    
                observationObj.unit_of_measure = ov.getElementsByTagName("om:result")[0].attributes["uom"].nodeValue
                observationList.append(observationObj)
            
            # Offering, procedure and features have been created here
            
            # Match observation
            for obs1 in observationList:
                for obs2 in observationList:
                    if "#"+obs1.feature_gml_id == obs2.feature_gml_id:
                        if obs1.valid == 1:
                            obs2.feature_ref = obs1.feature_ref
                            obs2.procedure_ref = obs1.procedure_ref
                            obs2.offering_id = obs1.offering_id  
                        else:
                            obs2.valid = 0
            
            # Insert observation                
            for obserObj in observationList:
                if obserObj.valid == 1:
                    observationTest = obserObj.handlingObservation()
                    if observationTest > 0:
                        message = ""
                        Log.Log().ConsoleOutput("Observation inserted: " + obserObj.numeric_value)
                        # Inserted or updated
                        # Log.Log().writeLog(pathLog, message)
                    elif observationTest == 0:
                        Log.Log().writeLog(pathLog, "Observation all ready inserted: "+filename)
                    else:
                        Log.Log().writeLog(pathErrorLog, "ERROR inserting observation: "+filename)
                else:
                    Log.Log().writeLog(pathErrorLog, "Observation xml not valid: "+filename)
                        
              
            message = "Inserted observations from file "+filename
            Log.Log().writeLog(pathLog, message)
            if Log.Log().copyFile(xmlfilepath, os.path.join(pathInserted, filename)) == 1:
                Log.Log().deleteFile(xmlfilepath)
                   
    except StopIteration:
        errorFilePath = os.path.join(pathError, filename)
        if(Log.Log().copyFile(xmlfilepath, errorFilePath)) == 1:
            Log.Log().deleteFile(xmlfilepath)
        #Log.Log().writeLog(pathErrorLog, message)
    except AttributeError:
        errorFilePath = os.path.join(pathError, filename)
        if(Log.Log().copyFile(xmlfilepath, errorFilePath)) == 1:
            Log.Log().deleteFile(xmlfilepath) 
        message = "XML parse error: "+filename
        Log.Log().writeLog(pathErrorLog, message)
    except:
        errorFilePath = os.path.join(pathError, filename)
        if(Log.Log().copyFile(xmlfilepath, errorFilePath)) == 1:
            Log.Log().deleteFile(xmlfilepath)    
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        message = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
        message += " Uncaught error: "+filename
        Log.Log().writeLog(pathErrorLog, message)
    ##continue with loop for next xml file
Log.Log().ConsoleOutput("---End---")
        