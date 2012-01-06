'''
Created on 28 Nov 2011

@author: BERG3428
'''
import arcpy
from arcpy import env

if __name__ == '__main__':
    env.workspace = 'c:/temp/python'

    zPath = "c:/temp/python/test.shp"
    print"toto"
    pDesc = arcpy.Describe(zPath)
    # error here RuntimeError: DescribeData: Method DatasetType does not exist
    print pDesc.DatasetType

    # and here
    pExtent = pDesc.Extent


    # and here
    print "Extent of shape :\nXMin: %f, YMin: %f, \nXMax: %f, YMax: %f" % \
    (pExtent.XMin,pExtent.YMin,pExtent.XMax,pExtent.YMax)

    # and here
    pSr = pDesc.spatialReference

    print pSr.name
