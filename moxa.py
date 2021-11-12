#!/usr/bin/env python3
# coding=utf-8


# 1. oppdatere firmware
# 2. skifte ip adreses
# 2. sette location til skapnavn
# 3. sjekke alarm settings



import requests
import subprocess
from requests_html import HTMLSession

ethernet_card = "enp0s31f6"
laptop_def_ip = "192.168.127.200"
laptop_new_ip = "172.16.172.200"
pre_ip = "192.168.127.253"
firmware_file = "EDS408A_V3.8.rom"
cookies = {'AccountName508': 'admin', 'sessionID': '3069018588', 'Password508': 'a5ca3184833791b4d2042acdb212f4aa', 'lasttime': '1636404960758'}
#cookies = {'AccountName508': 'admin', 'Password508': 'cc03e747a6afbbcbf8be7668acfebee5', 'lasttime': '1636378347744'}

def location():
    switch_location = input("Hvilket skap står switchen i? ")
    system_url = "http://" + pre_ip + "/goform/SwitchSystemSetting"
    system_payload = {
            'switch_name': 'Managed+Redundant+Switch+07088',
            'switch_location': switch_location,
            'switch_description': 'EDS-408A-MM-SC',
            'switch_contact': '',
            'switch_logout': '0',
            'switch_agetime': '300',
            'SystemSubmit.x': '60',
            'SystemSubmit.y': '12',
            }
    system_post = requests.post(system_url, data=system_payload, cookies=cookies)
    if system_post.status_code != 200:
        exit("Kunne ikke sette skapnavn")

def ipsettings():
    new_ip = input("Hvilken ip-adresse skal switchen ha? 172.16.172.")
    ip_url = "http://" + pre_ip + "/goform/SwitchNetworkSetting"
    ip_payload = {
            'dhcp_select': '2',
            'switch_ip': '172.16.172.' + new_ip,
            'switch_mask': '255.255.255.0',
            'switch_geteway': '',
            'switch_1stdns': '',
            'switch_2nddns': '',
            'switch_ipv6_prefix': '',
            'NetworkSubmit.x': '55',
            'NetworkSubmit.y': '15'
            }
    ip_post = requests.post(ip_url, data=ip_payload, cookies=cookies)
    if ip_post.status_code != 200:
        exit("Kunne ikke skifte ip")

def alarmsettings():
    alarm_url = "http://" + pre_ip + "/home.asp"
    alarm_url = "http://" + pre_ip + "/relay_alarm_setting.asp"
    #alarm_url = "http://" + pre_ip + "/goform/AlarmEventType"
    alarm_payload = {
            'port1_link_select': '1',
            'port1_traffic_select': '0',
            'port2_link_select': '3',
            'port2_traffic_select': '0',
            'port3_link_select': '0',
            'port3_traffic_select': '0',
            'port4_link_select': '0',
            'port4_traffic_select': '0',
            'port5_link_select': '0',
            'port5_traffic_select': '0',
            'port6_link_select': '0',
            'port6_traffic_select': '0',
            'port7_link_select': '3',
            'port7_traffic_select': '0',
            'port8_link_select': '3',
            'port8_traffic_select': '0',
            'relay1_enable': '0',
            'relay2_enable': '',
            'power1_select': '0',
            'power2_select': '0',
            'di1onoff_select': '',
            'di1offon_select': '',
            'di2onoff_select': '',
            'di2offon_select': '',
            'ringrelay_select': '0',
            } 
    # data ={'port1_link_select': ''}
    # alarm_post = requests.post(alarm_url, data=alarm_payload, cookies=cookies)
    # alarm_get = requests.get(alarm_url, data=data, cookies=cookies)
    # print(alarm_get)
    # print(data)
    # if alarm_post.status_code != 200:
    #     exit("kunne ikke endre på alarm")
    session = HTMLSession()
    r = session.get(alarm_url, cookies=cookies)
    print(r.url)
    r.html.render(reload=False)  # this call executes the js in the page
    print(r.html.text)
    print("-" * 80)
    print(r.html.search('relay1_enable'))
    # print(r.html.find('port1_link_select').text)

def firmware_update():
    files = {'binary': (firmware_file, open(firmware_file,'rb'))}
    firmware_url = 'http://' + pre_ip + '/goform/LocalFirmwareOpenFunction'
    # "Firmware Upgrade Ok."
    # "Firmware Upgrade Fail !!!"
    send_file = requests.post(firmware_url, files=files, cookies=cookies)
    print(send_file.text)

def change_ip(ip):
    get_ip = subprocess.run(["ip addr show " + ethernet_card], shell=True, capture_output=True, encoding='ascii')
    slicepos = get_ip.stdout.find('inet ')
    current_ip = ''.join(get_ip.stdout[slicepos+5:slicepos+20])
    if ip != current_ip:
        set_ip = subprocess.run(["sudo ip addr add local " + ip + "/24 broadcast " + ip[:-3] + "255 dev " + ethernet_card], shell=True)
        if set_ip.returncode == 0:
            print("IP addresse: {}".format(ip))
        else:
            print("Kunne ikke sette ip")
            exit(-1)
    else:
        print("Har allerede IP: ", current_ip)

def login_session():
    url = "http://" + pre_ip + "/auth/accountpassword.asp"
    try:
        session = HTMLSession()
        payload = {'account': 'admin', 'password': 'test', 'Loginin.x': '43', 'Loginin.y': '18'}
        r = session.post(url, data=payload)
        # r = session.get(url)
        r.html.render(reload=False)
        print(r.html.url)
        print("-" * 80)
        print(r.cookies)
        # account = login.html.search('Account')
        # print("-" * 80)
        # print(account)
        # login = session.post(url, data=payload)
        # print(login.cookies)
        # print(login.url)
        # response = session.get(url, cookies=cookies)
        # response.html.render()
        # print(response)
         
    except requests.exceptions.RequestException as e:
        print(e)


if __name__ == "__main__":

    while True:
        print()
        print("1. Sette IP addresse på laptop (192.168.127.200)")
        print("2. Oppdatere firmware på switch")
        print("3. Sette ny IP på switch (172.16.172.XXX)")
        print("4. Sette ny IP på laptop (127.16.172.200)")
        print("5. Ny beskrivelse av switchen")
        print("6. Sjekke portalarmer")
        print("7. Endre portalarmer ")
        choice = input(">_ ")
        if choice == '1':
            change_ip('192.168.127.200')
        elif choice == '2':
            firmware_update()
        elif choice == '3':
            ipsettings()
        elif choice == '4':
            change_ip('172.16.172.200')
        elif choice == '5':
            location()
        elif choice == '6':
            alarmsettings()
        elif choice == '7':
            pass
        elif choice == '8':
            login_session()
            #alarmsettings()
        else:
            break

