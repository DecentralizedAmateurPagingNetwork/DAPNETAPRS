import configparser
import urllib3
import json
import sys
import math
import MySQLdb
from logfunctions import *

# read configuration
cfg = configparser.ConfigParser()
try:
	cfg.read('/etc/dapaprs.cfg')
	dapnet_uri = cfg.get('dapnet','baseurl') + cfg.get('dapnet','trxurl')
	mask_server = cfg.get('maskdb','server')
	mask_database = cfg.get('maskdb','database')
	mask_username = cfg.get('maskdb','username')
	mask_password = cfg.get('maskdb','passwd')
except:
	logger.error('Cannot read config file')
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

trxdata = GetTXData()
mask_data = GetMaskData()
for tx in trxdata:
	phg = (EncodePHG(float(tx['power']),float(tx['antennaAboveGroundLevel']),float(tx['antennaGainDbi']),float(tx['antennaDirection'])))

