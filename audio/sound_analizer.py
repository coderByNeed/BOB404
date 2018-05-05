#!/usr/bin/env python
#-*- coding: utf-8 -*-
#base classes
from __future__ import absolute_import, division, print_function,with_statement
from sys import path
from os.path import dirname,abspath 
curPath = dirname( abspath( __file__ ) )
path.append(curPath)
try:
    import Tkinter as base
    from Tkinter import Tk
    from Tkinter import Canvas as canvas
except ImportError:
    import tkinter as base
    from tkinter import Tk
    from tkinter import Canvas as canvas

    

win_width,win_height=600,300
can_width,can_height= 600,260

grapher_window = Tk()
grapher_window.geometry( '{}x{}'.format(win_width,win_height) )
grapher_window.title('sound analyser')
grapher_window.resizable(width=False, height=False)
grapher_window.configure(background='#000009')

#legend

#grahing plot
graph = canvas( grapher_window, bg='#000010', highlightthickness=0, width=can_width,height=can_height)

#button to switch functionality
switch = base.Button(grapher_window,font=('Verdana',10),text='Spectrum', bg='#00001F',fg='#00292F')

#label form
l_frame = base.Frame(grapher_window,bg='#000014', width=500,height=40)

#vertical grid range changable
for x in range(5):
    height = int(((can_height-40)*x)/4)
    if height+20 != 130:
        graph.create_line( 20,20+height,570,20+height, fil='#004030',width=1,dash=(10,15) )
    else:
        graph.create_line( 20,20+height,580,20+height, fil='#FFAF2F',width=1,arrow='last')
#horisontal grid range changable
for x in range(10):
    width = int( (( can_width-55 )*x)/9 )
    if width+20 != 20:
        graph.create_line( 20+width,20,20+width,240, fil='#004030',width=1,dash=(10,20)  )
    else:
        graph.create_line(20+width,10,20+width,250, fil='#FFAF2F',width=1,arrow='both')


#main shit
graph.pack()
switch.pack(padx=20,pady=10,side='left')
l_frame.pack(side='right')
grapher_window.mainloop()
