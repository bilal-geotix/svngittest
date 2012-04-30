'''
Created on 8 Dec 2011

@author: berg3428
'''
#import RestService
import Log
import Service_API
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
        serviceInstance = Service_API.ServiceAPI().getServceInstance()
        obj = serviceInstance.getProcedure(self)
        # Create new if not existing
        if obj == None:
            result = self.createprocedure()
            Log.Log().ConsoleOutput("New procedure created")
            return result
        elif obj == -1:
            return 0                                                                                                                                       
        Log.Log().ConsoleOutput("Procedure"+str(obj.procedure_id))
        # Sets the ObejctId for the newly created
        self.procedure_id = obj.procedure_id
        self.x = obj.x
        self.y = obj.y 
        Log.Log().ConsoleOutput("Check prop_proc")
        test = serviceInstance.checkProp_Proc(self)
        
        if test == None:
            # Create relation procedure_property
            Log.Log().ConsoleOutput("create proc_prop")
            if self.createProc_prop() == 0:
                return 0
        elif test == -1:
            return 0
        return 1 
    
    def createprocedure(self):
        serviceInstance = Service_API.ServiceAPI().getServceInstance()
        procID = serviceInstance.createNewProcedure(self)
        if procID == None:
            return 0
        self.procedure_id = procID
        if self.createProc_prop() == 0:
            return 0
        
        return 1
    
    def updateprocedure(self):
        return 1
    
    def createProc_prop(self):
        serviceInstance = Service_API.ServiceAPI().getServceInstance()  
        result = serviceInstance.createNewProc_Prop(self)
        if result == None:
            return 0
        return 1