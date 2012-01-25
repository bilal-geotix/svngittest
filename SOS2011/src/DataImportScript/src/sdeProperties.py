# coding=utf-8
import os
import arcpy

class sdeProp():
    def __init__(self):
        #===========================================================================
        # SDE Conn
        #===========================================================================
        #I use a folder called Data where I save the sde connection file
        #self.sdeconnpath = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","..","DATA"))
        
        #Dont know where you'll save yours
        self.sdeconnpath = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
        self.sp={}
        self.sp['server'] =  "tetrasql"
        self.sp['service'] =  "sde:sqlserver:tetrasql"
        self.sp['database'] =  "sos" #Databasename
        self.sp['user'] =  "sa"
        self.sp['passw'] =  "Sowannebe2"
        self.sp['name'] =  "sos_sa.sde" #Name of connectionfile
        self.sp['schema'] =  "DBO"
        self.sp['auth'] =  "DATABASE_AUTH"
        self.sp['version'] =  "SDE.DEFAULT"
        self.sp['save'] =  "SAVE_USERNAME" 
        self.sp['path'] =  self.sdeconnpath
        self.sp['fullpath'] =  os.path.join(self.sp['path'],self.sp['name'])
        self.sp['dbstart'] =  self.sp['database'] +'.'+ self.sp['schema']+'.' 
        #If the file doesn't exist the it created
        if not os.path.exists(self.sp['fullpath']):
            arcpy.CreateArcSDEConnectionFile_management(self.sp['path'], self.sp['name'], self.sp['server'], self.sp['service'], self.sp['database'], self.sp['auth'], self.sp['user'], self.sp['passw'], self.sp['save'], self.sp['version'])

#===============================================================================
# TABLES
# If you for some reason change the tabel name, it's easy to just change the reference here instead of in your code
#===============================================================================
        self.sp['t_offering'] =  "Offering"
        self.sp['t_procedure'] =  "Procedure_"
        self.sp['t_observation'] =  "Observation"
        self.sp['t_feature'] =  "Feature"
        self.sp['t_property'] =  "Property"
        self.sp['t_proc_prop'] =  "Proc_prop"
        self.sp['t_prop_off'] =  "Prop_Off"
        self.sp['t_foi_off'] =  "Foi_Off"

#===========================================================================
# Fields
# The same goes for field names	
#===========================================================================
        #offering fields
        self.fields={}
        self.fields['f_userID'] = "FK_UserID"
        self.fields['f_user_uid'] = "UserID"
        self.fields['f_user_lisys'] = "LogInSystem"
        self.fields['f_user_lisysid'] = "LogInSystemUserID"
        self.fields['f_user_nn'] = "NickName"
        self.fields['f_user_crd'] = "CreateDate"
        self.fields['f_user_lad'] = "LastActivityDate"
        
        #Language table
        self.fields['f_lang_id'] = "LanguageCode"
        #Community species table
        self.fields['f_cs_id'] = "CommunitySpeciesID"
        self.fields['f_cs_ln'] = "LatinName"
        self.fields['f_cs_tid'] = "FK_SpeciesTypeID"
        self.fields['f_cs_att'] = "FK_AttachmentListID"
        self.fields['f_cs_cid'] = "FK_CommunityID"
        self.fields['f_cs_lsid'] = "LOV_SpeciesID"
        
        #Community table
        self.fields['f_com_id'] = "CommunityID"
        self.fields['f_com_type'] = "CommunityType"
        self.fields['f_com_il'] = "InitialLanguage"
        self.fields['f_com_sh'] = "ShortName"
        self.fields['f_com_n'] = "Name"
        self.fields['f_com_url'] = "WebSiteURL"
        self.fields['f_com_desc'] = "Description"
        self.fields['f_com_crd'] = "CreateDate"
        self.fields['f_com_aac'] = "AccepAnyCommunity"
        self.fields['f_com_ovaoi'] = "OnlyVerifyAreaOfIntrest"
        self.fields['f_com_olcs'] = "OnlyListCommSpecies"
        self.fields['f_com_orum'] = "OnlyRecordUploadedMedia"
        self.fields['f_com_lad'] = "LastActivityDate"
        self.fields['f_com_isa'] = "IsActive"
        self.fields['f_com_ish'] = "IsHidden"
        self.fields['f_com_attw'] = "FK_AttachmentListID_W"
        self.fields['f_com_attm'] = "FK_AttachmentListID_M"
        
    #Function to get the sde connection properties
    def getSdeProperties(self):
        return self.sp

    #Function to get the field names
    def getFields(self):
        return self.fields
    
    #Function to get the full table path
    # c:\bla\bla2\Data\myconnectionfile.sde\database.schema.tablename
    def getTPath(self,tablename):
        return os.path.join(self.sp['fullpath'], self.sp['dbstart']+ self.sp[tablename])

    def getFullPath(self):
        return self.sp['fullpath']
    