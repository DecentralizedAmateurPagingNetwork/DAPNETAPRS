#!/usr/bin/env python
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
# Date: 25.04.2017
# Version 0.1

import aprslib
import logging
import time
from time import sleep
from datetime import datetime
from aprslib.packets.base import APRSPacket
from aprslib.util import latitude_to_ddm, longitude_to_ddm, comment_altitude
import urllib2
import json
import base64
import math

logging.basicConfig(level=logging.DEBUG) # level=10

hampagerusername = 'dh3wr'
hampagerpassword = ''
hampagerurl = "http://www.hampager.de:8080/transmitters"

aprsisusername = 'DH3WR'
aprsispassword = ''
aprsissourcecallsign = 'DB0SDA-14'


def encodePHG ( power, height, gain, dir ):
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


AIS = aprslib.IS(aprsisusername, passwd=aprsispassword, port=14580)
AIS.connect()


request = urllib2.Request(hampagerurl)
base64string = base64.b64encode('%s:%s' % (hampagerusername, hampagerpassword))
request.add_header("Authorization", "Basic %s" % base64string)
response = urllib2.urlopen(request)
dapnetdata = json.loads(response.read())
#print (dapnetdata[0])


for tx in range (0, len(dapnetdata)):
	mytx = dapnetdata[tx]
	longitude = float(mytx['longitude'])
	latitude = float(mytx['latitude'])
	format = 'uncompressed'
	if mytx['status'] == 'ONLINE':
		active = '*'
	else:
		active = '_'

	callsign = mytx['name'].upper()
	
	# Crop callsign to 6 characters
	if len(callsign) > 6:
		callsign = callsign[:6]
	callsign = "{:<6}".format(callsign)
	timeSlots = mytx['timeSlot']
	symbol_table = 'P'
	symbol = '#'
	altitude = None
	comment = 'DAPNET POCSAG Transmitter'
	timestamp = datetime.utcfromtimestamp(time.time()).strftime("%d%H%M") + 'z'

	if mytx['antennaType'] == 'OMNI':
		direction = -1
	else:
		direction = mytx['antennaDirection']

	phg = encodePHG(float(mytx['power']),float(mytx['antennaAboveGroundLevel']),float(mytx['antennaGainDbi']),direction)
	if active == '_':
		pgh = ''
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
		' Timeslots: ',
		timeSlots,
	]

	data = "".join(body)
	print(data)

	AIS.sendall(data)
	sleep(0.3)
