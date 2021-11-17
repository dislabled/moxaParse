#!/usr/bin/env python3
# coding=utf-8

import telnetlib
from time import sleep
import tftpy


user = 'admin'
password = 'test'
switch_pre_ip = "192.168.127.253"
laptop_pre_ip ='192.168.127.200'
sleep_time = 0.5
fw_file = 'EDS408A_V3.8.rom'






def switch_mode_to_cli(ip):
    tn = telnetlib.Telnet(ip)
    print('Entering Ansi terminal...')
    sleep(sleep_time)
    tn.write(b'\r')                             # Press enter to use ansi terminal
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
                                                # connection closes automaticly

def switch_mode_to_menu(ip):
    tn = telnetlib.Telnet(ip)
    tn.write(b'login mode menu')

def switch_set_location(ip, location):
    tn = telnetlib.Telnet(ip)
    tn.write(b'configure')

def login(ip):
    hostname = input('Hostname: ')
    tn = telnetlib.Telnet(ip)
    tn.read_until(b'login as:')
    print('Writing Account name: {}'.format(user))
    tn.write(user.encode('ascii') + b'\n')      # Enter username
    tn.read_until(b'password:')
    print('Writing Password: {}'.format(password))
    tn.write(password.encode('ascii') + b'\n')  # Enter password
    # sleep(sleep_time)
    # tn.write(b'\n')
    tn.read_until(b'#')
    tn.write(b'configure\n')
    tn.write(b'hostname ' + hostname.encode('ascii') + b'\n')

def start_tftp_server():
    server = tftpy.TftpServer('')
    server.listen('192.168.127.200', 6969)

def switch_update_FW(ip):
    tn = telnetlib.Telnet(ip)
    tn.write(b'copy tftp device-firmware\n')
    tn.read_all()
    tn.write(laptop_pre_ip.encode('utf-8') + b'\n')
    tn.read_all()
    tn.write(fw_file.encode('utf-8') + b'\n')


if __name__ == "__main__":
    # tn = telnetlib.Telnet(switch_pre_ip)
    # tn.interact()
    # start_tftp_server()
    login(switch_pre_ip)
    # switch_set_location(switch_pre_ip, 'LOLTEST')
    # tn.read_until()
    # switch_mode_to_cli(switch_pre_ip)

# print(tn.read_all().decode('utf-8'))
# tn.read_until(b"account: ")
# tn.write(user.encode('ascii') + b"\n")
# if password:
#     tn.read_until(b"Password: ")
#     tn.write(password.encode('ascii') + b"\n")
# 
# tn.write(b"ls\n")
# tn.write(b"exit\n")
# 
# print(tn.read_all().decode('ascii'))
