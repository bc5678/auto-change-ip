# -*- codec: utf-8 -*-
import os
import re
import time
import shutil
from urllib.request import urlopen
from selenium import webdriver

vpngate_home = 'http://www.vpngate.net'

def get_file_from_http(url, dst):
	bytes_per_MB = 1024*1024
	file_name = url.split('/')[-1]
	u = urlopen(url)
	f = open(dst + '/' + file_name, 'wb')
	file_size = int(u.info()['Content-Length'])
	print('Downloading %s: %.2f MB (%d Bytes) ' % (file_name, file_size/bytes_per_MB, file_size))

	file_size_dl = 0
	block_sz = bytes_per_MB
	while (True):
		buffer = u.read(block_sz)
		if not buffer:
			break
		file_size_dl += len(buffer)
		f.write(buffer)
		status = "%10d bytes (%.2f MB) got:  [%3.2f%%]" % (file_size_dl, file_size_dl/bytes_per_MB, file_size_dl * 100. / file_size)
		status = status + chr(8)*(len(status)+1)
		print(status)
	f.close()

def refresh_list(driver):
	uncheckboxlist = ['C_SoftEther', 'C_L2TP', 'C_SSTP']
	for uncheckbox in uncheckboxlist:
		c = driver.find_element_by_id(uncheckbox)
		driver.execute_script("window.scrollBy(0, -50);")
		if c.is_selected():
			c.click()
	c = driver.find_element_by_id('C_OpenVPN')
	driver.execute_script("window.scrollBy(0, -50);")
	if not c.is_selected():
		c.click()
	button = driver.find_element_by_id('Button3')
	button.click()

def get_ovpn(driver, ovpnpages, ovpn_path):
	for page in ovpnpages:
		page = page.replace('&amp;', '&')
		driver.get(vpngate_home + '/en/' + page)
		ovpnfile_link = re.search('(/common/openvpn.+tcp_\d+.ovpn)', driver.page_source)
		if not ovpnfile_link:
			ovpnfile_link = re.search('(/common/openvpn.+udp_\d+.ovpn)', driver.page_source)
		if ovpnfile_link:
			ovpnfile_link = vpngate_home + ovpnfile_link.group(1).replace('&amp;', '&')
			get_file_from_http(ovpnfile_link, ovpn_path[0:-1])


def build_tblk(ovpn_path):
	for file in os.listdir(ovpn_path):
			if file.endswith('.ovpn'):
					print(file)
					tblk = re.match('vpngate_([0-9a-z-]+).opengw.+', file).group(1) + '.tblk'
					if not os.path.exists(ovpn_path + '/' + tblk):
							os.makedirs(ovpn_path + '/' + tblk)
							shutil.move(ovpn_path + '/' + file, ovpn_path + '/' + tblk)
					else:
							os.remove(ovpn_path + '/' + file)

def build_OVPN(ovpn_path, countries, scan_pages): 
	if os.path.exists(ovpn_path[0:-1]):
		shutil.rmtree(ovpn_path[0:-1])
	os.makedirs(ovpn_path[0:-1])

	#driver = webdriver.Safari()
	driver = webdriver.PhantomJS()
	driver.get('http://www.google.com')
	driver.maximize_window()

	for i in range(scan_pages): # refresh how many times for ovpn webpage
		driver.get(vpngate_home + '/en/')
		time.sleep(1)
		refresh_list(driver)
		ovpnpages = []
		if countries:
			for country in countries: 
				country_limit = country + '.*'
				ovpnpages += re.findall(country_limit + '(do_openvpn.aspx.+hid=\d+)', driver.page_source)
		else:
			ovpnpages += re.findall('(do_openvpn.aspx.+hid=\d+)', driver.page_source)
			
		get_ovpn(driver, ovpnpages, ovpn_path)

	driver.close()

	build_tblk(ovpn_path)
	os.system("""osascript import_tblk.scpt""")
