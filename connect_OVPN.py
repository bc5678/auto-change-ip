import os
import time
import get_ip


def connect(ovpn_path, wait_connect_time, ip_maintain_time):
	while True:
		try:
			original_ip = get_ip.get_ip()
			if (original_ip != '0.0.0.0'):
				break
		except:
			continue

	for folder in os.listdir(ovpn_path):
		cmd = '''osascript -e "tell application \\"Tunnelblick\\"" -e "connect \\"''' + folder[0:-5] + '''\\"" -e "end tell" > /dev/null'''
		os.system(cmd)
		connection_time = 0
		while True:
			time.sleep(3)
			connection_time += 3
			if (connection_time >= wait_connect_time):
				break
			try:
				new_ip = get_ip.get_ip()
				if (new_ip != '0.0.0.0') and (new_ip != original_ip):
					break
			except KeyboardInterrupt:
				raise
			except:
				continue
		if original_ip != new_ip:
			print(new_ip)
			time.sleep(ip_maintain_time)
		cmd = '''osascript -e "tell application \\"Tunnelblick\\"" -e "disconnect all" -e "end tell" > /dev/null'''
		os.system(cmd)
		time.sleep(3)
		cmd = 'killall Tunnelblick'
		os.system(cmd)
		time.sleep(2)
