#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals,with_statement
from sys import path
from os.path import dirname,abspath 
curPath = dirname( abspath( __file__ ) )
path.append(curPath)

__author__ = 'Danilo Mitrovic, <adewdda@gmail.com>'
__version__ = '1.0'

"""
    +/- Personal convection: 
    + done, - not done
    
        empty init to black                                             +
        implement argument and keyword argument init                    +
        implement init for cmyk,hsl,hsv ...                             +/-
        bit conversion :    
            -> 1 bit                                                    -
            -> 8 bit                                                    -
            ...
        
"""


class color(object):
    
    """
        color class is default color object that supports basic object type operands and initializes by arguments or keyword arguments
            if arguments are passed in __init__ : for every color in specific range : red,green,blue is asigned value
            if keyarguments are passed in  __init__ : for every color pair asigned value is defined if :
                    key is in RGB
                    key is in rgb
                    key is in red,green,blue
            there is specific managment system that has been implemented that converts any type of builtin data to number based data type
                for more information check color().manage_input
                for any purpouse empty initialization is default black
            str , and repr are initialized for console output only, so it can display values for tests and etc
            
            if other words color object behaves and container for color values :as container you can expect the following functions
                values, items,keys, has_key :> where key in 'red,green,blue' and value well... value of the color
            
            in general color dont support nothing else than integer values, but here float values are allowed to ease up the preccision when converting from byte per color to 2,3,4... bytes
                so _selfINT() converts all values in color to integer , does not return anything
                and _retINT() converts all values in color to integer and retuns duplicate
                
                _2hex : converts color object to hexadecimal representation:>
                        > allowed 6 digit hexadecimal : #ABCDEF in form of _2hex()
                        > allowed 3 digit hexadecimal : #FAB in form of _2hex(True) or _2hex(short=True)
                
                _2cmyk : returns cmyk color value conversion
                
                common_denominator(denominator): converts the color to the common denominator in order:
                    in order to establish formal steps for animation or any kind of transition it is easier to establish equal steps if there is common division base between objects
    """
    
    attributes = 'red,green,blue'.split(',') #:D the main is RGB
    color = 'color'
    
    def __init__(self,*args,**kwargs): # :D initialization 
        
        for xatr in self.attributes: # :D empty initialization
            setattr(self,xatr,0)
        
        if args: # :D if arguments are passed color(a,b,c)
            args = map( self.manage_input, args )
            args = tuple(args)
            
            if not len(args): pass
            elif len(args)==1:
                args = args[0]
                for xatr in self.attributes:
                    self[xatr]=args
            else:
                for i,xatr in enumerate(self.attributes):
                    try:
                        args[i]
                        self[xatr]=args[i]
                    except IndexError: pass
            
        if kwargs: # :D if keyword arguments are passsed color(a=b,c=d)
            if self.color in kwargs.keys():
                if isinstance( kwargs[self.color], (tuple,list) ):
                    self.__init__(*kwargs[self.color])
                elif isinstance( kwargs[self.color], dict ):
                    self.__init__(**kwargs[self.color])
                else:
                    self.__init__( kwargs[self.color] )
            else:
                for xatr,xval in kwargs.items():
                    if xatr in self.attributes:
                        xval = self.manage_input(xval)
                        self[xatr]=xval
               
    def __iter__(self): # :D iterator, returns tuple (xatr,xval)
        for xatr in self.attributes:
            yield xatr, self[xatr]
    
    def __next__(self): # :D next(self)
        return next(self)
    
    def __str__(self): # :D console representation
        return " , ".join( map(str, map(self.__getitem__, self.attributes) ) )
    
    def __repr__(self): # :D eval initialisation
        return 'color({})'.format( ' ' if str(self)=='0 , 0 , 0' else ' , '.join([ '{!s}={!r}'.format(*t) for t in self ]) )
    
    def manage_input(self,item): # :D converts most of builtin types to number base data types 
        if type(item).__name__ in 'int,float': pass
        if type(item).__name__ in 'bool': item = int(item)
        if type(item).__name__ in 'complex':
           from math import sqrt,pow
           item = sqrt( pow(item.imag,2) + pow(item.real,2) )
        if type(item).__name__ in 'bytes':
            if not len(item): item = len(item)
            if len(item)==1: item = item[0]
            else:
                item = item[0]
                item = ord(item)
        if type(item).__name__ in 'list,tuple':
            if not len(item): item = len(item)
            else:
                item = map( manage_data, item )
                item = list(item)
                s = int( sum(item) )
                l = int( len(item) )
                item = s/l
        if type(item).__name__ in 'str,unicode':
            item = ord( item[0] )
        if type(item).__name__ in 'dict':
            if not len(item): item = len(item)
            else:
                item = item.items()
                item = map(manage_data,item)
                item = tuple(item)
                item = manage_data(item)
        
        if not item: return 0
        if item>=0 and item <= 0xff: return item
        if item > 0xff: return 0xff
        if item <0 : return 0
    
    def manage_external(self,object): # :D manages passing argument as dict,tuple,list
        if isinstance(object,dict):
            object = color( **object )
        if isinstance( object, (list,tuple) ):
            object = color( *object )
        object = object if isinstance(object, color) else color(object)
        return object
        
    def __getitem__(self,item):
        
        """
            self[item]
        """
        
        if not item: raise LookupError('item not given')
        if item in 'RGB' or item in 'rgb' or item in self.attributes:
            if item in 'rR': item = 'red'
            if item in 'gG': item = 'green'
            if item in 'bB': item = 'blue'
            return getattr(self,item)
        else:
            raise TypeError('item not a string and item not found {} in {}'.format(item,self) )
    
    def __setitem__(self,item,value):
        
        """
            self[item]=value
        """
        
        try:
            self[item]
            value = self.manage_input(value)
            setattr(self,item,value)
        except (TypeError,LookupError):pass 
    
    def values(self): # :D returns values
        for xatr in self.attributes:
            yield self[xatr]
    
    def keys(self):  # :D returns keys
        for xatr in self.attributes:
            yield xatr
    
    def items(self):return list(self) # :D returns list of tuple pairs in form of (key,value)
    
    def has_key(self,color): # :D checks if color value at specifc key is > 0
        try:
            self[color]
            return True if self[color] else False
        except :
            return False
    
    ## boolean operands
    def __eq__(self,other):
        other = self.manage_external(other)
        return all( x[0]==x[1] for x in zip( self.values(),other.values() ) )
    def __ne__(self,other):
        return not self==other
    def __bool__(self):return sum( self.values() ) != 0
    def __lt__(self,other):
        other = self.manage_external(other)
        return sum( self.values() ) < ( sum( other.values() ) )
    def __le__(self,other):
        other = self.manage_external(other)
        return sum( self.values() ) <= ( sum( other.values() ) )
    def __gt__(self,other):
        other = self.manage_external(other)
        return sum( self.values() ) > ( sum( other.values() ) )
    def __ge__(self,other):
        other = self.manage_external(other)
        return sum( self.values() ) >= ( sum( other.values() ) )
    
    ## mathematical operands
    def __add__(self,other):
        other = self.manage_external(other)
        empty = eval( 'color()' )
        
        for xatr,xval in empty:
            empty[xatr]=other[xatr]+self[xatr]
        return empty
    def __radd__(self,other): return self.manage_external(other)+self
    def __iadd__(self,other): return self+self.manage_external(other)
    
    def __sub__(self,other):
        other = self.manage_external(other)
        empty = eval( 'color()' )
        for xatr in empty.attributes:
            empty[xatr]=self[xatr]-other[xatr]
        return empty
    def __radd__(self,other): return self.manage_external(other)-self
    def __radd__(self,other): return self-self.manage_external(other)
    
    def __mul__(self,other):
        other = self.manage_external(other)
        empty = eval( 'color()' )
        for xatr in empty.attributes:
            empty[xatr]=self[xatr]*other[xatr]
        return empty
    def __rmul__(self,other): return self.manage_external(other)*self
    def __imul__(self,other): return self*self.manage_external(other)
    
    def __truediv__(self,other):
        other = self.manage_external(other)
        empty = eval( 'color()' )
        for xatr in empty.attributes:
            empty[xatr]=self[xatr]/other[xatr]
        return empty
    def __rtruediv__(self,other):  return self.manage_external(other)/self
    def __itruediv__(self,other): return self/self.manage_external(other)
    
    def __floordiv__(self,other):
        other = self.manage_external(other)
        empty = eval( 'color()' )
        for xatr in empty.attributes:
            empty[xatr]=self[xatr]//other[xatr]
        return empty
    def __rfloordiv__(self,other): return self.manage_external(other)//self
    def __ifloordiv__(self,other): return self//self.manage_external(other)
    
    def __pow__(self,other):
        other = self.manage_external(other)
        empty = eval( 'color()' )
        for xatr in empty.attributes:
            empty[xatr]=self[xatr]**other[xatr]
        return empty
    def __rpow__(self,other): return self.manage_external(other)**self
    def __ipow__(self,other): return self**self.manage_external(other)
    
    def __divmod__(self,other): return divmod(self,other)
    def __rdivmod__(self,other): return divmod( self.manage_external(other),self )
    def __idivmod__(self,other): return divmod( self,self.manage_external(other) )
    
    ## bitwise operands
    def __lshift__(self,other):
        other = self.manage_external(other)
        empty = eval( 'color()' )
        for xatr in empty.attributes:
            empty[xatr]=self[xatr]<<other[xatr]
        return empty
    def __rlshift__(self,other): return self.manage_external(other)<<self
    def __ilshift__(self,other): return self<<self.manage_external(other)
    
    def __rshift__(self,other):
        other = self.manage_external(other)
        empty = eval( 'color()' )
        for xatr in empty.attributes:
            empty[xatr]=self[xatr]>>other[xatr]
        return empty
    def __rrshift__(self,other): return self.manage_external(other)>>self
    def __irshift__(self,other): return self>>self.manage_external(other)
    
    def __and__(self,other):
        other = self.manage_external(other)
        empty = eval( 'color()' )
        for xatr in empty.attributes:
            empty[xatr]=self[xatr]&other[xatr]
        return empty
    def __rand__(self,other): return self.manage_external(other)&self
    def __iand__(self,other): return self&self.manage_external(other)
    
    def __or__(self,other):
        other = self.manage_external(other)
        empty = eval( 'color()' )
        for xatr in empty.attributes:
            empty[xatr]=self[xatr]|other[xatr]
        return empty
    def __ror__(self,other): return self.manage_external(other)|self
    def __ior__(self,other): return self|self.manage_external(other)
    
    def __xor__(self,other): 
        other = self.manage_external(other)
        empty = eval( 'color()' )
        for xatr in empty.attributes:
            empty[xatr]=self[xatr]^other[xatr]
        return empty
    def __rxor__(self,other): return self.manage_external(other)^self
    def __ixor__(self,other): return self^self.manage_external(other)
    
    ## conversion methods
    
    def __hash__(self): # :D hash the object
        return hash(self)
    
    def _selfINT(self): 
        
        """
            convets its values to integer, not not returning anythin
        """
        
        for xatr,xval in self:
            self[xatr]=int(xval)
    
        return None
        
    def _retINT(self):
        
        """
            returns color object with all its values into integers
        """
        
        e = self
        for xatr,xval in e:
            e[xatr]=int(xval)
        
        return e
    
    ## outside of object methods
    
    def _2hex(self,short=False):
        
        """
            hexadecimal representation of color object 
                does hexadecimal triplet short = True
                does hexadecimal normal
        """
        
        if short:
            f = lambda x: x&0x0F if ( x&0xF0 )>>4 == x&0x0F else \
                                    ( x&0xF0 )>>4 if (x&0x0F)<=(0xf/2) else \
                                    ((x&0xF0)>>4)+1 if ((x&0xF0)>>4)<0xF else 0xF
            h = '{0:01X}'.format
        else:
            f = lambda x: x&0xff
            h = '{0:02X}'.format
            
        vals = map(int,self.values())
        vals = map(f,vals)
        return '#'+''.join( map(h,vals) )
    def __hex__(self): return self._2hex(short=False)
    
    ## color based methods
    
    def _2cmyk(self):
        
        """
            conversing RGB color space to CMYK:
                cyan, magneta, yellow, key
        """
        
        new = self
        new /=0xff
        
        k = 1 - max( new.values() )
        c = (1-new.red - k)/(1-k)
        m = (1-new.green-k)/(1-k)
        y = (1-new.blue-k)/(1-k)
        
        return (c,m,y,k)
    
    def common_denominator(self,denominator=None):
        
        """
            in order to establish great transition between color object for animation or any other transition, color must be dividable by some number
            so in form of divisor ( int ) where start and end points of transition can have larger step than 1.
            if denominator != None : denominator =5 
        """
        
        denominator = 5 if not denominator else int(denominator)
        
        f = lambda x: int(x) if int(x)%denominator==0 else ((int(x/denominator))+1)*denominator
        
        for xatr,xval in self:
            xval = int(xval)
            xval = f(xval)
            self[xatr]=xval

