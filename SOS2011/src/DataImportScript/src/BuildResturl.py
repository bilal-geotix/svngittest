'''
Created on 8 Dec 2011

@author: berg3428
'''

class BuildRestURL:
    restServiceUrl ="http://discomap.eea.europa.eu/ArcGIS/rest/services/Test/SOS/FeatureServer/"
    #http://mite:6080/arcgis/rest/services/SOS/SOS_noise/MapServer
    def __init__(self):
        return
    
    def buildUrl(self,typeID):
        if typeID == 1:
            # Insert feature
            return self.restServiceUrl + "0/addFeatures"
        if typeID == 2:
            # Get offering
            return self.restServiceUrl + "5/query?"
        if typeID == 3:
            # Get procedure
            return self.restServiceUrl + "1/query?" 
        if typeID == 4:
            # Insert procedure
            return self.restServiceUrl + "1/addFeatures"
        if typeID == 5:
            # Get feature
            return self.restServiceUrl + "0/query?"
        if typeID == 6:
            # Get property
            return self.restServiceUrl + "8/query?"
        if typeID == 7:
            # Get prop_off
            return self.restServiceUrl + "7/query?"
        if typeID == 8:
            # Get Proc_prop
            return self.restServiceUrl + "6/query?"
        if typeID == 9:
            # Get FOI_OFF
            return self.restServiceUrl +"3/query?"
        if typeID == 10:
            # Test observation
            return self.restServiceUrl +"4/query?"
        if typeID == 11:
            # Insert observation
            return self.restServiceUrl +"4/addFeatures"
        if typeID == 12:
            # Get serviceDesc
            return self.restServiceUrl +"2/query?"
        if typeID == 13:
            # Get ContactDescription
            return self.restServiceUrl +"9/query?"
        if typeID == 14:
            # Insert prop_prop
            return self.restServiceUrl +"6/addFeatures"
        if typeID == 15:
            # Insert FOI_OFF
            return self.restServiceUrl +"3/addFeatures"
        if typeID == 16:
            # Insert offering
            return self.restServiceUrl +"5/addFeatures"
        if typeID == 17:
            # Insert prop_off
            return self.restServiceUrl + "7/addFeatures"
        if typeID == 18:
            # Update observation
            return self.restServiceUrl + "4/updateFeatures"
        return ""
        