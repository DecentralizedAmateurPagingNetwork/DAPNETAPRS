#configuration file for DAPNETAPRS
#store this file in a safe directory, out of range of any kind of server

user = dict(
	username = '', #your DAPNET username
	password = '', #your DAPNET password
	datenotation = 'nl' #date notation (for weather messages) (en/de/nl)
)

dapnet = dict(
	callsign = '', #target callsign for weather messages
	transmittergrp = '', #transmittergroup for weather messages
	baseurl = 'http://www.hampager.de:8080', #base url of DAPNET API
	coreurl = '/calls', #path to send calls
	trxurl = '/transmitters' #path to query transmitters
)

aprsis = dict(
	username = '', #APRS-IS callsign
	password = '', #APRS-IS pass code
	sourcecall = '', #source call when placing objects
	apikey = '' #APRS-IS API key
)

misc = dict(
	logfile = '/var/tmp/dapnetaprs.log' #log file with full path
)
