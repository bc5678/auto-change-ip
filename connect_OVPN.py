import os
import time
import get_ip

ovpn_path = 'ovpn/'
sleep_time = 30
wait_connect_time = 30
ip_maintain_time = 30

while True:
    try:
        original_ip = get_ip.get_ip()
        if (original_ip != '0.0.0.0'):
            break
    except:
        continue

for folder in os.listdir(ovpn_path):
    cmd = '''osascript -e "tell application \\"Tunnelblick\\"" -e "connect \\"''' + folder[0:-5] + '''\\"" -e "end tell"'''
    #print(cmd)
    os.system(cmd)
    time.sleep(wait_connect_time)
    while True:
        try:
            new_ip = get_ip.get_ip()
            if (new_ip != '0.0.0.0'):
                break
        except:
            continue
    if original_ip != new_ip:
        print(new_ip)
        time.sleep(ip_maintain_time)
    cmd = '''osascript -e "tell application \\"Tunnelblick\\"" -e "disconnect all" -e "end tell"'''
    #print(cmd)
    os.system(cmd)
    time.sleep(5)
    cmd = 'killall Tunnelblick'
    os.system(cmd)
    #print(cmd)
    time.sleep(5)
