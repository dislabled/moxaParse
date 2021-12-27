#!/usr/bin/env python3
# coding=utf-8

import tkinter as tk
from tkinter import ttk
from csv import reader



# Generate Root window
root = tk.Tk()
root.title('Moxa Configurator')
root.minsize(640, 480)
# Testlabel
label = ttk.Label(root, text='test test test')
label.pack(ipadx=10, ipady=10)

# Treeview
columns = ('cab', 'sw_ip', 'loc', 'com')
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading('cab', text='Cabinet')
tree.heading('sw_ip', text='Switch IP')
tree.heading('loc', text='Location')
tree.heading('com', text='Comment')


def read_config(configfile:str) -> list:
    config = []
    with open(configfile, 'r') as file:
        csvconfig = reader(file, delimiter=',', quotechar='"')
        cnt = 0
        for row in csvconfig:
            config.append(row)
            cnt += 1
    return config
print(read_config('config.csv'))

# Start the main loop
root.mainloop()
