'''
Created on 24 Nov 2011

@author: berg3428
'''
#import RestService
import Service_API
class Property:
    property_id = -1
    offering_id = -1
    prop_desc = ""
    data_type = ""
    unit_of_measure = ""
    
    def __init__(self,desc):
        self.prop_desc = desc
        self.property_id = self.property_id
    
    def handlingProperty(self):
        serviceInstance = Service_API.ServiceAPI().getServceInstance()  
        obj = serviceInstance.getProperty(self)
        # Test that the property exist
        if obj == None:
            return 0
        elif obj == -1:
            return 0
        self.property_id = obj   
        return 1
    
    def checkProperty(self):
        serviceInstance = Service_API.ServiceAPI().getServceInstance()
        result = serviceInstance.checkProp_Off(self)
        if result == None:
            return 0
        return 1