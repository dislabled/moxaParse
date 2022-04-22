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
                if swmainred.get() == 0:
                    if row[9] != "" and row[11] == "":
                        config.append((row[0], row[9], row[10], row[13]))
                if swmainred.get() == 1:
                    if row[9] != "" and row[12] == "":
                        config.append((row[0], row[9], row[10], str(row[13])))
            cnt += 1
    return config


def item_selected(event) -> None:
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        record = item['values']
        # show a message
        showinfo(title='Information', message=','.join(record))

def refresh() -> None:
    for entry in tree.get_children():
        tree.delete(entry)
    lollist = read_config('config.csv')
    for entry in lollist:
        tree.insert('', tk.END, values=entry)
    # Statusline
    total_count = len(tree.get_children())
    label = ttk.Label(frame2, text='Total objects: {}'.format(total_count))
    label.grid(row=0, column=0)

# Generate Root window
root = tk.Tk()
root.title('Moxa Configurator')
# root.geometry('1000x600')
# root.minsize(1920, 1080)
root.attributes('-alpha',0.8)
root.bind("<Escape>", lambda _: root.destroy())
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)

# Frame 0 BUTTONS:
frame0 = tk.Frame(root)
frame0.grid(row=0, column=0, sticky='n')

# Frame 1 TREEVIEW:
frame1 = tk.Frame(root)
frame1.grid(row=1, column=0, sticky='nsew')

# Frame 2 STATUSLINE:
frame2 = tk.Frame(root)
frame2.grid(row=2, column=0, sticky='nsew')

swmainred = tk.IntVar(value=0)

# Treeview
columns = ('cab', 'sw_ip', 'loc', 'com')
tree = ttk.Treeview(frame1, columns=columns, show='headings')
scrollbar = ttk.Scrollbar(frame1, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
tree.column('cab', width=150, anchor=tk.NW)
tree.column('sw_ip', width=150, anchor=tk.NW)
tree.column('loc', width=350, anchor=tk.NW)
tree.column('com', width=400, anchor=tk.NW)
tree.heading('cab', text='Cabinet')
tree.heading('sw_ip', text='Switch IP')
tree.heading('loc', text='Location')
tree.heading('com', text='Comment')
tree.bind('<<TreeviewSelect>>', item_selected)
tree.pack(fill=tk.BOTH, expand=1, side="left")
scrollbar.pack(fill=tk.BOTH, side="right")

# get values
refresh()

# Buttons
main_button = tk.Radiobutton(frame0, text="Main", variable=swmainred,
                            indicatoron=False, value=0, width=8, command=refresh)
red_button = tk.Radiobutton(frame0, text="Red", variable=swmainred,
                            indicatoron=False, value=1, width=8, command=refresh)
main_button.pack(side="left")
red_button.pack(side="left")




# Start the main loop
root.mainloop()
