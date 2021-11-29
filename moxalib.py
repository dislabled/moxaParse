#!/usr/bin/env python3
# coding=utf-8

import re
import tftpy
import telnetlib
from time import sleep
from multiprocessing import Process


class Connection:
    """
    Functions on a telnet object for moxa EDS routers
    """
    def __init__(self, url:str, prompt:bytes=b'EDS-408A-MM-SC') -> None:
        self.url = url
        self.tn = telnetlib.Telnet(self.url)
        self.ts = tftpy.TftpServer('')
        self.p = Process(target=self.ts.listen, args=('0.0.0.0',69))
        self.p_end = b'#'
        self.prompt = prompt + self.p_end
        self.cprompt = prompt + b'(config)' + self.p_end
        self.iprompt = prompt + b'(config-if)' + self.p_end
        self.vprompt = prompt + b'(config-vlan)' + self.p_end
                # self.tn.read_until(b'EDS-408A-MM-SC#')
                # self.tn.read_until(b'EDS-408A-MM-SC(config)#')
                # self.tn.read_until(b'EDS-408A-MM-SC(config-if)#')
                # self.tn.read_until(b'EDS-408A-MM-SC(config-vlan)#')

    def test(self):
        print(self.prompt)
        print(self.cprompt)
        print(self.iprompt)
        print(self.vprompt)

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

    def cli_login(self, user:str='admin', password:str='') -> None:
        """ Login with cli login

        Args: 
            user (str): username, default 'admin'
            password (str): password, default ''
        """
        print('Writing Account name: {}'.format(user))
        self.tn.write(user.encode('utf-8') + b'\n')      # Enter username
        self.tn.read_until(b'password:').decode('utf-8')
        print('Writing Password: {}'.format(password))
        self.tn.write(password.encode('utf-8') + b'\n')  # Enter password
        self.tn.write('\n'.encode('utf-8'))              # Confirm popup for weak password
        self.tn.read_until(self.prompt)
        self.tn.write(b'terminal length 0\n')            # Change to unlimited length
        self.tn.read_until(b'EDS-408A-MM-SC#')

    def menu_login(self, user:str='admin', password:str='') -> None:
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

    def push_firmware(self, server_ip:str, fw_file:str) -> None:
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
        print(self.tn.read_until(b'Download OK !!!', 5.0).decode('utf-8'))
        print('Switch is rebooting.')
        self.p.terminate()
        self.p.join()
        self.p.close()

    def get_sysinfo(self) -> list:
        """ Gets system info and returns it as a list

        Returns:
            list: System parameters
                  0: System Name, 1: Switch Location,
                  2: Switch Description, 3: Maintainer Info,
                  4: MAC Address, 5: Switch Uptime
        """
        self.tn.write(b'show system\n')
        sysinfo = self.tn.read_until(self.prompt).decode('utf-8')
        return re.findall('(?<=: )(.*)\\r', sysinfo)

    def get_version(self) -> list:
        """ Gets version info and returns it as a list

        Returns:
            list: Version info
                    0: Device Model, 1: Firmware Version
        """
        self.tn.write(b'show version\n')
        version = self.tn.read_until(self.prompt).decode('utf-8')
        return re.findall('(?<=: )(.*)\\r', version.strip())

    def get_ifaces(self) -> list:
        """ Gets status of interfaces, and returns it as a list.
        
        Returns:
            list: Status of all interfaces
        """
        self.tn.write(b'show interfaces ethernet\n')
        return re.findall("(?<=(?:1/.{3}))\\w+", self.tn.read_until(self.prompt).decode('utf-8'))

    def get_portconfig(self) -> list:
        """ Gets the relay warning settings of the interfaces and returns it as a list.

        Returns:
            list: Relay warning status of all interfaces
        """
        self.tn.write(b'show relay-warning config\n')
        return re.findall("(?<=(?:1/.).{10})\\w+", self.tn.read_until(self.prompt).decode('utf-8'))

    def get_running_conf(self, server_ip:str) -> None:
        """ Start tftp server async and instruct switch to upload the running configuration

        Args:
            server_ip (str): The ip of the server which the switch should connect to
        """
        self.p.start()
        self.tn.write(b'copy running-config tftp ')
        self.tn.write(b'tftp://' + server_ip.encode('utf-8') + b'/running.ini\n')
        print(self.tn.read_until(b'Upload Ok !!!', 5.0).decode('utf-8'))
        self.p.terminate()
        self.p.join()
        self.p.close()

    def get_startup_conf(self, server_ip:str, filename:str) -> None:
        """ Start tftp server async and instruct switch to upload the startup configuration

        Args:
            server_ip (str): The ip of the server which the switch should connect to
            filename (str): The filename which is put on the tftp server
        """
        self.p.start()
        self.tn.write(b'copy startup-config tftp\n')
        self.tn.write(server_ip.encode('utf-8') + b'\n')
        self.tn.write(filename.encode('utf-8') + b'_sys.ini\n')
        print(self.tn.read_until(b'Upload Ok !!!', 5.0).decode('utf-8'))
        self.p.terminate()
        self.p.join()
        self.p.close()

    def login_change(self) -> None:
        """ Change login mode to menu """
        self.tn.write(b'login mode menu\n')

    def conf_iface(self, alarm:dict) -> None:
        """ Configures alarm for interfaces in alarmdict. value == 1 is alarm on

        Args:
            alarm (dict): key=Interface, value=enable
        """
        self.tn.write(b'configure\n')
        self.tn.read_until(self.cprompt)
        for iface in alarm:
            self.tn.write(b'interface ethernet 1/'+ str(iface).encode('utf-8') + b'\n')
            self.tn.read_until(self.iprompt)
            if alarm[iface] == 1:
                self.tn.write(b'relay-warning event link-off\n')
                self.tn.read_until(self.iprompt)
                self.tn.write(b'exit\n')
                self.tn.read_until(self.cprompt)
            else:
                self.tn.write(b'no relay-warning event link\n')
                self.tn.read_until(self.iprompt)
                self.tn.write(b'exit\n')
                self.tn.read_until(self.cprompt)
        self.tn.write(b'exit\n')
        self.tn.read_until(self.prompt)

    def conf_ip(self, ip:str) -> None:
        """ Changes the ip-address of the switch to (ip)

        Args:
            ip (str): IP Address to set
        """
        self.tn.write(b'configure\n')
        self.tn.read_until(self.cprompt)
        self.tn.write(b'interface mgmt\n')
        self.tn.read_until(self.vprompt)
        self.tn.write(b'ip address static ' +
                ip.encode('utf-8') + b' 255.255.255.0\n')
        self.tn.write(b'exit\n')
        self.tn.read_until(self.prompt)

    def conf_hostname(self, hostname:str) -> None:
        """ Changes the hostname of the switch

        Args:
            hostname (str): Hostname to switch to
        """
        self.tn.write(b'configure\n')
        self.tn.read_until(self.cprompt)
        self.tn.write(b'hostname ' + hostname.encode('utf-8') + b'\n')
        self.tn.read_until(self.cprompt)
        self.tn.write(b'exit\n')
        self.tn.read_until(self.prompt)

    def save(self) -> tuple:
        """ Saves the configuration from running to startup """
        self.tn.write(b'save\n')
        status = self.tn.expect([br'Success', br'Fail'], 5)
        self.tn.read_until(self.prompt)
        return status


if __name__ == "__main__":
    test = Connection('192.168.127.253')
    test.test()
