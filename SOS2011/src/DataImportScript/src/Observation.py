'''
Created on 21 Nov 2011

@author: berg3428
'''

#import RestService
import Log
import Service_API
class Observation():
    
    objectID = -1
    offering_id = None
    feature_ref = None
    procedure_ref = None
    property_ref = None
    property_id = None
    unit_of_measure = None
    feature_gml_id = None
    procedure_id = None
    time_stamp_begin = None
    time_stamp = None
    time_stamp_seconds = None
    time_stamp_seconds_begin = None
    numeric_value = None
    valid = 1
    def __init__(self):
        return
    
    def __str__(self):
        return ""
    
    def handlingObservation(self):
        service_Instance = Service_API.ServiceAPI().getServceInstance()
        resultCheck = service_Instance.checkProp_Off(self)#RestService.RestService()
        if resultCheck == None:
            if service_Instance.createNewProp_OFF(self) == None:
                return -1   
        elif resultCheck == -1:
            return -1
        obj = service_Instance.checkObservation(self)
        if obj == None:
            # Error
            return -1
        if obj.objectID > 0:
            valueF = None
            try:
                sValue = str(self.numeric_value)
                valueF = float(sValue)
            except:
                return 0
            if obj.numeric_value != valueF:
                self.objectID = obj.objectID
                if service_Instance.updateObservation(self) == None:
                    return -1
                # updated
                return 1
            return 0
        result = service_Instance.createNewObservation(self)
        if result == None:
            Log.Log().ConsoleOutput("Failed to insert observation")
            return -1
        # Inserted
        Log.Log().ConsoleOutput("Observation inserted: " + str(self.numeric_value))
        return 1
        