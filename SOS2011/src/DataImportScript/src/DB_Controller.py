'''
Created on 23 Nov 2011

@author: BERG3428
'''


import pyodbc
import arcpy

class Db_Controller:
    #connect_string = 'DRIVER={SQL Server};SERVER=tetrasql;DATABASE=envi311;UID=internetuser;PWD=y2cenow'
    connect_string = 'DRIVER={SQL Server};SERVER=localhost;DATABASE=TestIndex;UID=sa;PWD=fckfck29'
    connection = None
    

    def __init__(self):
        return
    
    def getFeatureID(self,name):
        try:
            sql = ("Select * from Test where Value = '%s' " %(name))
            self.connection = pyodbc.connect(self.connect_string)
            cursor = self.connection.cursor()
            featureList = cursor.execute(sql).fetchall()
            if len(featureList) == 0:
                return 2
                # create new feature of interest Maybe with rest instead
                #sql = ("insert into Test (Value) values '%s' " %(name))
                #cursor.execute(sql)
                #row = cursor.fetchone()
                #if row:
                #print row
                #return row.id 
            else:
                for feature in featureList:
                    return feature.ID
        except pyodbc.Error:
            print "ERROR DB"
        finally:
            if self.connection != None:
                self.connection.close()
            
        return 0    
    
    def InsertObservation(self):
        return