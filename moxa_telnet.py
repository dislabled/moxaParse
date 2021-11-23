#!/usr/bin/env python3
# coding=utf-8

import tftpy
import telnetlib
import subprocess
from time import sleep, time
from multiprocessing import Process


user = 'admin'
password = ''
sleep_time = 0.5
fw_file = 'EDS408A_V3.8.rom'
ethernet_card = "enp0s31f6"
switch_pre_ip = "192.168.127.253"
laptop_pre_ip ='192.168.127.200'

def get_ip():
    get_ip = subprocess.run(["ip addr show " + ethernet_card], shell=True, capture_output=True, encoding='ascii')
    slicepos = get_ip.stdout.find('inet ')
    current_ip = ''.join(get_ip.stdout[slicepos+5:slicepos+20])
    return current_ip

def change_ip(ip, current_ip):
    if ip != current_ip:
        # remove from last dot, not last 3 spaces in case of ip address under 100:
        set_ip = subprocess.run(["sudo ip addr add local " + ip + "/24 broadcast " + ip[:-3] + "255 dev " + ethernet_card], shell=True)
        if set_ip.returncode == 0:
            print("IP address set to: {}".format(ip))
        else:
            print("Could not set IP...")
            exit(-1)
    else:
        print("Already have IP: ", current_ip)


def login(ip):
    tn = telnetlib.Telnet(ip)
    n, match, previous_text = tn.expect([br'terminal type', br'login as:'], 5)
    if n == 0:
        # ----------------------------------------------------------------------------- change to cli
        print('Entering Ansi terminal...')
        sleep(sleep_time)
        tn.write(b'\r')                             # Press enter to use ansi terminal
        # tn.interact()
        print('Writing Account name: {}'.format(user))
        sleep(sleep_time)
        tn.write(user.encode('utf-8') + b'\n')      # Enter username
        print('Writing Password: {}'.format(password))
        sleep(sleep_time)
        tn.write(password.encode('utf-8') + b'\n')  # Enter password
        print('Command 1...')
        sleep(sleep_time)
        tn.write(b'1\n')                            # Enter menu - Basic
        print('Command 2...')
        sleep(sleep_time)
        tn.write(b'l\n')                            # Enter menu login mode
        print('Command 3...')
        sleep(sleep_time)
        tn.write(b'Y\n')                            # Enter yes to switch to CLI
        print('Restarting Connection')
        tn.close()
        sleep(3)
        login(ip)
    elif n == 1:
        # ----------------------------------------------------------------------------- normal login
        print('Writing Account name: {}'.format(user))
        tn.write(user.encode('ascii') + b'\n')      # Enter username
        tn.read_until(b'password:').decode('ascii')
        print('Writing Password: {}'.format(password))
        tn.write(password.encode('ascii') + b'\n')  # Enter password
        tn.write('\n'.encode('ascii'))
        tn.read_until(b'EDS-408A-MM-SC#')
        # ----- info:
        tn.write(b'terminal length 0\n')
        tn.read_until(b'EDS-408A-MM-SC#')
        tn.write(b'show system\n')
        sysinfo = tn.read_until(b'EDS-408A-MM-SC#').decode('ascii')
        tn.write(b'show version\n')
        version = tn.read_until(b'EDS-408A-MM-SC#').decode('ascii')
        print(sysinfo)
        print(version)
        # -----
        server = tftpy.TftpServer('')
        # ----------------------------------------------------------------------------- logged in
        while True:
            print('-' * 25)
            print('1. Update Firmware')
            print('2. Download Running Config')
            print('3. Download Startup Config')
            print('4. Upload Config')
            print('5. Set login mode to menu')
            print('6. Show relay-warnings')
            print('8. Change Name of switch')
            print('-' * 25)
            choice = input('What do you want to do: ')
            if choice == '':
                break
            if int(choice) == 1:
                p = Process(target=server.listen, args=(laptop_pre_ip,69))
                p.start()
                tn.write(b'copy tftp device-firmware\n')
                tn.write(laptop_pre_ip.encode('utf-8') + b'\n')
                tn.write(fw_file.encode('utf-8') + b'\n')
                print(tn.read_until(b'Download OK !!!', 5.0).decode('ascii'))
                print('Switch is rebooting.')
                p.terminate()
                p.join()
                p.close()
                break
            if int(choice) == 2:
                p = Process(target=server.listen, args=(laptop_pre_ip,69))
                p.start()
                tn.write(b'copy running-config tftp ')
                tn.write(b'tftp://' + laptop_pre_ip.encode('ascii') + b'/running.ini\n')
                print(tn.read_until(b'Upload Ok !!!', 5.0).decode('ascii'))
                p.terminate()
                p.join()
                p.close()
            if int(choice) == 3:
                p = Process(target=server.listen, args=(laptop_pre_ip,69))
                p.start()
                tn.write(b'copy startup-config tftp\n')
                tn.write(laptop_pre_ip.encode('ascii') + b'\n')
                tn.write(b'sys.ini\n')
                print(tn.read_until(b'Upload Ok !!!', 5.0).decode('ascii'))
                p.terminate()
                p.join()
                p.close()
            if int(choice) == 4:
                pass
            if int(choice) == 5:
                tn.write(b'login mode menu\n')
                break
            if int(choice) == 6:
                tn.write(b'terminal length 0\n')
                tn.read_until(b'EDS-408A-MM-SC#')
                tn.write(b'show relay-warning config\n')
                relay_text = tn.read_until(b'EDS-408A-MM-SC#')
                print(relay_text.decode('ascii'))
            if int(choice) == 7:
                tn.write(b'terminal length 0\n')
                tn.read_until(b'EDS-408A-MM-SC#')
                tn.write(b'configure\n')
                tn.read_until(b'EDS-408A-MM-SC(config)#')
                tn.write(b'interface mgmt\n')
                tn.read_until(b'EDS-408A-MM-SC(config-vlan)#')
                new_ip = input('Please input last digits of ip: ').encode('ascii')
                tn.write(b'ip address static 192.168.127.' + new_ip + b' 255.255.255.0\n')
                tn.write(b'exit\n')
                relay_text = tn.read_until(b'EDS-408A-MM-SC#')
                # print(relay_text)
            if int(choice) == 8:
                tn.write(b'terminal length 0\n')
                tn.read_until(b'EDS-408A-MM-SC#')
                tn.write(b'configure\n')
                relay_text = tn.read_until(b'EDS-408A-MM-SC(config)#')
                hostname = input('Switch Name: ')
                tn.write(b'hostname ' + hostname.encode('ascii') + b'\n')
                relay_text = tn.read_until(b'EDS-408A-MM-SC(config)#')
                tn.write(b'exit\n')
                tn.read_until(b'EDS-408A-MM-SC#')
            

if __name__ == "__main__":
    while True:
        current_ip = get_ip()
        if current_ip == laptop_pre_ip:
            login(switch_pre_ip)
            break
        else:
            print('1. Telnet options')
            print('2. Change laptop ip')
            choice = input('>_  ')
            if str(choice) == '':
                break
            if int(choice) == 1:
                login(switch_pre_ip)
                break
            if int(choice) == 2:
                change_ip(laptop_pre_ip, current_ip)
