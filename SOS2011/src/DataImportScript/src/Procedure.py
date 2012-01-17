'''
Created on 8 Dec 2011

@author: berg3428
'''
import RestService
class Procedure:
  
    procedure_id = None
    unique_id = ""
    longname = ""
    intended_application = ""
    contact = -1
    x = 0.0
    y = 0.0
    shape = ""
    property_id = None
    
    def __init__(self):
        return
    
    def handlingProcedure(self):
        # Gets the procedure
        obj = RestService.RestService().getProcedure(self)
        
        # Create new if not existing
        if obj == None:
            result = self.createprocedure()
            return result
        elif obj == -1:
            return 0
        # Sets the ObejctId for the newly created
        self.procedure_id = obj.procedure_id
        self.x = obj.x
        self.y = obj.y 
        test = RestService.RestService().checkProp_Proc(self)
        
        if test == None:
            # Create relation procedure_property
            if self.createProc_prop() == 0:
                return 0
        elif test == -1:
            return 0
      
        return 1 
    
    def createprocedure(self):
        procID = RestService.RestService().createNewProcedure(self)
        if procID == None:
            return 0
        self.procedure_id = procID
        if self.createProc_prop() == 0:
            return 0
        
        return 1
    
    def updateprocedure(self):
        return 1
    
    def createProc_prop(self):    
        result = RestService.RestService().createNewProc_Prop(self)
        if result == None:
            return 0
        return 1