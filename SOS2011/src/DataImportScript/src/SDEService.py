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
        return
    
    def getOffering(self,offeringObj):
        row = None
        rows = None
        sdeConn = None
        try:
           
            sdeConn = arcpy.ArcSDESQLExecute(self.sp.getFullPath())
            sql = "select top(1) * from dbo.Offering where OFFERING_NAME='"+str(offeringObj.name)+"'"
            rows = sdeConn.execute(sql)
            result = None
            if isinstance(rows, list):
                for row in rows:
                    result = row[0] if (row[0] != None) else None
            return result
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            print pymsg
            return -1
        finally:
            if row:
                del row
            if rows:
                del rows
            if sdeConn:
                del sdeConn 
            
    def getProperty(self,propertyObj):
        row = None
        rows = None
        sdeConn = None
        try:
            
            sdeConn = arcpy.ArcSDESQLExecute(self.sp.getFullPath())
            sql = "select top(1) * from dbo.Property where PROPERTY_DESCRIPTION='"+str(propertyObj.prop_desc)+"'"
            rows = sdeConn.execute(sql)
            result = None
            if isinstance(rows, list):
                for row in rows:
                    result = row[0] if (row[0] != None) else None
            return result
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            print pymsg
            return -1
        finally:
            if row:
                del row
            if rows:
                del rows
            if sdeConn:
                del sdeConn 
    
    def checkProp_Proc(self,procedureObj):
        row = None
        rows = None
        sdeConn = None
        try:
            sdeConn = arcpy.ArcSDESQLExecute(self.sp.getFullPath())
            sql = "select top(1) * from dbo.Proc_prop where PROPERTY_ID = '"+str(procedureObj.property_id)+"' AND PROCEDURE_ID='"+str(procedureObj.procedure_id)+"'"
        
            rows = sdeConn.execute(sql)
            result = None
            if isinstance(rows, list):
                for row in rows:
                    result = row[0] if (row[0] != None) else None
            return result
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            print pymsg
            return -1
        finally:
            if row:
                del row
            if rows:
                del rows
            if sdeConn:
                del sdeConn 
        
        
    def getProcedure(self,procedureObj):
        row = None
        rows = None
        try:
            query = "UNIQUE_ID='"+str(procedureObj.unique_id)+"'" 
            shapefieldname ="geometry"
            desc = arcpy.Describe(self.sp.getTPath("t_procedure"))
            shapefieldname = desc.ShapeFieldName
            del desc
            
            rows = arcpy.SearchCursor(self.sp.getTPath("t_procedure"),query)
            temp = Procedure.Procedure()
            for row in rows:
                objID = row.getValue("OBJECTID")
                temp.procedure_id = objID
                # Create the geometry object
                feat = row.getValue(shapefieldname)
                # For each point in the multipoint feature,
                for pnt in feat:
                    temp.x = pnt.X
                    temp.y = pnt.Y
                return temp
            return None
        except:
            return -1
        finally:
            if row:
                del row
            if rows:
                del rows
    
    def getFeature(self,featureObj):
        row = None
        rows = None
        try:
            query = "NAME = '"+str(featureObj.name)+"'"    
            rows = arcpy.SearchCursor(self.sp.getTPath("t_feature"),query)
            temp = FeatureOfInterest.FeatureOfInterest()
            for row in rows:
                objID = row.getValue("OBJECTID")
                temp.featureID = objID
                return temp
            return None
        except:
            return -1
        finally:
            if row:
                del row
            if rows:
                del rows
    
    def checkProp_Off(self,observationObj):
        row = None
        rows = None
        sdeConn = None
        try:   
            sdeConn = arcpy.ArcSDESQLExecute(self.sp.getFullPath())
            sql = "select top(1) * from dbo.Prop_Off where PROPERTY_ID = '"+str(observationObj.property_id)+"' AND OFFERING_ID ='"+str(observationObj.offering_id)+"'"
            rows = sdeConn.execute(sql) 
            result = None
            if isinstance(rows, list):
                for row in rows:
                    result = row[0] if (row[0] != None) else None
            return result
        except:
            return -1
        finally:
            if row:
                del row
            if rows:
                del rows
            if sdeConn:
                del sdeConn 
     
    def checkFoi_Off(self,featureObj):    
        row = None
        rows = None
        sdeConn = None
        try:
            sdeConn = arcpy.ArcSDESQLExecute(self.sp.getFullPath())
            sql = "select top(1) * from dbo.Foi_Off where FOI_ID = '"+str(featureObj.featureID)+"' AND OFFERING_ID ='"+str(featureObj.offering_id)+"'"
            rows = sdeConn.execute(sql)
            
            result = None
            if isinstance(rows, list):
                for row in rows:
                    result = row[0] if (row[0] != None) else None
            return result
        except:
            return -1
        finally:
            if row:
                del row
            if rows:
                del rows
            if sdeConn:
                del sdeConn 
     
    def checkObservation(self,observationObj):
        row = None
        rows = None
        sdeConn = None
        try:
            sdeConn = arcpy.ArcSDESQLExecute(self.sp.getFullPath())
            sql = "select top(1) OBJECTID,NUMERIC_VALUE from dbo.Observation where PROPERTY='"+str(observationObj.property_ref.property_id)+"' and OFFERING='"+str(observationObj.offering_id)+"' and PROCEDURE_='"+str(observationObj.procedure_ref.procedure_id)+"' and FEATURE='"+str(observationObj.feature_ref.featureID)+"' and TIME_STAMP='"+observationObj.time_stamp+"' and TIME_STAMP_BEGIN='"+observationObj.time_stamp_begin+"'"   
            rows = sdeConn.execute(sql)
            
            tempObj = Observation.Observation()
            if isinstance(rows, list):
                for row in rows:
                    tempObj.objectID = row[0] if (row[0] != None) else -1
                    tempObj.numeric_value = row[1] if (row[1] != None) else 0
            else:
                tempObj.objectID =  -1
                tempObj.numeric_value = 0
            return tempObj
        except:
            return None
        finally:
            if row:
                del row
            if rows:
                del rows
            if sdeConn:
                del sdeConn 
        
    def createNewProc_Prop(self,procedureObj):
        row = None
        insert_cs = None  
        sdeConn = None
        try:  
            # Gets the full table path by calling the sdeProperties function getTPath('Tablereferencename')
            insert_cs = arcpy.InsertCursor(self.sp.getTPath('t_proc_prop'))
            row = insert_cs.newRow() 
            row.setValue("PROCEDURE_ID",str(procedureObj.procedure_id))
            row.setValue("PROPERTY_ID",str(procedureObj.property_id))
            insert_cs.insertRow(row)
             
            # Getting New ID
            sdeConn = arcpy.ArcSDESQLExecute(self.sp.getFullPath())
            sql = "select top(1) OBJECTID from dbo.Proc_prop where PROCEDURE_ID = '"+str(procedureObj.procedure_id)+"' and PROPERTY_ID = '"+str(procedureObj.property_id)+"'" 
            newid = sdeConn.execute(sql)
            return newid
        except:
            return 0
        finally:
            if row:
                del row
            if insert_cs:
                del insert_cs
            if sdeConn:
                del sdeConn 
    
    def createNewProp_OFF(self,observationObj):
        row = None
        insert_cs = None  
        sdeConn = None
        try:   
            # Gets the full table path by calling the sdeProperties function getTPath('Tablereferencename')
            insert_cs = arcpy.InsertCursor(self.sp.getTPath('t_prop_off'))
            row = insert_cs.newRow() 
            row.setValue("OFFERING_ID",str(observationObj.offering_id))
            row.setValue("PROPERTY_ID",str(observationObj.property_id))
            insert_cs.insertRow(row)
             
            # Getting New ID
            sdeConn = arcpy.ArcSDESQLExecute(self.sp.getFullPath())
            sql = "select top(1) OBJECTID from dbo.Prop_Off where PROPERTY_ID = '"+str(observationObj.property_id)+"' and OFFERING_ID = '"+str(observationObj.offering_id)+"'" 
            newid = sdeConn.execute(sql)
            return newid
        except:
            return None
        finally:
            if row:
                del row
            if insert_cs:
                del insert_cs
            if sdeConn:
                del sdeConn
    
    def createNewFoi_Off(self,featureObj):
        row = None
        insert_cs = None  
        sdeConn = None
        try:
            # Gets the full table path by calling the sdeProperties function getTPath('Tablereferencename')
            insert_cs = arcpy.InsertCursor(self.sp.getTPath('t_foi_off'))
            row = insert_cs.newRow() 
            row.setValue("FOI_ID",str(featureObj.featureID))
            row.setValue("OFFERING_ID",str(featureObj.offering_id))
            insert_cs.insertRow(row)
             
            # Getting New ID
            sdeConn = arcpy.ArcSDESQLExecute(self.sp.getFullPath())
            sql = "select top(1) OBJECTID from dbo.Foi_Off where FOI_ID = '"+str(featureObj.featureID)+"' and OFFERING_ID = '"+str(featureObj.offering_id)+"'" 
            newid = sdeConn.execute(sql)
            return newid
        except:
            return None
        finally:
            if row:
                del row
            if insert_cs:
                del insert_cs
            if sdeConn:
                del sdeConn
                
    def createNewOffering(self,offeringObj):
        row = None
        insert_cs = None  
        sdeConn = None
        try:   
            # Gets the full table path by calling the sdeProperties function getTPath('Tablereferencename')
            insert_cs = arcpy.InsertCursor(self.sp.getTPath('t_offering'))
            row = insert_cs.newRow() 
            row.setValue("OFFERING_NAME",str(offeringObj.name))
            row.setValue("PROCEDURE_",str(offeringObj.procedure_id))
            row.setValue("SERVICE",str(offeringObj.service_id))
            
            insert_cs.insertRow(row)
             
            # Getting New ID
            sdeConn = arcpy.ArcSDESQLExecute(self.sp.getFullPath())
            sql = "select top(1) OBJECTID from dbo.Offering where OFFERING_NAME = '"+str(offeringObj.name)+"' and PROCEDURE_ = '"+str(offeringObj.procedure_id)+"' and SERVICE ='"+ str(offeringObj.service_id) +"'" 
            newid = sdeConn.execute(sql)
            return newid
        except:
            return None
        finally:
            if row:
                del row
            if insert_cs:
                del insert_cs
            if sdeConn:
                del sdeConn
                
    def createNewProcedure(self,procedureObj):
        row = None
        insert_cs = None  
        sdeConn = None
        array_container = arcpy.Array()
        try:

            point_object = arcpy.Point()
            point_object.X = procedureObj.x
            point_object.Y = procedureObj.y
            print ""+str(point_object.X)+ " " + str(point_object.Y) 
            array_container.add(point_object) #put first point in container
            desc = arcpy.Describe(self.sp.getTPath('t_procedure'))
            shapefieldname = desc.ShapeFieldName
            del desc
            print shapefieldname
            insert_cs = arcpy.InsertCursor(self.sp.getTPath('t_procedure'))
            row = insert_cs.newRow() 
            row.setValue("LONG_NAME",str(procedureObj.longname))
            row.setValue("UNIQUE_ID",str(procedureObj.unique_id))
            row.setValue("INTENDED_APPLICATION","")
            row.setValue("CONTACT",None)
            row.setValue(shapefieldname,array_container)# add multipoint
            
            insert_cs.insertRow(row)
             
            # Getting New ID
            sdeConn = arcpy.ArcSDESQLExecute(self.sp.getFullPath())
            sql = "select top(1) OBJECTID from dbo.Procedure_ where UNIQUE_ID = '"+str(procedureObj.unique_id)+"' and LONG_NAME = '"+str(procedureObj.longname)+"'" 
            newid = sdeConn.execute(sql)
            return newid
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            print pymsg
            return None
        finally:  
            if row:
                del row
            if insert_cs:
                del insert_cs
            if sdeConn:
                del sdeConn
            if array_container:
                del array_container
                
    def createNewFeature(self,featureObj):
        row = None
        insert_cs = None  
        sdeConn = None
        try:
            
            
            point_object = arcpy.Point()
            point_object.X = featureObj.x
            point_object.Y = featureObj.y
            
            desc = arcpy.Describe(self.sp.getTPath('t_feature'))
            shapefieldname = desc.ShapeFieldName
            del desc
            
            insert_cs = arcpy.InsertCursor(self.sp.getTPath('t_feature'))
            row = insert_cs.newRow() 
            row.setValue("NAME",str(featureObj.name))
            row.setValue("DESCRIPTION",str(featureObj.description))
            row.setValue("ID_VALUE",str(featureObj.id_value))
            row.setValue("CODE_SPACE",str(featureObj.code_space))
            row.setValue("SAMPLED_FEATURE_URL",str(featureObj.sampled_feature_url))
            row.setValue(shapefieldname,point_object)# add point
            
            insert_cs.insertRow(row)
             
            # Getting New ID
            sdeConn = arcpy.ArcSDESQLExecute(self.sp.getFullPath())
            sql = "select top(1) OBJECTID from dbo.Feature where NAME = '"+str(featureObj.name)+"'" 
            newid = sdeConn.execute(sql)
            return newid
        except:
            return None
        finally:  
            if row:
                del row
            if insert_cs:
                del insert_cs
            if sdeConn:
                del sdeConn
                
    def createNewObservation(self,observationObj):
        row = None
        insert_cs = None  
        sdeConn = None
        try:    
            
            insert_cs = arcpy.InsertCursor(self.sp.getTPath('t_observation'))
            row = insert_cs.newRow() 
            row.setValue("UNIT_OF_MEASURE",str(observationObj.unit_of_measure))
            row.setValue("TEXT_VALUE","")
            row.setValue("NUMERIC_VALUE", observationObj.numeric_value)
            # A SQL server trigger is used to update these fields
            #newObservation[0][u'attributes']['TIME_STAMP'] = 
            #newObservation[0][u'attributes']['TIME_STAMP_BEGIN'] = 
            row.setValue("TIME_STAMP_TEXT",observationObj.time_stamp)
            row.setValue("TIME_STAMP_BEGIN_TEXT",observationObj.time_stamp_begin)
            row.setValue("PROPERTY",observationObj.property_ref.property_id)
            row.setValue("PROCEDURE_",observationObj.procedure_ref.procedure_id)
            row.setValue("FEATURE",observationObj.feature_ref.featureID)
            row.setValue("OFFERING",observationObj.offering_id)
            
            insert_cs.insertRow(row)
             
            # Getting New obejct ID
            sdeConn = arcpy.ArcSDESQLExecute(self.sp.getFullPath())
            sql = "select top(1) OBJECTID from dbo.Observation where PROCEDURE_ = '"+str(observationObj.procedure_ref.procedure_id)+"' AND FEATURE = '"+str(observationObj.feature_ref.featureID)+"' AND OFFERING='"+str(observationObj.offering_id)+"' AND PROPERTY='"+str(observationObj.property_ref.property_id)+"' and TIME_STAMP_TEXT='"+observationObj.time_stamp+"' and TIME_STAMP_BEGIN_TEXT='"+observationObj.time_stamp_begin+"'" 
            newid = sdeConn.execute(sql)
            return newid
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            print pymsg
            return None
        finally:  
            if row:
                del row
            if insert_cs:
                del insert_cs
            if sdeConn:
                del sdeConn
                
    def updateObservation(self,observationObj):
        row = None
        update_cs = None
        try:
          
            qWhere = " OBJECTID = '"+str(observationObj.objectID)+"' and PROCEDURE_ = '"+str(observationObj.procedure_ref.procedure_id)+"' AND FEATURE = '"+str(observationObj.feature_ref.featureID)+"'"
            update_cs = arcpy.UpdateCursor(self.sp.getTPath('t_observation'),qWhere)
            for row in update_cs:
                row.setValue("NUMERIC_VALUE", observationObj.numeric_value)
                row.setValue("TEXT_VALUE","")
                update_cs.updateRow(row)
            return observationObj.objectID
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            print pymsg
            return None
        finally:  
            if row:
                del row
            if update_cs:
                del update_cs