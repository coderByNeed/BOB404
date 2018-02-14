#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals,with_statement
from sys import path
from os.path import dirname,abspath 
curPath = dirname( abspath( __file__ ) )
path.append(curPath)

## globals
__author__ = 'Danilo Mitrovic, <adewdda@gmail.com>'
__version__ = '1.0'


"""
    --
    defined range from 0 to white
    --
    +/- Personal convection: 
    + done, - not done
    
        empty init to black                                             +
        implement argument and keyword argument init                    +
        init cmyk                                                       -
        init hsl                                                        -    
        init hsv                                                        -
        color depth                                                     -
        implement init for byte color packet                            -
        mixing colors                                                   - #? additive, subtractive, alpha, proportion mixing
"""

## object definitions

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
                    and _retINT() converts all values in color to integer and returns duplicate
                    
                web_color : converts color object to hexadecimal representation:>
                        > allowed 6 digit hexadecimal : #ABCDEF in form of web_color()
                        > allowed 3 digit hexadecimal : #FAB in form of web_color(True) or web_color(short=True)
                    
                _2cmyk : returns cmyk color value conversion
                    
                common_denominator(denominator): converts the color to the common denominator in order:
                    in order to establish formal steps for animation or any kind of transition it is easier to establish equal steps if there is common division base between objects
    """
    
    attributes = 'red,green,blue,alpha'.split(',') #:D the main is RGBA
    color = 'color'
    
    def __init__(self,*args,**kwargs): # :D initialization 
        
        for xatr in self.attributes: #:D empty init
            setattr( self, xatr, 0 if xatr!= 'alpha' else 1.0)
        
        if args: #:D if args are passed
            
            args = map( self.manage_input, args )
            args = tuple(args)
            
            if not len(args):pass
            
            if len(args)==1 or isinstance( args, (int,float) ):                
                args = args[0]
                for xatr in self.attributes[:3]:
                    self[xatr]=args
            else:
                for i,xatr in enumerate(self.attributes):
                    try:
                        args[i]
                        self[xatr]=args[i]
                    except IndexError:pass
                    except Exception as e:
                        print( e.message, i,args )
            
        if kwargs: #:D if kwargs are passed
            
            if self.color in kwargs.keys():
                
                if isinstance( kwargs[self.color], (tuple,list) ):
                    self.__init__( *kwargs[self.color] )
                
                if isinstance( kwargs[self.color], dict ):
                    self.__init__( **kwargs[self.color] )
                
                self.__init__( kwargs[self.color] )
            
            for xatr,xval in kwargs.items():
                if xatr in self.attributes:
                    xval = self.manage_input(xval)
                    self[xatr]=xval
            
        self.alpha = float(self.alpha) if not isinstance(self.alpha,float) else self.alpha
        self.alpha = round( self.alpha if self.alpha <= 1.0 else self.alpha/0xff ,3 )
        
        
    def __iter__(self): # :D iterator, returns tuple (xatr,xval)
        for xatr in self.attributes:
            yield xatr, self[xatr]
    
    def __next__(self): # :D next(self)
        return next(self)
    
    def __str__(self): # :D console representation
        return " , ".join( map(str, map(self.__getitem__, self.attributes[:3]) ) )+' :{!s}'.format( self.__getitem__(self.attributes[3]) )
    
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
                item = sum(item)/len(item)
                
        if type(item).__name__ in 'str,unicode':
            item = ord( item[0] )
        if type(item).__name__ in 'dict':
            if not len(item): item = len(item)
            else:
                item = self.manage_external(item)
                item = sum(item.values())/len(item)
        
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
        if item in 'RGBA' or item in 'rgba' or item in self.attributes:
            if item in 'rR': item = 'red'
            if item in 'gG': item = 'green'
            if item in 'bB': item = 'blue'
            if item in 'aA': item = 'alpha'
            return getattr(self,item)
        else:
            raise TypeError('item not a string and item not found {} in {}'.format(item,self) )
    
    def __setitem__(self,item,value):
        
        """
            self[item]=value
        """
        
        try:
            self[item]
            value = self.manage_input(value) if not value>=0 and value<=0xff else value
            if item in 'aAalpha':
                value = value if value <=1 else round( float(value)/0xff, 3 )
            setattr(self,item,value)
        except (TypeError,LookupError):pass 
    
    def implement_opacity(self):
        r = color()
        for xatr in self.attributes[:3]:
            r[xatr]=self[xatr]*self.alpha
        return r

    def values(self): # :D returns values
        for xatr in self.attributes:
            yield self[xatr]
    
    def keys(self):  # :D returns keys
        for xatr in self.attributes:
            yield xatr
    
    def items(self):return list(self) # :D returns list of tuple pairs in form of (key,value)
    
    def __len__(self): return len( self.attributes )
    
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
    def __bool__(self):return sum( self.values()[:3] ) != 0 # if not black
    def __lt__(self,other):
        other = self.manage_external(other)
        return sum(self.values()) < sum(other.values())
    def __le__(self,other):
        other = self.manage_external(other)
        return sum(self.values()) <= sum(other.values())
    def __gt__(self,other):
        other = self.manage_external(other)
        return sum(self.values()) > sum(other.values())
    def __ge__(self,other):
        other = self.manage_external(other)
        return sum(self.values()) >= sum(other.values())
    
    ## mathematical operands
    def __add__(self,other): # alpha 1
        other = self.manage_external(other)
        
        self_o = self.implement_opacity()
        other = other.implement_opacity()
        
        empty = eval( 'color()' )
        
        for xatr in empty.attributes[:3]:
            empty[xatr]=other[xatr]+self_o[xatr]
        return empty
    def __radd__(self,other): return self.manage_external(other)+self
    def __iadd__(self,other): return self+self.manage_external(other)
    
    def __sub__(self,other):
        other = self.manage_external(other)
        
        self_o = self.implement_opacity()
        other = other.implement_opacity()
        
        empty = eval( 'color()' )
        
        for xatr in empty.attributes[:3]:
            empty[xatr]=self_o[xatr]-other[xatr]
        
        return empty
    def __rsub__(self,other): return self.manage_external(other)-self
    def __isub__(self,other): return self-self.manage_external(other)
    
    def __mul__(self,other):
        other = self.manage_external(other)
        
        self_o = self.implement_opacity()
        other = other.implement_opacity()
        
        empty = eval( 'color()' )
        for xatr in empty.attributes[:3]: # no alpha
            empty[xatr]=self_o[xatr]*other[xatr]
        return empty
    def __rmul__(self,other): return self.manage_external(other)*self
    def __imul__(self,other): return self*self.manage_external(other)
    
    def __truediv__(self,other):
        other = self.manage_external(other)
        
        self_o = self.implement_opacity()
        other = other.implement_opacity()
        
        empty = eval( 'color()' )
        for xatr in empty.attributes[:3]: # no alpha
            empty[xatr]=self_o[xatr]/other[xatr]
        return empty
    def __rtruediv__(self,other):  return self.manage_external(other)/self
    def __itruediv__(self,other): return self/self.manage_external(other)
    
    def __floordiv__(self,other):
        other = self.manage_external(other)
        
        self_o = self.implement_opacity()
        other = other.implement_opacity()
        
        empty = eval( 'color()' )
        for xatr in empty.attributes[:3]: # no alpha
            empty[xatr]=self_o[xatr]//other[xatr]
        return empty
    def __rfloordiv__(self,other): return self.manage_external(other)//self
    def __ifloordiv__(self,other): return self//self.manage_external(other)
    
    def __pow__(self,other):
        other = self.manage_external(other)
        
        self_o = self.implement_opacity()
        other = other.implement_opacity()
        
        empty = eval( 'color()' )
        for xatr in empty.attributes[:3]: # no alpha
            empty[xatr]=self_o[xatr]**other[xatr]
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
        for xatr in empty.attributes[:3]: # no alpha
            empty[xatr]=self[xatr]<<other[xatr]
        return empty
    def __rlshift__(self,other): return self.manage_external(other)<<self
    def __ilshift__(self,other): return self<<self.manage_external(other)
    
    def __rshift__(self,other):
        other = self.manage_external(other)
        empty = eval( 'color()' )
        for xatr in empty.attributes[:3]: # no alpha
            empty[xatr]=self[xatr]>>other[xatr]
        return empty
    def __rrshift__(self,other): return self.manage_external(other)>>self
    def __irshift__(self,other): return self>>self.manage_external(other)
    
    def __and__(self,other):
        other = self.manage_external(other)
        empty = eval( 'color()' )
        for xatr in empty.attributes[:3]: # no alpha
            empty[xatr]=self[xatr]&other[xatr]
        return empty
    def __rand__(self,other): return self.manage_external(other)&self
    def __iand__(self,other): return self&self.manage_external(other)
    
    def __or__(self,other):
        other = self.manage_external(other)
        empty = eval( 'color()' )
        for xatr in empty.attributes[:3]: # no alpha
            empty[xatr]=self[xatr]|other[xatr]
        return empty
    def __ror__(self,other): return self.manage_external(other)|self
    def __ior__(self,other): return self|self.manage_external(other)
    
    def __xor__(self,other): 
        other = self.manage_external(other)
        empty = eval( 'color()' )
        for xatr in empty.attributes[:3]: # no alpha
            empty[xatr]=self[xatr]^other[xatr]
        return empty
    def __rxor__(self,other): return self.manage_external(other)^self
    def __ixor__(self,other): return self^self.manage_external(other)
    
    ## conversion methods
    
    def __hash__(self): # :D hash the object
        return hash(self)
    
    ## outside of object methods
    
    def web_color(self,short=False):
        
        """
            hexadecimal representation of color object 
                does hexadecimal triplet short = True
                does hexadecimal normal
        """
        
        # f = function to contstrain the color value for integer
        # h = hex formating , so it can format to byte or nibble hex
        if short:
            f = lambda x: x&0x0F if ( x&0xF0 )>>4 == x&0x0F else \
                                    ( x&0xF0 )>>4 if (x&0x0F)<=(0xf/2) else \
                                    ((x&0xF0)>>4)+1 if ((x&0xF0)>>4)<0xF else 0xF
            h = '{0:01X}'.format
        else:
            f = lambda x: x&0xff
            h = '{0:02X}'.format
        
        vals = map( self.__getitem__, self.attributes[:3] )
        vals = map(int, vals )
        vals = map(f,vals)
        return '#'+''.join( map(h,vals) )

    ## color based methods
    
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
    
    def __int__(self):
        vals = self.values()
        vals = map( lambda x: int(x) if x-int(x)<=.5 else int(round(x)) ,vals)
        vals = map(lambda x:x&0xff, vals)
        vals = list(vals) if not isinstance(vals,list) else vals
        
        return ( vals[0]<<16 )+(vals[1]<<8)+vals[2]
    
    def mix_over(self,other): ## ? not sure, closest to blend in ilustrator , 
        other = self.manage_external(other)
        empty = eval( 'color()' )
        
        alpha_r = ( 1 - (1-self.alpha)*(1-other.alpha) )
        
        for xatr in self.attributes:
            val = ( self.alpha*self[xatr] + (1-self.alpha)*other.alpha*other[xatr] )/alpha_r
            empty[xatr]=val
        
        return empty

##########################################################################################################################################

base = 123 # base for conversion : to get what object can and can not be converted to colours
c_Set = []
[ c_Set.append( x(base)) for x in [int,str,chr] ]
c_Set.append( str(chr(base) ))
[ c_Set.append( x() ) for x in [list,tuple,dict]  ]
[ c_Set.append( x( [base] ) ) for x in [list,tuple]  ]
c_Set.append( {"red":base} )
[ c_Set.append( x( [base]*2 ) ) for x in [list,tuple]  ]

def test_base( clas_obj , database = None):
    if database == None: database = c_Set
    for x in c_Set:
        try:
            clas_obj(x)
            print( type(x), ":PASS" )
            print("\t {}::\t{}".format(x,clas_obj(x)) )
        except Exception as e:
            print( type(x), e.message )

black,white = color(),color(0xff)
red,green,blue = color( red=0xff ),color( green=0xff ),color( blue=0xff )
cyan,magenta,yellow = color( blue=0xff,green=0xff ),color(red=0xff,blue=0xff),color(red=0xff,green=0xff)

rgb_colorSet = [ red,green,blue ]
cmyk_colorSet= [cyan,magenta,yellow,black]

isColor = lambda x: x.__class__.__name__ == 'color'

## color formater


## global lambdas
range_multiplier = lambda r1,r2: -1 if not isinstance(r1,int) and isinstance(r2,int) else float(r1)/r2 if r1>r2 else float(r2)/r1 # returns range multiplier for range1 and range 2
range_coeficient = lambda value,range: float(value)/range if value < range else -1 # returns relation of range and value within range
bit_range = lambda i: 2**int(i) if isinstance(i,(int,float)) else None # i = bit number
bit_max_val = lambda i: ( 2**int(i) )-1 if isinstance(i,(int,float)) else None # i = bit number


class color_format(object):
    
    input = None
    valid_expressions = ''
    
    def __init__(self,color_obj):
        
        self.input = color_obj if isColor(color_obj) else color.manage_external(color_obj)
    
    def web(self,short=None):
        short = False if short == None else bool(short)
        try:
            return self.input.web_color(short)
        except Exception as e:
            print( e.__name__ )
            raise
        
print( color_format( white ).input == white )

def bit_offset( bits_number, channels = None): # returns zip(bit,offset)
    
    """
        Distirbute bits per channels, so if you have 8 beats and 4 channels it will distribute 2 bits per channel.
        Then it generates offsets for that channels so you can pack values to specific beats for specific elemenents
        
        returns a list of tuples in form (bits,offset)
    """
    
    try:
        bits_number = int(bits_number)
    except Exception as e:
        raise LookupError('{} element must be an int or int convertable'.format(bits_number) )
    channels = 3 if channels is None or channels == None else channels
    minimal_offset = []
    
    if channels>bits_number:
        raise ValueError('bit_offset :> {} is smaller than {} -- no can do'.format(channels,bits_number) )
    
    if bits_number%channels:
        minimal_offset=[ int(bits_number/channels) ]*channels
        bits_number = bits_number%channels
    else:
        minimal_offset=[ int(bits_number/channels) ]*channels
        bits_number = 0
    
    if bits_number:
    
        for c_i in range(channels):
            
            minimal_offset[c_i]+=1
            bits_number-=1
            
            if not bits_number: break
    
    bits_number = sum(minimal_offset)
    offset = []
    
    for ch in range(channels):
        bits_number=bits_number-minimal_offset[ch]
        offset.append(bits_number)
    
    return zip(minimal_offset,offset)
   
def shift_value( value_range,result ): # returns float
    
    if not isinstance( value_range, (list,tuple) ):
        raise TypeError('{!s} is not list , tuple'.format(value_range) )
    if not isinstance(result,int):
        raise TypeError('{!s} is not integer'.format(result))
    
    if len(value_range)>2:
        raise ValueError('{} != 2 for {!r}, desired formulation must be of value:range with length 2'.format(len(value_range),value_range))
    if value_range[0]>value_range[1]:
        raise ValueError("{!r} must be in value:range pair where value<=range".format(value_range))
    
    if value_range[0]==value_range[1] and value_range[0]!=0: return float(result)
    if value_range[0]==0 :return 0
    
    if range_coeficient(*value_range) == -1:
        raise ValueError('something went wrong for {!r}'.format(value_range))
    
    return range_coeficient(*value_range)*result

def shift_bit_value(value,range,bit): #returns int
    rc = range_coeficient(value,range)
    
    if rc == -1:
        raise ValueError('something went wrong for {!r}'.format(value_range))
        
    bit = bit_max_val(bit)
    r = rc*bit
    
    if rc>1:
        return None
    
    if r-int(r)<0.5:
        return int(r)
    return int(r+1)


__all__ = [
    'black','white',
    'red','green','blue',
    'bit_mask_red','bit_mask_grn','bit_mask_blu',
    'cyan','magenta','yellow',
    'bit_mask_cyn','bit_mask_mgnt','bit_mask_ylw',
    
    'rgb_colorSet','cmyk_colorSet','isColor','color'
]