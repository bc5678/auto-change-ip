# -*- codec: utf-8 -*-
import build_OVPN_DB
import connect_OVPN

ovpn_path = 'ovpn/'
wait_connect_time = 30 # unit: seconds. If connection could not be established during this time, then give up this VPN server
ip_maintain_time = 10 # unit: seconds. The period to stay at this IP.

#countries = [''] # A list containing indicated countries, empty means all countries
countries = ['Korea Republic of']
#countries = ['Germany']
scan_pages = 1 # How many refresh pages of www.vpngate.net will be browsed to collect VPN servers

build_OVPN_DB.build_OVPN(ovpn_path, countries, scan_pages)
connect_OVPN.connect(ovpn_path, wait_connect_time, ip_maintain_time) 
