#Ralf Wilke DH3WR
# First tests

import aprslib
import logging
import time
from datetime import datetime
from aprslib.packets.base import APRSPacket
from aprslib.util import latitude_to_ddm, longitude_to_ddm, comment_altitude

logging.basicConfig(level=logging.DEBUG) # level=10

# a valid passcode for the callsign is required in order to send
AIS = aprslib.IS("DH3WR", passwd="22269", port=14580)
AIS.connect()

format = 'uncompressed'
latitude = 50.01
longitude = 6.01
symbol_table = 'P'
symbol = '#'
altitude = None
comment = 'Testing DH3WR'

timestamp = datetime.utcfromtimestamp(time.time()).strftime("%d%H%M") + 'z'

phg = 'PHG2230'

body = [
    'DH3WR-3>APRS,TCPIP*:',
    ';',
    'PS-',
    'DB0SDA*',
    timestamp,
    latitude_to_ddm(latitude),
    symbol_table,
    longitude_to_ddm(longitude),
    symbol,
#    comment_altitude(altitude) if altitude is not None else '',
    phg,
    comment,
]
data = "".join(body)
print(data)
# send a single status message
#AIS.sendall('DH3WR-3>APRS,TCPIP*:;PS-DB0SDA*211330z5000.00NP00600.00E#Test')
#             DH3WR-3>APRS,TCPIP*:;211400z5000.60NP00600.60E#Testing DH3WR
AIS.sendall(data)
