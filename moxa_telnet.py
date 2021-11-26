#!/usr/bin/env python3
# coding=utf-8

"""
TODO:
    [x] class to keep connection
    [ ] keep connection alive: 2min timeout
    [ ] automate everything
    [ ] get macaddress(and other info) and note switch as done in file

ACTION ORDER:
    1. Update Hostname
    2. Check and adjust port alarms if neccessary
    4. Update Firmware
    3. Change Switch IP address
"""
import re
import tftpy
import telnetlib
import subprocess
from time import sleep
from multiprocessing import Process

user = 'admin'
password = ''
sleep_time = 0.5
fw_file = ['EDS408A_V3.8.rom', 3.8]
ethernet_card = 'enp0s31f6'
client_ip ='192.168.127.200'
client_ip2 = '172.168.16.200'
switch_def_ip = '192.168.127.253'

def get_ip():
    """
    get client ip and return it as a string
    """
    get_ip = subprocess.run(["ip addr show " + ethernet_card], shell=True, capture_output=True, encoding='ascii')
    slicepos = get_ip.stdout.find('inet ')
    current_ip = ''.join(get_ip.stdout[slicepos+5:slicepos+20])
    print(current_ip)
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


class Connection:
    def __init__(self, url) -> None:
        self.url = url
        self.tn = telnetlib.Telnet(self.url)
        self.ts = tftpy.TftpServer('')
        self.p = Process(target=self.ts.listen, args=('0.0.0.0',69))

    def check_login(self):
        """
        checks if login mode is menu or cli
        returns 0 for menu login, 1 for cli login
        """
        return self.tn.expect([br'terminal type', br'login as:'], 5)

    def cli_login(self):
        """
        login with cli login
        """
        print('Writing Account name: {}'.format(user))
        self.tn.write(user.encode('ascii') + b'\n')      # Enter username
        self.tn.read_until(b'password:').decode('ascii')
        print('Writing Password: {}'.format(password))
        self.tn.write(password.encode('ascii') + b'\n')  # Enter password
        self.tn.write('\n'.encode('ascii'))              # Confirm popup for weak password
        self.tn.read_until(b'EDS-408A-MM-SC#')
        self.tn.write(b'terminal length 0\n')            # Change to unlimited length
        self.tn.read_until(b'EDS-408A-MM-SC#')

    def menu_login(self):
        """
        login with menu, and change to cli login
        """
        print('Entering Ansi terminal...')
        sleep(sleep_time)
        self.tn.write(b'\r')                             # Press enter to use ansi terminal
        # tn.interact()
        print('Writing Account name: {}'.format(user))
        sleep(sleep_time)
        self.tn.write(user.encode('utf-8') + b'\n')      # Enter username
        print('Writing Password: {}'.format(password))
        sleep(sleep_time)
        self.tn.write(password.encode('utf-8') + b'\n')  # Enter password
        print('Command 1...')
        sleep(sleep_time)
        self.tn.write(b'1\n')                            # Enter menu - Basic
        print('Command 2...')
        sleep(sleep_time)
        self.tn.write(b'l\n')                            # Enter menu login mode
        print('Command 3...')
        sleep(sleep_time)
        self.tn.write(b'Y\n')                            # Enter yes to switch to CLI
        print('Restarting Connection')
        self.tn.close()
        sleep(3)

    def push_firmware(self):
        """
        starts tftp server, and instruct switch to download firmware
        closes tftp server when done
        """
        self.p.start()
        self.tn.write(b'copy tftp device-firmware\n')
        self.tn.write(client_ip.encode('utf-8') + b'\n')
        self.tn.write(fw_file[0].encode('utf-8') + b'\n')
        print(self.tn.read_until(b'Download OK !!!', 5.0).decode('ascii'))
        print('Switch is rebooting.')
        self.p.terminate()
        self.p.join()
        self.p.close()

    def get_sysinfo(self):
        """
        gets system info and returns it as a list
        """
        self.tn.write(b'show system\n')
        sysinfo = self.tn.read_until(b'EDS-408A-MM-SC#').decode('ascii')
        return re.findall('(?<=: )(.*)\\r', sysinfo)

    def get_version(self):
        """
        gets version info and returns it as a list
        """
        self.tn.write(b'show version\n')
        version = self.tn.read_until(b'EDS-408A-MM-SC#').decode('ascii')
        return re.findall('(?<=: )(.*)\\r', version.strip())

    def get_ifaces(self):
        """
        gets status of interfaces, and returns it as a list.
        """
        self.tn.write(b'show interfaces ethernet\n')
        return re.findall("(?<=(?:1/.{3}))\\w+", self.tn.read_until(b'EDS-408A-MM-SC#').decode('ascii'))

    def get_portconfig(self):
        """
        gets the relay warning settings of the interfaces and returns it as a list.
        """
        self.tn.write(b'show relay-warning config\n')
        return re.findall("(?<=(?:1/.).{10})\\w+", self.tn.read_until(b'EDS-408A-MM-SC#').decode('ascii'))

    def get_running_conf(self):
        """
        start tftp server async and instruct switch to upload the running configuration
        """
        self.p.start()
        self.tn.write(b'copy running-config tftp ')
        self.tn.write(b'tftp://' + client_ip.encode('ascii') + b'/running.ini\n')
        print(self.tn.read_until(b'Upload Ok !!!', 5.0).decode('ascii'))
        self.p.terminate()
        self.p.join()
        self.p.close()

    def get_startup_conf(self, filename):
        """
        start tftp server async and instruct switch to upload the startup configuration
        """
        self.p.start()
        self.tn.write(b'copy startup-config tftp\n')
        self.tn.write(client_ip.encode('ascii') + b'\n')
        self.tn.write(filename.encode('ascii') + b'_sys.ini\n')
        print(self.tn.read_until(b'Upload Ok !!!', 5.0).decode('ascii'))
        self.p.terminate()
        self.p.join()
        self.p.close()

    def parse_info(self):
        """
        temporary function to showcase the all the info
        """
        counter1 = 1
        portliste = []
        for port in Connection.get_portconfig(self):
            if port == 'Off':
                portliste.append(counter1)
            counter1 += 1
        ifaceliste = []
        counter2 = 1
        for port in Connection.get_ifaces(self):
            if port == 'Up':
                ifaceliste.append(counter2)
            counter2 += 1
        print('{:<35}{}'.format('Interfaces configured with alarm: ', portliste))
        print('{:<35}{}'.format('Interfaces in use: ', ifaceliste))

    def login_change(self):
        """
        Change login mode to menu
        """
        self.tn.write(b'login mode menu\n')

    def conf_iface(self, alarmdict):
        """
        Configures alarm for interfaces in alarmdict. value == 1 is alarm on
        """
        self.tn.write(b'configure\n')
        self.tn.read_until(b'EDS-408A-MM-SC(config)#')
        for iface in alarmdict:
            self.tn.write(b'interface ethernet 1/'+ str(iface).encode('ascii') + b'\n')
            self.tn.read_until(b'EDS-408A-MM-SC(config-if)#')
            if alarmdict[iface] == 1:
                self.tn.write(b'relay-warning event link-off\n')
                self.tn.read_until(b'EDS-408A-MM-SC(config-if)#')
                self.tn.write(b'exit\n')
                self.tn.read_until(b'EDS-408A-MM-SC(config)#')
            else:
                self.tn.write(b'no relay-warning event link\n')
                self.tn.read_until(b'EDS-408A-MM-SC(config-if)#')
                self.tn.write(b'exit\n')
                self.tn.read_until(b'EDS-408A-MM-SC(config)#')
        self.tn.write(b'exit\n')
        self.tn.read_until(b'EDS-408A-MM-SC#')

    def conf_ip(self, ip):
        """
        Changes the ip-address of the switch to (ip)
        """
        self.tn.write(b'configure\n')
        self.tn.read_until(b'EDS-408A-MM-SC(config)#')
        self.tn.write(b'interface mgmt\n')
        self.tn.read_until(b'EDS-408A-MM-SC(config-vlan)#')
        self.tn.write(b'ip address static 172.168.16.' +
                ip.encode('ascii') + b' 255.255.255.0\n')
        self.tn.write(b'exit\n')
        self.tn.read_until(b'EDS-408A-MM-SC#')

    def conf_hostname(self, hostname):
        """
        Changes the hostname of the switch to (hostname)
        """
        self.tn.write(b'configure\n')
        self.tn.read_until(b'EDS-408A-MM-SC(config)#')
        self.tn.write(b'hostname ' + hostname.encode('ascii') + b'\n')
        self.tn.read_until(b'EDS-408A-MM-SC(config)#')
        self.tn.write(b'exit\n')
        self.tn.read_until(b'EDS-408A-MM-SC#')

    def save(self):
        self.tn.write(b'save\n')
        status = self.tn.expect([br'Success', br'Fail'], 5)
        self.tn.read_until(b'EDS-408A-MM-SC#')
        return status

def parse_list(list, keyword):
    """
    Parses the port/or alarmlist(list). (keyword) triggers on.
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
            print("Unknown login, exiting...")
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
                moxa_switch.push_firmware()
                print('pushing firmware')
                print('Waiting 10s for reboot')
                sleep(10)
            print('Checking and changing IP address of switch: {}'.format('172.168.16.'+ ip_add))
            if current_ip == client_ip:
                moxa_switch.conf_ip(ip_add)
                print('changing ip address to 172.168.16.{}'.format(ip_add))
                print('Waiting 5 seconds, then reconnect')
                sleep(5)
                with open('switch.log', 'a') as logfile:
                    moxa_switch = Connection('172.168.16.'+ ip_add)
                    moxa_switch.cli_login()
                    if moxa_switch.save()[0] == 0:
                        system = moxa_switch.get_sysinfo()
                        version = moxa_switch.get_version()
                        portlist = parse_list(moxa_switch.get_portconfig(), 'Off')
                        ifacelist = parse_list(moxa_switch.get_ifaces(), 'Up')
                        moxa_switch.get_startup_conf('configs/' + system[0])
                        logfile.write('\n' + system[4] + ' - ' + system[0] + ' - 172.168.16.' + ip_add + ' - DONE')
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
