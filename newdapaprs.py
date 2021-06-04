import aprslib
import configparser
import urllib3
import json
import sys
import math
import time
from time import sleep
from datetime import datetime
import MySQLdb
from logfunctions import *
from aprslib.util import latitude_to_ddm, longitude_to_ddm, comment_altitude

errorcalls = []

# read configuration
cfg = configparser.ConfigParser()
try:
	cfg.read('/etc/dapaprs.cfg')
	dapnet_uri = cfg.get('dapnet','baseurl') + cfg.get('dapnet','trxurl')
	mask_server = cfg.get('maskdb','server')
	mask_database = cfg.get('maskdb','database')
	mask_username = cfg.get('maskdb','username')
	mask_password = cfg.get('maskdb','passwd')
	aprsissourcecallsign = cfg.get('aprsis','sourcecall')
	aprsisuser = cfg.get('aprsis','username')
	aprsispasswd = cfg.get('aprsis','password')
except:
	logger.error('Cannot read config file')
	sys.exit(0)

# setup aprs is link
def APRSConnect(aprsisuser,aprsispassword,aprstelegram):
	try:
		ais = aprslib.IS(aprsisuser,passwd = aprsispasswd, host = 'server.pd2rld.nl' ,port = 14580)
		ais.connect()
		ais.sendall(aprstelegram)
	except:
		aprs_logger.error('Can not connect to APRS-IS')
		sys.exit(0)

# read dapnet transmitters
def GetTXData():
	try:
		http = urllib3.PoolManager()
		trxdata = http.request('GET',dapnet_uri)
		trxdata = json.loads(trxdata.data.decode('utf-8'))
		return(trxdata)
	except:
		logger.error('Cannot retrieve DAPNET transmitter data')
		sys.exit(0)

def GetMaskData():
	try:
		db = MySQLdb.connect(host=mask_server,user=mask_username,passwd=mask_password,db = mask_database)
		cur = db.cursor()
		cur.execute('SELECT MASK_CALL FROM masktable')
		mask_result = cur.fetchall()
		mask_list = []
		for row in mask_result:
			mask_list.append(row[0])
		return(mask_list)
	except:
		logger.error('Cannot connect to mask database')
		sys.exit(1)

def IsTXMasked(callsign):
	if callsign in mask_data:
		return(True)
	else:
		return(False)

def EncodePHG(power, height, gain, dir):
	p = round(math.sqrt(power))
	if p > 9:
		p = 9
	if height <= 0:
		h = 0
	else:
		h = round(math.log(height/10/0.3048,2))
	if h <= 0:
		h = 0
	if h > 9:
		h = 9
	g = round(gain)
	if g > 9:
		g = 9
	if dir <= -1:
		d = 0
	else:
		d = round(dir / 45)
	if d > 9:
		d = 9
	return ('PHG' + "{:.0f}".format(p) + "{:.0f}".format(h) + "{:.0f}".format(g) + "{:.0f}".format(d))

def LoopTx(trxdata,maskdata):
	for tx in trxdata:
		callsign = tx['name'][:7].upper()
		callsign = "{:<7}".format(callsign)
		if IsTXMasked(callsign) == False and tx['status'] == 'ONLINE':
			phg = (EncodePHG(float(tx['power']),float(tx['antennaAboveGroundLevel']),float(tx['antennaGainDbi']),float(tx['antennaDirection'])))
			latitude = latitude_to_ddm(float(tx['latitude']))
			longitude = longitude_to_ddm(float(tx['longitude']))
			timeslots = ' (' + tx['timeSlot'] + ')'
			txtype = tx['deviceType']
			timestamp = datetime.utcfromtimestamp(time.time()).strftime("%d%H%M") + 'z'

			# fix fields
			prefix = '>APRS,TCPIP*:;P-'
			activetx = '*'
			symbol = '#'
			symboltable = 'P'
			comment = 'DAPNET POCSAG TX'

			# compose message body
			body = [
				aprsissourcecallsign,
				prefix,
				callsign,
				activetx,
				timestamp,
				latitude,
				symboltable,
				longitude,
				symbol,
				phg,
				comment,
				': ',
				txtype,
				timeslots,
			]
			aprstelegram = ''.join(body)
			try:
				APRSConnect(aprsisuser,aprsispasswd,aprstelegram)
				sleep(0.1)
			except:
				errorcalls.append(tx['name'])
				print(errorcalls)
				aprs_logger.error('Can not send APRS telegram (' + aprstelegram + ')')
logger.debug('Start loop')
trxdata = GetTXData()
mask_data = GetMaskData()
LoopTx(trxdata,mask_data)
aprs_logger.error(errorcalls)
logger.debug('Loop completed')

