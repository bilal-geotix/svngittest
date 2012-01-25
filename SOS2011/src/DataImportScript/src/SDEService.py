'''
Created on 25 Jan 2012

@author: Thomas
'''
import arcpy
from sdeProperties import sdeProp
import sys
import traceback
import Procedure
import FeatureOfInterest
import Observation


class SDEService():
    
    def __init__(self):
        self.sp = sdeProp()
        #prop = sp.getSdeProperties()
        #fields = sp.getFields()
        return
    
    def getOffering(self,offeringObj):
        row = None
        try:
           
            sdeConn = arcpy.ArcSDESQLExecute(self.sp.getFullPath())
            sql = "select top(1) * from dbo.Offering where OFFERING_NAME='"+str(offeringObj.name)+"'"
           
            try:
                sdeReturn = sdeConn.execute(sql)
            except Exception:
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]
                pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
                print pymsg  
                return -1
            result = None
            if isinstance(sdeReturn, list):
                for row in sdeReturn:
                    result = row[0] if (row[0] != None) else None
            del row,sdeReturn
            return result
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            print pymsg
            del row
            return -1
            
    def getProperty(self,propertyObj):
        row = None
        try:
            sdeConn = arcpy.ArcSDESQLExecute(self.sp.getFullPath())
            sql = "select top(1) * from dbo.Property where PROPERTY_DESCRIPTION='"+str(propertyObj.prop_desc)+"'"
            
            try:
                sdeReturn = sdeConn.execute(sql)
            except Exception:
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]
                pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
                print pymsg  
                return -1
            # for holdning objectID
            result = None
            if isinstance(sdeReturn, list):
                for row in sdeReturn:
                    result = row[0] if (row[0] != None) else None
            del row,sdeReturn
            return result
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            print pymsg
            del row
            return -1
    
    def checkProp_Proc(self,procedureObj):
        
        row = None
        try:
            sdeConn = arcpy.ArcSDESQLExecute(self.sp.getFullPath())
            sql = "select top(1) * from dbo.Proc_prop where PROPERTY_ID = '"+str(procedureObj.property_id)+"' AND PROCEDURE_ID='"+str(procedureObj.procedure_id)+"'"
            try:
                sdeReturn = sdeConn.execute(sql)
            except Exception:
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]
                pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
                print pymsg  
                return -1
            result = None
            if isinstance(sdeReturn, list):
                for row in sdeReturn:
                    result = row[0] if (row[0] != None) else None
            del row,sdeReturn
            return result
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            print pymsg
            del row
            return -1
        
    def getProcedure(self,procedureObj):
        query = "UNIQUE_ID='"+str(procedureObj.unique_id)+"'" 
        rows = None
        shapefieldname ="geometry"
        try:
            try:
                desc = arcpy.Describe(self.sp.getTPath("t_procedure"))
                shapefieldname = desc.ShapeFieldName
                del desc
                rows = arcpy.SearchCursor(self.sp.getTPath("t_procedure"),query)
            except Exception:
                del rows
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]
                pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
                print pymsg  
                return -1
            temp = Procedure.Procedure()
            for row in rows:
                objID = row.getValue("OBJECTID")
                temp.procedure_id = objID
                # Create the geometry object
                feat = row.getValue(shapefieldname)
                # For each point in the multipoint feature,
                for pnt in feat:
                    # Maybe the point should be change
                    temp.x = pnt.X
                    temp.y = pnt.Y
                return temp
            del rows
            return None
        except:
            del rows
            return -1
    
    def getFeature(self,featureObj):
        query = "NAME = '"+str(featureObj.name)+"'" 
        rows = None
        #shapefieldname ="geometry"
        try:
            try:
                #desc = arcpy.Describe(self.sp.getTPath("t_feature"))
                #shapefieldname = desc.ShapeFieldName
                #del desc
                rows = arcpy.SearchCursor(self.sp.getTPath("t_feature"),query)
            except Exception:
                del rows
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]
                pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
                print pymsg  
                return -1
            temp = FeatureOfInterest.FeatureOfInterest()
            for row in rows:
                objID = row.getValue("OBJECTID")
                temp.featureID = objID
                return temp
            del rows
            return None
        except:
            del rows
            return -1
    
    def checkProp_Off(self,observationObj):
        
        row = None
        try:
            sdeConn = arcpy.ArcSDESQLExecute(self.sp.getFullPath())
            sql = "select top(1) * from dbo.Prop_Off where PROPERTY_ID = '"+str(observationObj.property_id)+"' AND OFFERING_ID ='"+str(observationObj.offering_id)+"'"
            try:
                sdeReturn = sdeConn.execute(sql)
            except Exception:
                del sdeConn
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]
                pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
                print pymsg  
                return -1
            result = None
            if isinstance(sdeReturn, list):
                for row in sdeReturn:
                    result = row[0] if (row[0] != None) else None
            del sdeReturn,sdeConn
            return result
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            print pymsg
            del row
            return -1
     
    def checkFoi_Off(self,featureObj):
        row = None
        try:
            sdeConn = arcpy.ArcSDESQLExecute(self.sp.getFullPath())
            sql = "select top(1) * from dbo.Foi_Off where FOI_ID = '"+str(featureObj.featureID)+"' AND OFFERING_ID ='"+str(featureObj.offering_id)+"'"
            try:
                sdeReturn = sdeConn.execute(sql)
            except Exception:
                del row,sdeConn
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]
                pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
                print pymsg  
                return -1
            result = None
            if isinstance(sdeReturn, list):
                for row in sdeReturn:
                    result = row[0] if (row[0] != None) else None
            del row,sdeReturn, sdeConn
            return result
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            print pymsg
            del row
            return -1
     
    def checkObservation(self,observationObj):
        
        row = None
        try:
            sdeConn = arcpy.ArcSDESQLExecute(self.sp.getFullPath())
            sql = "select top(1) OBJECTID,NUMERIC_VALUE from dbo.Observation where PROPERTY='"+str(observationObj.property_ref.property_id)+"' and OFFERING='"+str(observationObj.offering_id)+"' and PROCEDURE_='"+str(observationObj.procedure_ref.procedure_id)+"' and FEATURE='"+str(observationObj.feature_ref.featureID)+"' and TIME_STAMP='"+observationObj.time_stamp+"' and TIME_STAMP_BEGIN='"+observationObj.time_stamp_begin+"'"   
            try:
                sdeReturn = sdeConn.execute(sql)
                
            except Exception:
                del row, sdeConn
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]
                pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
                print pymsg  
                return None
            tempObj = Observation.Observation()
            if isinstance(sdeReturn, list):
                for row in sdeReturn:
                    tempObj.objectID = row[0] if (row[0] != None) else -1
                    tempObj.numeric_value = row[1] if (row[1] != None) else 0
            del row,sdeReturn, sdeConn
            return tempObj
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            print pymsg
            del row
            return None
        
    def createNewProc_Prop(self,procedureObj):
        try:
            row = None
            # Gets the full table path by calling the sdeProperties function getTPath('Tablereferencename')
            insert_cs = arcpy.InsertCursor(self.sp.getTPath('t_proc_prop'))
            row = insert_cs.newRow() 
            row.setValue("PROCEDURE_ID",str(procedureObj.procedure_id))
            row.setValue("PROPERTY_ID",str(procedureObj.property_id))
            insert_cs.insertRow(row)
            del insert_cs, row
            return 1
            # TODO get new ID where PROCEDURE_ID and PROPERTY_ID and return new ID
        except:
            return None
    