def color_fromHEX(hex_str='#000'): # :D generates color object from HEX string
    
    """generates color object form hexadecimal value, defaulting to black"""
    
    if not type(hex_str).__name__ in 'str,unicode':
        raise TypeError('hex input must be a string or unicode')
    
    if '#' in hex_str: hex_str = hex_str.replace('#','')
    
    if len(hex_str) == 3:
        hex_str = [x for x in hex_str]
        hex_str = map(str,hex_str)
        hex_str = map( lambda x: '0x'+x+x , hex_str )
        hex_str = map( lambda x: int(x,16), hex_str )
        hex_str = color(*hex_str)
        return hex_str
    elif len(hex_str) == 6:
        hex_str = [ hex_str[i:i+2] for i in range( len(hex_str) ) if i%2==0 ]
        hex_str = map( lambda x: '0x'+x , hex_str )
        hex_str = map( lambda x: int(x,16), hex_str )
        hex_str = color(*hex_str)
        return hex_str
    else:
        raise ValueError('accepted hex string length is 3 and 6 for {}'.format(hex_str) ) 

def color_fromCMYK(c=1,m=1,y=1,k=1): # :D generates color object form CMYK values
    
    """generates RGB color object from CMYK color space, default is black"""
    
    red = 255*(1-c)*(1-k)
    green = 255*(1-m)*(1-k)
    blue = 255*(1-y)*(1-k)
    
    return color(red=red, green=green, blue=blue)

black   = color()
white   = color( 0xff)
red     = color( red=0xff )
blue    = color( blue=0xff )
green   = color( green=0xff )

__all__ = 'color,color_fromHEX,color_fromCMYK,black,white,red,green,blue'.split(',')



