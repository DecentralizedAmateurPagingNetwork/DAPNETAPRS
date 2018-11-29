#!/usr/bin/env python3
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Author: Ralf Wilke DH3WR  dh3wr atREMOVETHIS darc .REMOVETHIS de
# Author: Ronald Bouwens PE2KMV pe2kmv atREMOVETHIS gmail .REMOVETHISPART c0m
# Date: 11.05.2017
# Version 1.1

import aprslib
import logging
import time
from time import sleep
from datetime import datetime
from aprslib.packets.base import APRSPacket
from aprslib.util import latitude_to_ddm, longitude_to_ddm, comment_altitude
import urllib3
import json
import base64
import math
import sys
import configparser
import os
import MySQLdb

logging.basicConfig(filename='dapnet.log',level=logging.CRITICAL)

#assign configuration file
cfg = configparser.RawConfigParser()
try:
	#attempt to read the config file config.cfg
	config_file = os.path.join(os.path.dirname(__file__),'config.cfg')
	cfg.read(config_file)
except:
	#no luck reading the config file, write error and bail out
	logger.error('APRS script could not find / read config file')
	sys.exit(0)


#setup the logging system. Error logs are written in logfile as determined by config
logger = logging.getLogger('dapnet')
handler = logging.FileHandler(cfg.get('misc','logfile'))
logformat = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(logformat)
logger.addHandler(handler)
logger.setLevel(logging.WARNING)

#DAPNET credentials and API URL are read from config file
hampagerusername = cfg.get('user','username')
hampagerpassword = cfg.get('user','password')
hampagerurl = cfg.get('dapnet','baseurl') + cfg.get('dapnet','trxurl')

#APRS-IS credentials and settings are read from the config file
aprsisusername = cfg.get('aprsis','username')
aprsispassword = cfg.get('aprsis','password')
aprsissourcecallsign = cfg.get('aprsis','sourcecall')

#read settings to access masking database
maskserver = cfg.get('maskdb','server')
maskuser = cfg.get('maskdb','username')
maskpasswd = cfg.get('maskdb','passwd')
maskdatabase = cfg.get('maskdb','database')

#open database connection
try:
	db = MySQLdb.connect(host=maskserver,user=maskuser,passwd=maskpasswd,db=maskdatabase)
except:
	#can't connect to database, bail out
	logger.error('No connection to masking database')
	sys.exit()

#read entries from masking database
cur = db.cursor()
cur.execute("SELECT MASK_CALL FROM masktable")
excl_result = cur.fetchall()
excl_list = []
for row in excl_result:
	excl_list.append(row[0])

#create a PHG code using TRX power, antenna height and antenna gain from DAPNET data
def encodePHG (power, height, gain, dir):
	p = round(math.sqrt(power))
	if p > 9:
		p = 9
	if height <= 0:
		h = 0
	else:
	    h = round(math.log(height/10/0.3048,2))
	if h > 9:
		h = 9	
	g = round(gain)
	if g > 9:
		g = 9
	if dir <= -1:
		d = 0
	else:
		d = round(dir/45)
	if d > 9:
		d = 9
	return ('PHG' + "{:.0f}".format(p) + "{:.0f}".format(h) + "{:.0f}".format(g) + "{:.0f}".format(d))


#open the link to APRS-IS. If connnection can't be established, print warning to console, print warning to error log and bail out
AIS = aprslib.IS(aprsisusername, passwd=aprsispassword, port=14580)
try:
	AIS.connect()
except:
	print('Invalid APRS credentials')
	logger.error('Invalid APRS credentials')
	sys.exit(0)
else:
	#connection to APRS-IS has been established, now continue
	
	#create the complete URL to send to DAPNET
	http = urllib3.PoolManager()
	headers = urllib3.util.make_headers(basic_auth= hampagerusername + ':' + hampagerpassword)

try:
	#try to establish connection to DAPNET
	response = http.request('GET',hampagerurl,headers=headers)
except:
	#connection to DAPNET failed, write warning to console, write warning to error log then bail out
	print('Invalid DAPNET credentials')
	logger.error('Invalid DAPNET credentials')
	sys.exit(0)
else:
	#connection to DAPNET has been established, continue
	dapnetdata = json.loads(response.data.decode('utf-8'))

#loop through all transmitters returned in dapnetdata variable
for tx in range (0, len(dapnetdata)):
	mytx = dapnetdata[tx] #get the station call
	if (mytx['status'] == 'ONLINE') & (mytx['name'].upper() not in excl_list):
		longitude = float(mytx['longitude']) #station longitude
		latitude = float(mytx['latitude']) #station latitude
		format = 'uncompressed' #aprs coordinates format
		#pager transmitter is online, add in 'create object' symbol
		active = '*'
		symbol = '#' #green digi star - transmitter online

		callsign = mytx['name'].upper() #station call is converted into upper case
	
		# Crop callsign to 6 characters
		if len(callsign) > 6:
			callsign = callsign[:6]
		callsign = "{:<6}".format(callsign)
		symbol_table = 'P' #add in APRS symbol character
	#	symbol = '#' #add in APRS symbol
		altitude = None #don't use altitude
		comment = 'DAPNET POCSAG Transmitter(' #add comment to object
		timeSlots = mytx['timeSlot'] + ')' #extract timeslots for station
		status = '(' + mytx['status'] + ')'
		timestamp = datetime.utcfromtimestamp(time.time()).strftime("%d%H%M") + 'z'
	
		#differentiate between omnidirectonal antenna or beam
		if mytx['antennaType'] == 'OMNI':
			direction = -1 #add in string to mark 'omnidirectional'
		else:
			direction = mytx['antennaDirection'] #add in beaming direction if applicable

		#jump back and calculate PHG code with DAPNET data as input
		phg = encodePHG(float(mytx['power']),float(mytx['antennaAboveGroundLevel']),float(mytx['antennaGainDbi']),direction)
		if active == '_':
			pgh = ''
		
		#put all variables in the correct order in a list
		body = [
			aprsissourcecallsign,
			'>APRS,TCPIP*:',
			';',
			'PS-',
			callsign,
			active,
			timestamp,
			latitude_to_ddm(latitude),
			symbol_table,
			longitude_to_ddm(longitude),
			symbol,
			phg,
			comment,
			timeSlots,
			status,
		]

		#create the complete message string out of all components
		data = "".join(body)

		#transmitters with status ERROR are ignored
		try:
			AIS.sendall(data)
#			print(data) #print the APRS message string to the console
			sleep(0.3)
		except:
			#APRS string could not be sent, log error, log string then continue
			logger.error('APRS message not sent to server')
			logger.info(data)

