'''
Created on 21 Nov 2011

@author: berg3428
'''

import RestService

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
    numeric_value = None
    valid = 1
    def __init__(self):
        return
    
    def __str__(self):
        return "test"#return "feaID: " + str(self.feature_of_interest_id) + " Time: " + str(self.time_stamp) +" value: "+self.numeric_value +" OffID; "+str(self.offering_id)+" PropID: "+str(self.property_id)+" ProcedureID: "+str(self.procedure_id)+" Point: "+self.featureObj.shape
    
    def handlingObservation(self):
        if RestService.RestService().checkProp_Off(self) == None:
            if RestService.RestService().createNewProp_OFF(self) == None:
                return -1   
        
        obj = RestService.RestService().checkObservation(self)
        if obj == None:
            # Error
            return -1
        if obj.objectID == 0:
            print "DO update"
            return 0
        result = RestService.RestService().createNewObservation(self)
        if result == None:
            return -1
        # Inserted
        return 1
        