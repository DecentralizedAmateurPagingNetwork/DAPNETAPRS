#configuration file for DAPNETAPRS
#store this file in a safe directory, out of range of any kind of server

user = dict(
	username = "pe2kmv", #your DAPNET username
	password = "ronald123", #your DAPNET password
	datenotation = 'nl' #date notation (for weather messages)
)

dapnet = dict(
	callsign = 'pa-weather', #target callsign for weather messages
	transmittergrp = 'pa-all', #transmittergroup for weather messages
	baseurl = 'http://www.hampager.de:8080', #base url of DAPNET API
	coreurl = '/calls', #path to send calls
	trxurl = '/transmitters' #path to query transmitters
)

aprsis = dict(
	username = "pe2kmv", #APRS-IS callsign
	password = "23738", #APRS-IS pass code
	sourcecall = "PE2KMV", #source call when placing objects
	apikey = "8881.Nba3ye37KpRWrA" #APRS-IS API key
)

misc = dict(
	logfile = '/var/tmp/dapnetaprs.log' #log file with full path
)
