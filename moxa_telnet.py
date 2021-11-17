#!/usr/bin/env python3
# coding=utf-8

import telnetlib
from multiprocessing import Process
from time import sleep
import tftpy


user = 'admin'
password = ''
switch_pre_ip = "192.168.127.253"
laptop_pre_ip ='192.168.127.200'
sleep_time = 0.5
fw_file = 'EDS408A_V3.8.rom'


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
        server = tftpy.TftpServer('')
        p = Process(target=server.listen, args=(laptop_pre_ip,69))
        # ----------------------------------------------------------------------------- logged in
        while True:
            print('-' * 25)
            print('1. Update Firmware')
            print('2. Download Config')
            print('3. Upload Config')
            print('4. Set login mode to menu')
            print('-' * 25)
            choice = input('What do you want to do: ')
            if choice == '':
                break
            if int(choice) == 1:
                p.start()
                tn.write(b'copy tftp device-firmware\n')
                tn.write(laptop_pre_ip.encode('utf-8') + b'\n')
                tn.write(fw_file.encode('utf-8') + b'\n')
                print(tn.read_until(b'Download OK !!!').decode('ascii'))
                print('Switch is rebooting.')
                p.terminate()
                break
            if int(choice) == 2:
                p.start()
                tn.write(b'copy running-config tftp ')
                tn.write(b'tftp://' + laptop_pre_ip.encode('ascii') + b'/cli.ini\n')
                print(tn.read_until(b'Upload Ok !!!').decode('ascii'))
                p.terminate()
            if int(choice) == 3:
                pass
            if int(choice) == 4:
                tn.write(b'login mode menu\n')
                break

if __name__ == "__main__":
    login(switch_pre_ip)
