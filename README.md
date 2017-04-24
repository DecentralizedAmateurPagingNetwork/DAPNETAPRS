# DAPNETAPRS
APRS Interface to display transmitters on APRS MAP

__Tasks:__
* Get transmitter status and location via curl request to DAPNET Core
* Open APRS IS connection
* Generate APRS objects with name PS-<CALLSIGN_FROM_DAPNET> (reduce to 7 letters if needed)
* Online transmitters: Active object with ``;``

Example: ``DH3WR-3>APRS,TCPIP*:;PS-DB0SDA*240909z5000.60NP00600.60E#PHG2230Testing DH3WR``
* Offline transmitters: Delete object from map with ``_``

Example: ``DH3WR-3>APRS,TCPIP*:;PS-DB0SDA*240909z5000.60NP00600.60E#PHG2230Testing DH3WR``

* Generate PHG comment according to curl transmitter data (Infos: http://www.tapr.org/pipermail/aprssig/2006-October/016629.html http://aprsisce.wikidot.com/phg

* Add owner in comment text from curl answer

Symbol is:
* Overlay ``P``
* Symbol ``#``
