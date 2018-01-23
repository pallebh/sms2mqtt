#!/usr/bin/env python

"""
Sms2Mqtt script called by smsd(smstools) when a sms is send or received

Usage:
    sms2mqtt action filename [messageid]
"""

import logging
import logging.handlers
import json
import sys

from docopt import docopt
import paho.mqtt.client as mqttw

logger = None

def mqttpublish( number , content ) :
    address = 'localhost'
	port = 1883 , 
	id = 'sms2mqtt'
	
    client = mqttw.Client( client_id = id )
	client.connect( address , port)
    
    topic = 'sms/incoming'
	qos = 0
	retain = False

	payload = {'number' : number , 'content' : content }
	payloadjson = json.dumps( payload )

    client.publish( topic  , payloadjson , qos , retain )

def createLogger() :
    logger = logging.getLogger()
    logger.setLevel( logging.INFO )
    logFile = logging.handlers.RotatingFileHandler( "/var/log/sms2mqtt.log" , mode = "a", maxBytes = 1024*1024 , backupCount = 5  )
   
    formatter = logging.Formatter( '%(asctime)s %(module)s:%(funcName)s:%(lineno)d' , datefmt= '%m/%d/%Y %H:%M:%S' )
    
    logFile.setFormatter(formatter)
    logger.addHandler( logFile )

    logConsole = logging.StreamHandler()
    logConsole.setLevel( logging.DEBUG )
    logConsole.setFormatter(formatter)
    logger.addHandler( logConsole )


def dispatch( action , filename ):
    logger.info( 'action:{} filename:{}'.format( action , filename ) ) 
    
    dispatch = {}
    dispatch[ 'SENT' ] = sent
    dispatch[ 'RECEIVED' ] = received  
    dispatch[ 'FAILED' ] = None
    dispatch[ 'REPORT' ] = None
    dispatch[ 'CALL' ] = None

def received( filename ) :
    with open( filen , 'rb' ) as f :
        content = f.read() 
    logger.info( 'received number:{} content:{}'.format( number , content ) ) 

    mqttpublish( number , content )   

if __name__ == '__main__' :
    try :
        createlogger()
        logger = logging.getLogger( __name__ )
		arguments = docopt ( __doc__  )
        action = arguments['action']
        filename = arguments['filename']
        dispatch( action , filename )  

    except Exception as e:
        logger.error( e , exc_info = True ) 
		sys.exit( 1 )
   
    sys.exit( 0 )
