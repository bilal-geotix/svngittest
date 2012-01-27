'''
Created on 27 Jan 2012

@author: Berg3428
'''
import RestService
import SDEService;

class ServiceAPI:
    '''
    classdocs
    
    Class to switch between rest API or arcPy sde 
    
    '''
    # 0 for sde otherwise rest
    type_to_use  = 1

    def __init__(self):
        '''
        Constructor
        '''
    def getServceInstance(self):
        if self.type_to_use == 0:
            return SDEService.SDEService()
        return RestService.RestService()