'''
Created on 23 Nov 2011

@author: berg3428
'''

import RestService

class FeatureOfInterest():
    '''
    Feature_of_interest
    '''
    featureID = None
    offering_id = None
    name = None
    description =None
    sampled_feature_url = None
    code_space = None
    id_value = None
    x = 0.0 
    y = 0.0
    
    def __init__(self):
        return
    def handling_feature(self):
        obj = RestService.RestService().getFeature(self)
        if obj == None:
            result = self.createfeature()
            return result
        elif obj == -1:
            return 0
        self.featureID = obj.featureID
        resultCheck =RestService.RestService().checkFoi_Off(self)
        if resultCheck == None or resultCheck == -1:
            return 0
        return 1
    
    def createfeature(self):
        feaID = RestService.RestService().createNewFeature(self)
        if feaID == None:
            return 0
        self.featureID = feaID 
        return self.create_Foi_off()
    
    def create_Foi_off(self):
        result = RestService.RestService().createNewFoi_Off(self)
        if result == None:
            return 0
        return 1