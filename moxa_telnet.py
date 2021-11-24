#!/usr/bin/env python3
# coding=utf-8

"""
TODO:
    * class to keep connection
    * keep connection alive: 2min timeout
    * automate everything

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
    n = tn.expect([br'terminal type', br'login as:'], 5)
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
        tn.write(b'show interfaces ethernet\n')
        ifaceinfo = re.findall("(?<=(?:1/.{3}))\\w+", tn.read_until(b'EDS-408A-MM-SC#').decode('ascii'))
        tn.write(b'show relay-warning config\n')
        relayinfo = re.findall("(?<=(?:1/.).{10})\\w+", tn.read_until(b'EDS-408A-MM-SC#').decode('ascii'))
        sysinfo_list = re.findall('(?<=: ).*', sysinfo)
        version_list = re.findall('(?<=: ).*', version)
        print('Hostname: ' + sysinfo_list[0])
        print('FW Version: ' + version_list[1])
        counter1 = 1
        portliste = []
        for port in relayinfo:
            if port == 'Off':
                portliste.append(counter1)
            counter1 += 1
        print('porter med alarm: {}'.format(portliste))
        ifaceliste = []
        counter2 = 1
        for port in ifaceinfo:
            if port == 'Up':
                ifaceliste.append(counter2)
            counter2 += 1
        print('porter i bruk: {}'.format(ifaceliste))
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
            print('7. Change switch IP address')
            print('8. Change Name of switch')
            print('-' * 25)
            choice = input('What do you want to do: ')
            if choice == '':
                break
            if int(choice) == 1:
                p = Process(target=server.listen, args=('localhost',69))
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
                iface = input('configure which port: ')
                tn.write(b'configure\n')
                tn.read_until(b'EDS-408A-MM-SC(config)#')
                tn.write(b'interface ethernet 1/'+ iface.encode('ascii') + b'\n')
                tn.read_until(b'EDS-408A-MM-SC(config-if)#')
                config_if = input('activate(0) or deactivate(1)?: ')
                if config_if == '0':
                    tn.write(b'relay-warning event link-off\n')
                    tn.read_until(b'EDS-408A-MM-SC(config-if)#')
                    tn.write(b'exit\n')
                    tn.read_until(b'EDS-408A-MM-SC(config)#')
                    tn.write(b'exit\n')
                    tn.read_until(b'EDS-408A-MM-SC#')
                else:
                    tn.write(b'no relay-warning event link\n')
                    tn.read_until(b'EDS-408A-MM-SC(config-if)#')
                    tn.write(b'exit\n')
                    tn.read_until(b'EDS-408A-MM-SC(config)#')
                    tn.write(b'exit\n')
                    tn.read_until(b'EDS-408A-MM-SC#')
            if int(choice) == 7:
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
                tn.write(b'configure\n')
                relay_text = tn.read_until(b'EDS-408A-MM-SC(config)#')
                hostname = input('Switch Name: ')
                tn.write(b'hostname ' + hostname.encode('ascii') + b'\n')
                relay_text = tn.read_until(b'EDS-408A-MM-SC(config)#')
                tn.write(b'exit\n')
                tn.read_until(b'EDS-408A-MM-SC#')
            
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
        self.tn.write(laptop_pre_ip.encode('utf-8') + b'\n')
        self.tn.write(fw_file.encode('utf-8') + b'\n')
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
        return re.findall('(?<=: ).*', sysinfo)

    def get_version(self):
        """
        gets version info and returns it as a list
        """
        self.tn.write(b'show version\n')
        version = self.tn.read_until(b'EDS-408A-MM-SC#').decode('ascii')
        return re.findall('(?<=: ).*', version)

    def get_ifaces(self):
        """
        gets status of interfaces, and returns it as a list.
        """
        self.tn.write(b'show interfaces ethernet\n')
        return re.findall("(?<=(?:1/.{3}))\\w+", self.tn.read_until(b'EDS-408A-MM-SC#').decode('ascii'))

    def get_portconfg(self):
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
        self.tn.write(b'tftp://' + laptop_pre_ip.encode('ascii') + b'/running.ini\n')
        print(self.tn.read_until(b'Upload Ok !!!', 5.0).decode('ascii'))
        self.p.terminate()
        self.p.join()
        self.p.close()

    def get_startup_conf(self):
        """
        start tftp server async and instruct switch to upload the startup configuration
        """
        self.p.start()
        self.tn.write(b'copy startup-config tftp\n')
        self.tn.write(laptop_pre_ip.encode('ascii') + b'\n')
        self.tn.write(b'sys.ini\n')
        print(self.tn.read_until(b'Upload Ok !!!', 5.0).decode('ascii'))
        self.p.terminate()
        self.p.join()
        self.p.close()

if __name__ == "__main__":
    moxa_switch = Connection(switch_pre_ip)
    login_mode = moxa_switch.check_login()
    if login_mode[0] == 0:
        moxa_switch.menu_login()
    elif login_mode[0] == 1:
        moxa_switch.cli_login()
    else:
        print("Unknown login, exiting...")
        exit(-1)

    # while True:
    #     hostname = input('Hostname: ')
    #     switch_new_ip = input('Last 3 digits of switch ip: ')
    #     current_ip = get_ip()
    #     if current_ip == laptop_pre_ip:
    #         login(switch_pre_ip)
    #         break
    #     else:
    #         print('1. Telnet options')
    #         print('2. Change laptop ip')
    #         choice = input('>_  ')
    #         if str(choice) == '':
    #             break
    #         if int(choice) == 1:
    #             login(switch_pre_ip)
    #             break
    #         if int(choice) == 2:
    #             change_ip(laptop_pre_ip, current_ip)
