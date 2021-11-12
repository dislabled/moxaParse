#!/usr/bin/env python3
# coding=utf-8

import telnetlib
from time import sleep
import os
import tftpy


user = 'admin'
password = 'test'
switch_pre_ip = "192.168.127.253"
sleep_time = 0.5
fw_file = "EDS408A_V3.8.rom"

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

def login(ip):
    tn = telnetlib.Telnet(ip)
    tn.read_until(b'login as:')
    print('Writing Account name: {}'.format(user))
    tn.write(user.encode('utf-8') + b'\n')      # Enter username
    tn.read_until(b'password:')
    print('Writing Password: {}'.format(password))
    tn.write(password.encode('utf-8') + b'\n')  # Enter password
    tn.interact()

def start_tftp_server():
    server = tftpy.TftpServer('.')
    server.listen('0.0.0.0', 6969)

if __name__ == "__main__":
    start_tftp_server()
    # login(switch_pre_ip)
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
