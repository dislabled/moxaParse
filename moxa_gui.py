<<<<<<< HEAD
#!/usr/bin/env python3
# coding=utf-8

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
# import moxalib
from csv import reader


def read_config(configfile:str) -> list:
    config = []
    with open(configfile, 'r') as file:
        csvconfig = reader(file, delimiter=',', quotechar='"')
        cnt = 0
        for row in csvconfig:
            if cnt >= 2:
                config.append((row[0], row[9], row[10], row[13]))
            cnt += 1
    return config


def item_selected(event):
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        record = item['values']
        # show a message
        showinfo(title='Information', message=','.join(record))



# Generate Root window
root = tk.Tk()
root.title('Moxa Configurator')
root.minsize(1920, 1080)
root.attributes('-alpha',0.8)
root.bind("<Escape>", lambda _: root.destroy())
# Testlabel
label = ttk.Label(root, text='test test test')
label.grid(row=0, column=0)

# Treeview
columns = ('cab', 'sw_ip', 'loc', 'com')
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.column('cab', width=150, anchor=tk.W)
tree.column('sw_ip', width=150, anchor=tk.W)
tree.column('loc', width=350, anchor=tk.W)
tree.column('com', width=400, anchor=tk.W)
tree.heading('cab', text='Cabinet')
tree.heading('sw_ip', text='Switch IP')
tree.heading('loc', text='Location')
tree.heading('com', text='Comment')

lollist = read_config('config.csv')
for entry in lollist:
    tree.insert('', tk.END, values=entry)

tree.bind('<<TreeviewSelect>>', item_selected)
tree.grid(row=0, column=0, sticky='nsew')
# add a scrollbar
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky='ns')



# Start the main loop
root.mainloop()
||||||| 10217c7
=======
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
>>>>>>> 81926934b9cb01081cd1c943c1644863b96ff5a5
