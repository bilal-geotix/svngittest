import sys 
import serial
import json
import urllib
import urllib2
import time
import datetime

debug = 1
debug_print = 0

comport = "\\\\.\\COM11"

# Debug print
def dprint(obj):
    if debug_print==1:
        print obj        
        
# Split serial data into a dictionary  
def parseSensorData(sd): 
    sd = sd.replace(' ', '')

    items = sd.split(';')
    dd = {}
    for item in items:
        key,value = item.split(':')
        dd[key] = value
    return dd
    
# Retreive sensorboard information
def getSensorBoard(macaddress):
    url = "http://discomap.eea.europa.eu/ArcGIS/rest/services/Internal/EEASensors_Dyna_WM/FeatureServer/1/query"
    parameters = {'f' : 'json', 'geometryType' : 'esriGeometryPoint', 'returnGeometry' : 'true', 'returnIdsOnly' : 'false', 'spatialRel' : 'esriSpatialRelIntersects' }
    
    # Retrieve MacAddress from sensor serial port
    parameters['where'] = "MacAddress = " + "'" + macaddress + "'"

    dprint(parameters)
    
    req = urllib2.Request(url, urllib.urlencode(parameters))
    
    f = urllib2.urlopen(req)
    response = f.read()
    dprint(response)
    f.close()
    
    # Parse the JSON
    b = json.loads(response)
       
    return b

# Add observation
def addObservation(board, sensordata):
    url = "http://discomap.eea.europa.eu/ArcGIS/rest/services/Internal/EEASensors_Dyna_WM/FeatureServer/0/applyEdits"
    
#    observation = [{u'geometry':{"x":1403052.2283525378,"y":7486560.715396234,"spatialReference":{"wkid":102100}},"attributes":{"Unit":"9","ObservationId":1,"SensorId":2,"ValueRaw":3,"ValueCorrected":4,"TimeStamp":1304028005000,"MacAddress":"6","Type":"7"}}]
    observation = [{u'geometry':{"x":1403052.2283525378,"y":7486560.715396234,"spatialReference":{"wkid":102100}},"attributes":{}}]
    
    # Relevant board data items for the observation
    #    board['features'][0][u'geometry']
    #    board['spatialReference']
    observation[0][u'geometry'] = board['features'][0][u'geometry']
    observation[0][u'spatialReference'] = board['spatialReference']
    
    # update observation with data from sensor
    #observation[0][u'attributes']['ObservationId'] = 100
    #observation[0][u'attributes']['SensorId'] = 200
    observation[0][u'attributes']['ValueRaw'] = float(sensordata['VAL'])
    #observation[0][u'attributes']['ValueCorrected'] = 400
    observation[0][u'attributes']['TimeStamp'] = sensordata['TS'] #1304028005000
    observation[0][u'attributes']['MacAddress'] = sensordata['MAC']
    observation[0][u'attributes']['Type'] = sensordata['TYP']   
    #observation[0][u'attributes']['Unit'] = "9"

    dprint(observation)

    parameters = {'adds' : json.dumps(observation), 'f' : 'json'}
    
    req = urllib2.Request(url, urllib.urlencode(parameters))
    
    f = urllib2.urlopen(req)
    response = f.read()
    dprint(response)
    f.close()
    
    response = json.loads(response)
    return response['addResults'][0]['success'] == True


# Main loop 
try:
    ser = serial.Serial(comport, 38400)  # open serial port
except serial.SerialException:
    print "Could not open Com port: " + comport
    sys.exit(1)

while 1:
    if debug==0:
            sd = ser.readline()   # Read line from serial port - hanging wait
    else: # use dummy data
#        sd = "#MAC: 0123456789AB; TYP: O2; VAL: 1.2345"
#        sd = "\x1b~\x00T\x80\x00}3\xa2\x00@o\xb4\x17K\x02R\x01#\x01\x00}3\xa2\x00@o\xb4\x17--hello,thisisWaspmote.MAC': '0013A200406FB417--\r\n"
        sd = "garbage--MAC: 0013A200406FB417; TYP: O2; VAL: 1.2345--garbage\r\n"
    
    # Retrieve data block
    _, _, sd = sd.partition("--")    
    sd, _, _ = sd.partition("--")
    
    print sd
    
    # Add timestamp to sensordata string
    timestamp = long(time.mktime(time.gmtime()))*1000
    sd += "; TS:" + str(timestamp)

    sensordata = parseSensorData(sd)
    dprint(sensordata)

    try:
        board = getSensorBoard(sensordata['MAC'])
        dprint(board)
        
        if board['features'] != []:
            if addObservation(board, sensordata):
                print "Added: " + str(sensordata)
            else:
                print "Could not add: " + str(sensordata) 
        else:
            print "Board not found for sensor data: " + str(sensordata)
            
    
        if debug==1:
            time.sleep(5)
    except KeyError:
        print "Could not parse sensor data: " + str(sensordata)
    
