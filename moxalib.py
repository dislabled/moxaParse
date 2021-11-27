#!/usr/bin/env python3
# coding=utf-8

import re
import tftpy
import telnetlib
from time import sleep
from multiprocessing import Process


class Connection:
    def __init__(self, url) -> None:
        self.url = url
        self.tn = telnetlib.Telnet(self.url)
        self.ts = tftpy.TftpServer('')
        self.p = Process(target=self.ts.listen, args=('0.0.0.0',69))

    def check_login(self):
        """ Checks if login mode is menu or cli

        Returns:
            (tuple): first element is match, second is the item matched,
                        third is the text read up until the match
                        (0 is menu, 1 is cli, -1 when nothing matched)
        Raises:
            EOFError: when connection is closed
        """
        return self.tn.expect([br'terminal type', br'login as:'], 5)

    def cli_login(self, user='admin', password=''):
        """ Login with cli login

        Args: 
            user (str): username, default 'admin'
            password (str): password, default ''
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

    def menu_login(self, user='admin', password=''):
        """ Login with menu, and change to cli login

        Args: 
            user (str): username, default 'admin'
            password (str): password, default ''
        """
        sleep_time = 0.4
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

    def push_firmware(self, server_ip, fw_file):
        """
        Starts tftp server, and instruct switch to download firmware
        closes tftp server when done

        Args:
            server_ip (str): IP Address of the tftp server
            fw_file (str): Filename to pull
        """
        self.p.start()
        self.tn.write(b'copy tftp device-firmware\n')
        self.tn.write(server_ip.encode('utf-8') + b'\n')
        self.tn.write(fw_file.encode('utf-8') + b'\n')
        print(self.tn.read_until(b'Download OK !!!', 5.0).decode('ascii'))
        print('Switch is rebooting.')
        self.p.terminate()
        self.p.join()
        self.p.close()

    def get_sysinfo(self):
        """ Gets system info and returns it as a list

        Returns:
            list: System parameters
                   0: System Name, 1: Switch Location,
                   2: Switch Description, 3: Maintainer Info,
                   4: MAC Address, 5: Switch Uptime
        """
        self.tn.write(b'show system\n')
        sysinfo = self.tn.read_until(b'EDS-408A-MM-SC#').decode('ascii')
        return re.findall('(?<=: )(.*)\\r', sysinfo)

    def get_version(self):
        """ Gets version info and returns it as a list

        Returns:
            list: Version info
                    0: Device Model, 1: Firmware Version
        """
        self.tn.write(b'show version\n')
        version = self.tn.read_until(b'EDS-408A-MM-SC#').decode('ascii')
        return re.findall('(?<=: )(.*)\\r', version.strip())

    def get_ifaces(self):
        """ Gets status of interfaces, and returns it as a list.
        
        Returns:
            list: Status of all interfaces
        """
        self.tn.write(b'show interfaces ethernet\n')
        return re.findall("(?<=(?:1/.{3}))\\w+", self.tn.read_until(b'EDS-408A-MM-SC#').decode('ascii'))

    def get_portconfig(self):
        """ Gets the relay warning settings of the interfaces and returns it as a list.

        Returns:
            list: Relay warning status of all interfaces
        """
        self.tn.write(b'show relay-warning config\n')
        return re.findall("(?<=(?:1/.).{10})\\w+", self.tn.read_until(b'EDS-408A-MM-SC#').decode('ascii'))

    def get_running_conf(self, server_ip):
        """ Start tftp server async and instruct switch to upload the running configuration

        Args:
            server_ip (str): The ip of the server which the switch should connect to
        """
        self.p.start()
        self.tn.write(b'copy running-config tftp ')
        self.tn.write(b'tftp://' + server_ip.encode('ascii') + b'/running.ini\n')
        print(self.tn.read_until(b'Upload Ok !!!', 5.0).decode('ascii'))
        self.p.terminate()
        self.p.join()
        self.p.close()

    def get_startup_conf(self, server_ip, filename):
        """ Start tftp server async and instruct switch to upload the startup configuration

        Args:
            server_ip (str): The ip of the server which the switch should connect to
            filename (str): The filename which is put on the tftp server
        """
        self.p.start()
        self.tn.write(b'copy startup-config tftp\n')
        self.tn.write(server_ip.encode('ascii') + b'\n')
        self.tn.write(filename.encode('ascii') + b'_sys.ini\n')
        print(self.tn.read_until(b'Upload Ok !!!', 5.0).decode('ascii'))
        self.p.terminate()
        self.p.join()
        self.p.close()

    def login_change(self):
        """ Change login mode to menu
        """
        self.tn.write(b'login mode menu\n')

    def conf_iface(self, alarm):
        """ Configures alarm for interfaces in alarmdict. value == 1 is alarm on

        Args:
            alarm (dict): key=Interface, value=enable
        """
        self.tn.write(b'configure\n')
        self.tn.read_until(b'EDS-408A-MM-SC(config)#')
        for iface in alarm:
            self.tn.write(b'interface ethernet 1/'+ str(iface).encode('ascii') + b'\n')
            self.tn.read_until(b'EDS-408A-MM-SC(config-if)#')
            if alarm[iface] == 1:
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
        """ Changes the ip-address of the switch to (ip)

        Args:
            ip (str): IP Address to set
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
        """ Changes the hostname of the switch

        Args:
            hostname (str): Hostname to switch to
        """
        self.tn.write(b'configure\n')
        self.tn.read_until(b'EDS-408A-MM-SC(config)#')
        self.tn.write(b'hostname ' + hostname.encode('ascii') + b'\n')
        self.tn.read_until(b'EDS-408A-MM-SC(config)#')
        self.tn.write(b'exit\n')
        self.tn.read_until(b'EDS-408A-MM-SC#')

    def save(self):
        """ Saves the configuration from running to startup
        """
        self.tn.write(b'save\n')
        status = self.tn.expect([br'Success', br'Fail'], 5)
        self.tn.read_until(b'EDS-408A-MM-SC#')
        return status
