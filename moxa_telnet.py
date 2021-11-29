#!/usr/bin/env python3
# coding=utf-8

"""
TODO:
    [x] class to keep connection
    [/] keep connection alive: 2min timeout (not needed with automation)
    [x] automate everything
    [ ] get macaddress(and other info) and note switch as done in file

ACTION ORDER:
    1. Update Hostname
    2. Check and adjust port alarms if neccessary
    4. Update Firmware
    3. Change Switch IP address
"""
import subprocess
from time import sleep
from moxalib import Connection

fw_file = ['EDS408A_V3.8.rom', 3.8]
ethernet_card = 'enp0s31f6'
client_ip ='192.168.127.200'
client_ip2 = '172.168.16.200'
switch_def_ip = '192.168.127.253'
switch_new_ip_r = '172.168.16.'

def cls():
    print("\033[H\033[J", end="")

def get_ip():
    """
    get client ip and return it as a string
    """
    get_ip = subprocess.run(["ip addr show " + ethernet_card], shell=True, capture_output=True, encoding='utf-8')
    slicepos = get_ip.stdout.find('inet ')
    current_ip = ''.join(get_ip.stdout[slicepos+5:slicepos+20])
    return current_ip


def change_ip(ip, ip2):
    """
    change ip address of client to (ip)
    """
    # remove from last dot, not last 3 spaces in case of ip address under 100:
    set_ip = subprocess.run(['sudo ip addr add local ' + ip + '/24 broadcast ' + ip[:-3] + '255 dev ' + ethernet_card], shell=True)
    set_ip = subprocess.run(['sudo ip addr add local ' + ip2 + '/24 broadcast ' + ip[:-3] + '255 dev ' + ethernet_card], shell=True)
    if set_ip.returncode == 0:
        print("IP address set to: {}".format(ip))
    else:
        print("Could not set IP...")
        exit(-1)


def make_alarmdict(ifacelist, alarmlist, clientport):
    alarmdict = {}
    for i in range(len(ifacelist)):
        if i != int(clientport) -1:
            if ifacelist[i] == 'Up' and alarmlist[i] != 'Off':
                alarmdict[i+1] = 1
            elif ifacelist[i] == 'Down' and alarmlist[i] == 'Off':
                alarmdict[i+1] = 0
        else:
            alarmdict[i+1] = 0
    return alarmdict


def parse_list(list, keyword):
    """
    Parses the port/or alarmlist(list). (keyword) triggers on.
    Returns a list of active in list
    """
    cnt = 1
    ports = []
    for port in list:
        if port == keyword:
            ports.append(cnt)
        cnt += 1
    return ports


if __name__ == "__main__":
    while True:
        # -----------[ client ]---------------
        current_ip = get_ip()
        if current_ip != client_ip:
            ipchange = input('Default IP doesnt match, change? (y/n)')
            if ipchange.lower() == 'y':
                change_ip(client_ip, client_ip2)
        # -----------[ switch ]---------------
        hostname = input('Enter hostname for the switch: ')
        clientport = input('Which port is the client attached to: ')
        ip_add = input('Enter the last three digits of the new ip-address: ')
        moxa_switch = Connection(switch_def_ip)
        login_mode = moxa_switch.check_login()
        if login_mode[0] == 0:
            moxa_switch.menu_login()
            print('Reestablishing connection')
            sleep(5)
        elif login_mode[0] == -1:
            cls()
            print("Unknown login:")
            print('-'*80)
            print(login_mode[2].decode('utf-8'), end='')
            print('-'*80)
            break
        elif login_mode[0] == 1:
            moxa_switch.cli_login()
            version = moxa_switch.get_version()
            system = moxa_switch.get_sysinfo()
            portlist = parse_list(moxa_switch.get_portconfig(), 'Off')
            ifacelist = parse_list(moxa_switch.get_ifaces(), 'Up')
            print('-'*80)
            print('{:<45}{}\n{:<45}{}\n{}'.format('Switch Name: ' + system[0], 'Switch Location: ' + system[1],
                'Switch Description: ' + system[2], 'MAC Address: ' + system[4], 'Uptime: ' + system[5]))
            print('{:<45}{}'.format('Model Version: ' + version[0], 'FW Version: ' +  version[1]))
            print('{:<35}{}'.format('Interfaces configured with alarm: ', portlist))
            print('{:<35}{}'.format('Interfaces in use: ', ifacelist))
            print('-'*80)
            if input('continue? (y/n)').lower() != 'y':
                break
            print('Changing Hostname: {}'.format(hostname))
            moxa_switch.conf_hostname(hostname)
            print('Checking and setting port alarms...')
            moxa_switch.conf_iface(make_alarmdict(moxa_switch.get_ifaces(), moxa_switch.get_portconfig(), clientport))
            print('Checking for firmware updates...')
            if float(moxa_switch.get_version()[1][1:]) < fw_file[1]:
                moxa_switch.push_firmware(client_ip, fw_file[0])
                print('pushing firmware')
                print('Waiting 10s for reboot')
                sleep(10)
            print('Checking and changing IP address of switch: {}{}'.format(switch_new_ip_r, ip_add))
            if current_ip == client_ip:
                moxa_switch.conf_ip(switch_new_ip_r + ip_add)
                print('Waiting 5 seconds, then reconnect')
                sleep(5)
                with open('switch.log', 'a') as logfile:
                    moxa_switch = Connection(switch_new_ip_r + ip_add)
                    moxa_switch.cli_login()
                    if moxa_switch.save()[0] == 0:
                        system = moxa_switch.get_sysinfo()
                        version = moxa_switch.get_version()
                        portlist = parse_list(moxa_switch.get_portconfig(), 'Off')
                        ifacelist = parse_list(moxa_switch.get_ifaces(), 'Up')
                        moxa_switch.get_startup_conf(client_ip, 'configs/' + system[0])
                        logfile.write('\n' + system[4] + ' - ' + system[0] + ' - ' + switch_def_ip + ip_add + ' - DONE')
                        print('-'*80)
                        print('{:<45}{}\n{:<45}{}\n{}'.format('Switch Name: ' + system[0], 'Switch Location: ' + system[1],
                            'Switch Description: ' + system[2], 'MAC Address: ' + system[4], 'Uptime: ' + system[5]))
                        print('{:<45}{}'.format('Model Version: ' + version[0], 'FW Version: ' +  version[1]))
                        print('{:<35}{}'.format('Interfaces configured with alarm: ', portlist))
                        print('{:<35}{}'.format('Interfaces in use: ', ifacelist))
                        print('-'*80)
                    else:
                        print('Saving to eeprom failed')
            break
