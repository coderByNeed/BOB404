#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals,with_statement


__author__ = 'Danilo Mitrovic, <adewdda@gmail.com>'
__version__ = '0.0 still in progress'
__name__ = 'color'

class color(object):
    
    """
        Color object for future use, initializes with:
            
            color(red,green,blue) : red,green,blue in type of int,float,string,byte
            
            color(red=red_el, green=green_el, blue=blue_el) : red_el,green_el,blue_el in type of int,float,string,byte
            
            color( color=(red,green,blue) ) : red,green,blue in type of int,float,string,byte
            
        color class can utilitize next operands:
            
            mathematic: arithmetic
            comparison: equality and such
            bitwise: binary shifts 
        
        color class can utilitize external private ment methods:
            color().manage_external_data()
                // it suplys that any element that can not be converted to int ( like list,tuple,dict,generators and such) be passed to color object as arguments or keyword arguments
            color().manage_input(element)
                // converts element to int as long as it is not a container
        
        color class can utilitize next public methods:
            
            color()._toDivisor(divisor=None)
                // it makes values of color divisable by smallest of said divisor so lowest common denominator can be in base of that divisor
            color()._2hex()
                // generates the hexadecimal representation of color in form #000000
            color()
    """
    
    attributes = 'red,green,blue'.split(',') #:D RGB color spaces in reserve
    whole_init = 'color' #:D if user wants to input a color in tuple form
    
    def __init__(self,*args,**kwargs):
        
        """
            initializer , pass arguments that are not containers ( as for list,tuple .... )
            for more information check help element
        """
        
        for xatr in self.attributes:
            setattr(self,xatr,0) #empty init is black
        
        if args: #:D argument handling
            
            if len(args)==1:
                args = self.manage_input( args[0] )
                for xatr in self.attributes:
                    setattr(self,xatr,args)
            else:
                args = filter( lambda x: type(x).__name__ not in 'list,dict,tuple', args )
                args = map( self.manage_input, args)
                args = tuple(args) if not isinstance(args,tuple) else args
                
                for i,xatr in enumerate(self.attributes):
                    try:
                        args[i]
                        setattr(self,xatr,args[i])
                    except IndexError as ie:
                        pass
                    except Exception as e: # failsafe
                        print( type(e).__name__, xatr, args[i]  )
        
        if kwargs: # key word argument handling
            try:
                kwargs[self.whole_init]
                
                if isinstance( kwargs[self.whole_init], (list,tuple) ):
                    self.__init__( *kwargs[self.whole_init] )
                elif isinstance( kwargs[self.whole_init], dict ):
                    self.__init__( **kwargs[self.whole_init] )
                else:
                    self.__init__( kwargs[self.whole_init] )
            
            except KeyError:
                for xatr,xval in kwargs.items():
                    if xatr in self.attributes and getattr(self,xatr)==0:
                        xval = self.manage_input(xval)
                        setattr(self,xatr,xval)
            
            except Exception as e:
                print( type(e).__name__,kwargs )
    
    def __contain__(self,item):
        
        """
            if element in color:
                //str:element -> if element in color spaces
                //val:element -> if element in color value 
        """
        
        return item in self.attributes or item in [ getattr(self,xatr) for xatr in self.attributes ]
    
    def __str__(self):
        
        """
            virtual representation for color object in form of val,val,val in form of RGB
        """
        
        col = [ getattr(self,xatr) for xatr in self.attributes ]
        col = map( str, col )
        return ",".join(col)
    
    def __repr__(self):
        
        """
            repr part of color class, if you dont know what repr is google it and use it if you need it
        """
        
        col_stip = { xatr:getattr(self,xatr) for xatr in self.attributes if getattr(self,xatr)!=0 }
        col_stip = '' if not col_stip else ','.join([ "{}={}".format(xatr,xval) for xatr,xval in col_stip.items() ])
        return "color({!s})".format(col_stip)
    
    def __iter__(self):
        
        """
            iterates over color object in form of pairs (attribute:attr_val)
        """
        
        for xatr in self.attributes:
            yield xatr, self.__next__(xatr)
    
    def __next__(self,xatr):
        return getattr(self,xatr)
    
    def __getitem__(self,xatr):
        
        """
            simple get item in form searching for RGB or rgb or red,green,blue values
        """
        
        if xatr in self.attributes:
            return getattr(self,xatr)
        if xatr in 'rgb' or xatr in 'RGB':
            if xatr in 'rR': xatr = 'red'
            if xatr in 'gG': xatr = 'green'
            if xatr in 'bB': xatr = 'blue'
            return getattr(self,xatr)
        
    def __setitem__(self,xatr,xval):
        
        """
            sets item if attribute is valuable for RGB,rgb or red,green,blue value
        """ 
        
        if self[xatr] or self[xatr]==0:
            if xatr in 'rgb' or 'RGB':
                if xatr in 'rR':xatr = 'red'
                if xatr in 'gG':xatr = 'green'
                if xatr in 'bB':xatr = 'blue'
            
            setattr(self,xatr,xval)
        else:
            raise LookupError(xatr,xval)

    ## math operands
    
    def __add__(self,other):
        
        other = self.manage_external_data(other)
        empty = eval( 'color()' )
        
        for xatr in self.attributes:
            empty[xatr] = self.manage_input(self[xatr]+other[xatr])
        
        return empty
    __iadd__ = __radd__ = __add__
    
    def __sub__(self,other):
        other = self.manage_external_data(other)
        empty = eval( 'color()' )
        
        for xatr in self.attributes:
            empty[xatr] = self.manage_input(self[xatr]-other[xatr])
        
        return empty
    __isub__ = __rsub__ = __sub__
    
    def __mul__(self,other):
        other = self.manage_external_data(other)
        empty = eval( 'color()' )
        
        for xatr in self.attributes:
            empty[xatr] = self.manage_input(self[xatr]*other[xatr])
        
        return empty
    __imul__ = __rmul__ = __mul__
    
    def __truediv__(self,other):
        other = self.manage_external_data(other)
        empty = eval( 'color()' )
        
        for xatr in self.attributes:
            empty[xatr] = self.manage_input(self[xatr]/other[xatr])
        
        return empty
    __itruediv__ = __rtruediv__ = __truediv__
    
    def __floordiv__(self,other):
        other = self.manage_external_data(other)
        empty = eval( 'color()' )
        
        for xatr in self.attributes:
            empty[xatr] = self.manage_input(self[xatr]//other[xatr])
        
        return empty
    __ifloordiv__ = __rfloordiv__ = __floordiv__
    
    def __mod__(self,other):
        other = self.manage_external_data(other)
        empty = eval( 'color()' )
        
        for xatr in self.attributes:
            empty[xatr] = self.manage_input(self[xatr]%other[xatr])
        
        return empty
    __imod__ = __rmod__ = __mod__
    
    def __divmod__(self,other):
        other = self.manage_external_data(other)
        
        div = self/other
        mod = self&other
        
        return div,mod
    __idivmod__ = __rdivmod__ = __divmod__
    
    def __pow__(self,other):
        other = self.manage_external_data(other)
        empty = eval( 'color()' )
        
        for xatr in self.attributes:
            empty[xatr]= self[xatr]**other[xatr]
        
        return empty
    __ipow__ = __rpow__ = __pow__
    
    def __lshift__(self,other):
        other = self.manage_external_data(other)
        empty = eval( 'color()' )
        
        for xatr in self.attributes:
            empty[xatr]=self[xatr]<<other[xatr]
        
        return empty
    __ilshift__ = __rlshift__ = __lshift__
    
    def __rshift__(self,other):
        other = self.manage_external_data(other)
        empty = eval( 'color()' )
        
        for xatr in self.attributes:
            empty[xatr]=self[xatr]>>other[xatr]
        
        return empty
    __irshift__ = __rrshift__ = __rshift__
    
    def __and__(self,other):
        other = self.manage_external_data(other)
        empty = eval( 'color()' )
        
        for xatr in self.attributes:
            empty[xatr]=self[xatr]&other[xatr]
        
        return empty
    __iand__ = __rand__ = __and__
    
    def __xor__(self,other):
        other = self.manage_external_data(other)
        empty = eval( 'color()' )
        
        for xatr in self.attributes:
            empty[xatr]=self[xatr]^other[xatr]
        
        return empty
    __ixor__ = __rxor__ = __xor__
    
    def __or__(self,other):
        other = self.manage_external_data(other)
        empty = eval( 'color()' )
        
        for xatr in self.attributes:
            empty[xatr]=self[xatr]|other[xatr]
        
        return empty
    __ior__ = __ror__ = __or__
    
    ## boolean + comparison operands
    
    def __eq__(self,other):
        other = self.manage_external_data(other)
        
        return all( self[xatr]==other[xatr] for xatr in self.attributes )
    
    def  __ne__(self,other):
        return not self==other
    
    def __bool__(self):
        return self == eval( 'color()' )
    
    def __lt__(self,other):
        other = self.manage_external_data(other)
        
        return all( self[xatr]<other[xatr] for xatr in self.attributes )
    
    def __le__(self,other):
        other = self.manage_external_data(other)
        
        return all( self[xatr]<=other[xatr] for xatr in self.attributes )
    
    def __gt__(self,other):
        other = self.manage_external_data(other)
        
        return all( self[xatr]>other[xatr] for xatr in self.attributes )
        
    def __ge__(self,other):
        other = self.manage_external_data(other)
        
        return all( self[xatr]>=other[xatr] for xatr in self.attributes )
    
    ## class specific methods
    
    def manage_external_data(self,other):
        
        """
            manages the input element when making mathematical operands for containers
        """
        
        if isinstance(other, (list,tuple) ): other = color(*other)
        if isinstance( other, dict ): other = color(**other)
        
        other = other if isinstance(other, color) else color(other)
        return other
    
    def manage_input(self,data):
                
        """
            converts data to integer, not to be used with containers and wrappers, individual data only
        """
        
        try:
            data= int(data) # :D checks if it is integer type
        except ValueError:
            data= data[0] if isinstance(data[0],int) else ord(data[0]) #:D checks if it is unicode or bytes cross version
        except TypeError:
            data= int(data.real) # :D complex numbers

        return data if data >= 0 and data <= 0xff else 0 if data < 0 else 0xff
    
    def _toDivisor(self,divisor=None):
        
        """
            complicated to explain, soo .... lets talk about it like this. I needed to implement a steping system for color animation to make color transition gradualy and easier to define a specific color step. So in that way the steps for color animation needs to be divisible by specific divisor in order to remove the element of common divisibles of 1. 
        """
        
        divisor = self.manage_input(divisor) if divisor else 5
        
        for xatr,xval in self:
            
            if xval%divisor!=0:
                
                if (xval%divisor)<( divisor/2.0 ):
                    self[xatr] = int( xval/divisor )*divisor
                else:
                    self[xatr] = ( int(xval/divisor) + 1 )*divisor
        
        return self
    
    def _2hex(self):
        
        """
            transits the color object to form of #000000
        """
        
        return '#'+''.join([ "{0:02X}".format(xval) for i,xval in self])
    
    
    
## outside class functions

def color_generator(*args):
    
    """
        generator for color objects depending on data that is inputed, if you input every data as independent containers you will get for n of containers n number of colors
    """
    
    isARGS      = lambda x: type(x).__name__ in 'list,tuple'
    isPY35      = lambda x: type(x).__name__ in 'range,filter,map'
    isKWARGS    = lambda x: type(x).__name__ == 'dict'
    
    if args:
        
        for xel in args:
            if isKWARGS(xel):
                yield color(**xel)
            elif isARGS(xel) or isPY35(xel):
                yield color(*xel)
            else:
                yield color(xel)
    else:
        raise AttributeError('arguments not passed')

def color_from_hex(hexstring):
    
    """
        generates color object from string hex value
    """
    
    if not type(hexstring).__name__ in 'str,unicode,bytes':
        raise TypeError('{} is not a string'.format(hexstring) )
    if isinstance(hexstring,str) and not hexstring.startswith('#'):
        raise ValueError('hexstring must have # element in front')
    
    hexstring = hexstring.replace( '#', '' )
    
    if len( hexstring )==3:
        hexstring = [ x+x for x in hexstring ]
    else:
        hexstring = [ hexstring[x:x+2] for x in range(len(hexstring)) if x%2==0 ]
    
    hexstring = [ int(x,16) for x in hexstring ]
    
    return color(*hexstring)
        
a = color( **{"red":12,"blue":13,"green":15} )

print( color_from_hex( '#FAB' ) )
print( color_from_hex( a._2hex() ) )