#!/usr/bin/env python3
# coding=utf-8



import tftpy
from requests_html import HTMLSession

pre_ip = "192.168.127.253"
ip = '127.0.0.1'

client = tftpy.TftpClient(ip, 69)
client.download('EDS408A_V3.8.rom', 'test.rom')


