'''
Created on 23 Nov 2011

@author: berg3428
'''
import RestService

class Offering:

    offering_id = -1
    name = ""
    procedure_id = None
    service_id = None
    def __init__(self,name,procedureID, serviceID):
        self.name = name
        self.procedure_id = procedureID
        self.service_id = serviceID
        
    def handlingOffering(self):
        service = RestService.RestService()
        id_off = service.getOffering(self)
        if id_off == None:
            newid = service.createNewOffering(self)
            if newid == None:
                return 0
            self.offering_id = newid
            return 1
        else:
            if id_off == -1:
                return 0
            else:
                self.offering_id = id_off 
                return 1 
        
    def exist(self):
        return bool(1)
    
    def findOfferingId(self):
        id_off = RestService.RestService().getOffering(self)
        if id_off == None:
            return 0
        else:
            self.offering_id = id_off 
            return 1 