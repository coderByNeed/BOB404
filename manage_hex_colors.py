#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals,with_statement
from sys import version

__author__ = 'Danilo Mitrovic, <adewdda@gmail.com>'
__version__ = '0.0 still in progress'

version = version[0:3] # for cross version python checking when needed 

"""
    personal convetion: 
        + = done
        - = not done
        ? = not sure, proofing needed
    
    TO DO:
:D        / figureout workarund with bigger/smaller number than a byte    +
:D        / define logic for testing/maping/filtering step                +?
:D        / convert numbers to hex strings                                +?
:D        / lowest common denominator, test and proof                     +?
:D        / lcd , make function with arguments 2 by 2 is limited          -
:D        / conversion from hex string to tuple numbers back and forth    +/- ?
:D        / generate middle color                                         +?
:D        / generate color value by step                                  -
:D        / generate color value by individual step                       -
:D        / complex math and ordinary math with color                     - # maybe color class ??? 
:D        / 

"""

within_limit = lambda x: x<=0xff and x>0x0 # :D check if number is withing values of a byte
hex_step = lambda x: x!=0 and x%5==0 # :D defining logic for necesery step
numb_to_HEX_2b = '{0:02X}'.format # :D string hexadecimal formating

def manage_data(element): # :D converts data to integer
    
    """
        converts data to integer, not to be used with containers and wrappers, individual data only
    """
    
    try:
        element= int(element) # :D checks if it is integer type
    except ValueError:
        element= element[0] if isinstance(element[0],int) else ord(element[0]) #:D checks if it is unicode or bytes cross version
    except TypeError:
        element= int(element.real) # :D complex numbers
    
    if within_limit(element): # :D if element within limit of byte
        return element
    else:
        return 0 if element <0x0 else 0xff #:D if element smaller than byte then 0, larger than 0xff
    
def standardize_Byte(element): # :D manages , so every result has at least 5 common divisor
    
    """
        step standardisation of byte order, so it can be divisible by 5
    """
    
    element = manage_data(element) # :D converts data to suitable type
    
    if hex_step(element): # :D if data is withing divisible range, then returns data
        return element
    else:
        # else, checks if data is below or above the midpoint of common divisor, and acts accordingly
        return 5*( element//5 if element%5<=2.5 else element//5+1 )

def lcd(element1,element2): # largest common denominator
    
    # :D data managment
    element1 = manage_data(element1)
    element2 = manage_data(element2)
    
    # :D sorts data per value
    max = element1 if element1<=element2 else element2
    min = element1 if max == element2 else element2
    
    # :D defining test that it shoud use
    test = lambda x: min%x==0 and max%x==0
    
    # :D filters the range of all possible solutions by 1 step, filtration by test step value
    _base = filter( test, range(1, min+1, 1 ) )
    _base = list(_base) if version == '3.5' else _base #:D  converts it to list so i can grab maximum value 
    
    #:D i could return list here, but i figure for step value ( not number value ) i should probably go with highest and save myself unecesery steps 
    
    return _base[ len(_base)-1 ] #:D  max did not work here, so did it old fashioned way, since it is sorted by filtration system

args2Hex = lambda *t: '#'+''.join( map( numb_to_HEX_2b, map( standardize_Byte, t ) ) ) #:D generates unlimited hexadecimal value in string form

def args_2_color(*args): #:D generates 3 point value system for color managment RGB
    
    if args == (): args = (0,0,0) # :D  if there are not arguments , black is default
    if len(args) == 1: args = [ args[0] ]*3 # :D if there is only 1 arugment it is coppied 3 times
    if len(args) == 2: args+=(0,) # :D if there are 2 values, 0 is added the addition looks like this since args are tuple
    if len(args) > 3: args = [ args[i] for i in range(3) ] # if larger than 3 then it limits to the first 3 indexes
    
    return args2Hex(*args) # prints out 3 byte value of hexadecimal string

def color_split(string): #:D splits color into individual values
    
    string = string.replace('#','') # :D deletes the # sign
    string = [ string[i:i+2] for i in range( len(string) ) if i%2==0 ] # :D splits it to pairs of 2
    string = map( lambda x: '0x'+x , string ) # :D adds 0x prefix ( stupid step in function but necesery )
    string = map( lambda x: int(x,16), string ) # converts it to int
    return list(string) # returns value in list... perhaps tuple more suitable
 
def colors_middle(color1,color2): # :D gets avrage middle of 2 colors
    
    if any( isinstance(xcolor, (list,tuple,int) ) for xcolor in [color1,color2] ):
        raise TypeError('not yet implemented, wait a little')
    
    color_pair = zip(*map( color_split, [color1,color2] )) # :D generates tuple of individual places for each RGB place
    middle = lambda x: int( (x[0]+x[1])/2 ) # :D small function for avraging the middle point into integer
    
    return args_2_color( *map( middle, color_pair ) ) # returns the hexadecimal string version of color
   
ca = args_2_color(125,325,129) # :D color a
cb = args_2_color(213,123,543) # :D color b

print( ca )
print( cb )
# print( colors_middle(ca,cb) )

print( colors_middle(ca,cb) )