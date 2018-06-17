#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function,with_statement
from sys import path
from os.path import dirname,abspath,exists
curPath = dirname( abspath( __file__ ) )
path.append(curPath)
del dirname,abspath,path
#:? end of header

#:? meta
__author__ 	= 'Danilo Mitrovic, <adewdda@gmail.com>'
__licence__	= 'GNU'
__version__ = '0.3'

from math import cos,sin
from math import pi,e
from math import radians
from math import log
## constants
phi = ( 1+5**.5 )*.5
SAMPLE_RATE = 8000
## ---------------------------------------------------------------------------------------
## lambdas

###> functions for wave generation
sine_wave = lambda freq,time,phase: cos( 2*pi*freq*time + phase )
sqre_wave = lambda freq,time,phase: 1 if sine_wave(freq,time,phase)>=0 else -1

###> binary representation for quantisation
chck_4b = lambda x: ''.join( map( lambda x: '{0:02b}'.format( x&3 ), [ (x>>2)&0b11, x&0b11 ] ) )
chck_1B = lambda x: '-'.join( map( chck_4b, [ (x>>4)&0xf, x&0xf ] ) )

####> linear function generation

## ---------------------------------------------------------------------------------------
## errors
class AliasingError(ValueError):pass

class ColorTypeError(TypeError):pass
class ColorArithmeticError(ArithmeticError):pass

class PointDefError(Exception): pass
class PointGetError(AttributeError):pass
class PointSetError(AttributeError):pass

## ---------------------------------------------------------------------------------------
factorial 					= lambda x: 					x*fract(x-1) if x not in range(2) else 1
lsb_byte					= lambda x,m=0x01:				None if x>0xff \
																	else 0 if x==0 \
																	else m if x&m==m \
																	else lsb_byte( x, m<<1 )
msb_byte					= lambda x,m=0x80:				None if x>0xff \
																	else 0 if x==0 \
																	else m if x&m==m \
																	else msb_byte( x, m>>1 )
unary_2scmp 				= lambda n:						None if n>0xff else n^( 0xff^( ( lsb_byte(n) << 1 )-1 ) )
step_sequence				= lambda step,index,start=0:	start + step*index ## shold be a0+d*(n-1): but in this case, computers calculate from zero, first element (just start) has index of 0
sumation 					= lambda n:						n*(n+1)*.5
inductiive_step_sumation	= lambda n:						n*(n+1)*.5 + (n+1)
## NEED PROTO GENERATOR BASE ?? how...
## ---------------------------------------------------------------------------------------

## point def class
class point(object):
	
	i = j = k = 0.0
	pos = 0
	
	def __init__(self,i=None,j=None,k=None):
		if i is not None: self.i = float(i)
		if j is not None: self.j = float(j)
		if k is not None: self.k = float(k)
		
		self.value = ( self.i**2 + self.j**2 + self.k**2  )**.5
	
	def __getitem__(self,key):
		if key in range(3):
			return [self.i, self.j, self.k][key]
		raise PointGetError( 'acceptable keys are 0,1,2' )
		
	def __setitem__(self,key,value):
		if key in range(3):
			key = 'i,j,k'.split(',')[key]
			try:
				setattr( self, key, float(value) )
			except:
				raise PointSetError( '{} not convertable to float'.format(value) )
		raise PointGetError( 'acceptable keys are 0,1,2' )
	
	def __delitem__(self,key):
			self[key]=0.0
	
	def __del__(self):
		del self
	
	def __next__(self):
		if self.pos == 3: 
			self.pos %= 3
			raise GeneratorExit
		self.pos+=1
		return self[self.pos-1]
	next = __next__
	
	def __iter__(self):
		while 1:
			try:
				yield next(self)
			except GeneratorExit: break
	
	def __add__(self,other):
		if type(other).__name__ in 'list,tuple,point'
	
# linear function generator
## ?> https://brilliant.org/wiki/3d-coordinate-geometry-equation-of-a-line/
class lin_funct_2d(object):pass #	__call__
#	object.__call__(self[, args...])
	
class lin_funct_3d(object):pass # __call__
#	object.__call__(self[, args...])
		
# color base
class color(object):
	ind = 0
	def __init__(self,red=None,green=None,blue=None,hex_i=None):
		
		if hex_i is not None:
			self.value = int(hex_i)
		elif red is not None and green is not None and blue is not None:
			red = int(red)
			green=int(green)
			blue =int(blue)
			self.value = (red<<16) + (green<<8) + blue
		else:
			self.value = 0
		
		self.value &= 0xffffff
		
	def __str__(self):
		return '#{0:06X}'.format(self.value)
	
	def red(self):
		return ( self.value >>16 )&0xff
	
	def green(self):
		return (self.value >> 8)&0xff
	
	def blue(self):
		return self.value&0xff
	
	def __contains__(self,item):
		return item in [self.red(),self.green(),self.blue()]
	
	def __len__(self):return 3
	
	def __iter__(self):
		while 1:
			try:
				yield next(self)
			except GeneratorExit: break
		self.ind = 0
	
	def __next__(self):
		if self.ind ==3 : raise GeneratorExit
		self.ind += 1
		return self[self.ind-1]
	next = __next__
	
	def __getitem__(self,key):
		if isinstance(key,str) and key in 'red,green,blue':
			key = 'red,green,blue'.split(',').index(key)
		else:pass
		return self.red() if key==0 else self.green() if key==1 else self.blue()
	
	def __delitem__(self,item):
		if item in self:
			item = [ x for x in range(3) if self[x]==item ][0]
			self[item]=0x0
	
	def __setitem__(self,key,value):
		if self[key]:
			key = 'blue,green,red'.split(',').index(key)
			key *= 8 #no bits
			value = int(value)&0xff
			MASK = (self.value>>key)&0xff
			MASK <<=key
			self.value = self.value^MASK
			self.value += value<<key
	
	def _is_cool(self,other):
		return type(other).__name__ in 'int,list,tuple,color'
	
	def asign_per_type( self,other):
		if not self._is_cool(other):
			raise ColorTypeError('{} of {} got , expected int, or tuple of length 3'.format( other, type(other).__name__ ) )
		if isinstance(other,color):return other
		if isinstance(other,tuple):
			return color( *other, hex_i=None )
		if isinstance(other,int) and other<0xff:
			return color( other,other,other, hex_i=None )
		return color( hex_i = other )
	
	def __bool__(self):
		return self.value != 0x0
	__nonzero__ = __bool__
	def __invert__(self): #2's compliment
		return color( hex_i=sum( unary_2scmp( self[x] )<<(x*8) for x in range(3) ))
	def invert(self): # 1;s compliment
		return color( hex_i=self.value^0xffffff )
	
	## binary
	
	def __and__(self,other):
		other = self.asign_per_type(other)
		return color( hex_i=( self.value&other.value ) )
	def __rand__(self,other):
		return self&other
	def __iand__(self,other):
		return self&other
		
	def __or__(self,other):
		other = self.asign_per_type(other)
		return color( hex_i=( self.value|other.value ) )
	def __ror__(self,other):
		return self|other
	def __ior__(self,other):
		return self|other
	
	def __xor__(self,other):
		other = self.asign_per_type(other)
		return color( hex_i=( self.value^other.value ) )
	def __rxor__(self,other):
		return self^other
	def __ixor__(self,other):
		return self^other
	
	def __lshift__(self,other):
		if not isinstance(other,int):
			raise ColorArithmeticError( 'for lshift item must be an int got {}'.format(other) )
		return color( hex_i=(self.value<<other) )
	def __rlshift__(self,other):
		return self<<other
	def __ilshift__(self,other):
		return self<<other
	
	def __rshift__(self,other):
		if not isinstance(other,int):
			raise ColorArithmeticError( 'for lshift item must be an int got {}'.format(other) )
		return color( hex_i=(self.value>>other) )
	def __rrshift__(self,other):
		return self>>other
	def __irshift__(self,other):
		return self>>other
	
	## integer based
	
	def __add__(self,other):
		if type(other).__name__ in 'color,tuple,list':
			r,g,b = map( lambda x: x&0xff, map( sum, zip( self, other ) ) )
			return color( red=r, green=g, blue=b )
		if isinstance(other, (int,float) ):
			r,g,b = map( lambda x: int( x+other)&0xff, self )
			return color( red=r,green=g,blue=b )
		raise ColorArithmeticError( 'got {} of {}, expected int,float,tuple,list or color' )
	def __radd__(self,other):
		return self+other
	def __iadd__(self,other):
		return self+other
	
	def __sub__(self,other):
		if type(other).__name__ in 'color,tuple,list':
			r,g,b = map( lambda t: int(abs( t[0]-t[1] ))&0xff , zip( self, other ) )
			return color( red=r, green=g, blue=b )
		if isinstance(other, (int,float) ):
			r,g,b = map( lambda x: int( x-other)&0xff, self )
			return color( red=r,green=g,blue=b )
		raise ColorArithmeticError( 'got {} of {}, expected int,float,tuple,list or color' )
	def __rsub__(self,other):
		return self-other
	def __isub__(self,other):
		return self-other
	
	def __mul__(self,other):
		if type(other).__name__ in 'color,tuple,list':
			s = [ x for x in self ]
			o = [ x for x in other ]
			return color( red= int( s[1]*o[2] - s[2]*o[1] )&0xff ,green=int( s[0]*o[2] - s[2]*o[0] )&0xff ,blue=int( s[0]*o[1] - s[1]*o[0] )&0xff  )
		if isinstance(other, (int,float) ):
			r,g,b = map( lambda x: int( x*other)&0xff, self )
			return color( red=r,green=g,blue=b )
		raise ColorArithmeticError( 'got {} of {}, expected int,float,tuple,list or color' )
	def __rmul__(self,other):
		return self*other
	def __imul__(self,other):
		return self*other
	
	def __truediv__(self,other):
		if isinstance(other, (int,float) ):
			r,g,b = map( lambda x: int( x/other)&0xff, self )
			return color( red=r,green=g,blue=b )
		raise ColorArithmeticError( 'got {} of {}, expected int,float' )
	def __rtruediv__(self,other):
		return self/other
	def __itruediv__(self,other):
		return self/other
	
	def __floordiv__(self,other):
		if isinstance(other, (int,float) ):
			r,g,b = map( lambda x: int( x//other)&0xff, self )
			return color( red=r,green=g,blue=b )
		raise ColorArithmeticError( 'got {} of {}, expected int,float' )
	def __rfloordiv__(self,other):
		return self//other
	def __ifloordiv__(self,other):
		return self//other
	
	def __mod__(self,other):
		if type(other).__name__ in 'color,tuple,list':
			r,g,b = map( lambda x: int( x[0]%x[1] )&0xff, zip(self,other) )
			return color( red=( s[0]%o[0] )&0xff ,green=( s[1]%o[1] )&0xff ,blue=int( s[0]*o[1] - s[1]*o[0] )&0xff  )
		if isinstance(other, (int,float) ):
			r,g,b = map( lambda x: int( x%other)&0xff, self )
			return color( red=r,green=g,blue=b )
		raise ColorArithmeticError( 'got {} of {}, expected int,float,tuple,list or color' )
	def __rmod__(self,other):
		return self%other
	def __imod__(self,other):
		return self%other
	
	def __divmod__(self,other):
		return self/other, self%other
	def __rdivmod__(self,other):
		return divmod(self,other)
	def __idivmod__(self,other):
		return divmod(self,other)
	
# time range generator
class timeRange(object):
	pos =0
	def __init__(self,end,increment=1,start=0):
		
		self.end = float(end)
		self.increment = float(increment)
		self.start = float(start)
		if self.start > self.end:
			raise ValueError( 'end :{} is smaller than start :{}'.format(self.end,self.start) )
	
	def __len__(self): return int( (self.end-self.start)/self.increment)+1
	def __str__(self): return 'timeRange {}:{}:{}'.format(self.start,self.increment,self.end)
	def __getitem__(self,key):
		if key>=0 and key <= len(self):	return self.start+self.increment*key
		else: raise GeneratorExit
	
	def __contains__(self,item):
		item = float(item) - self.start
		return ( item/self.increment ).is_integer() and int( item/self.increment ) <= len(self)
	
	__setitem__ = None
	__delitem__ = None
	
	def __next__(self):
		if self.pos == len(self):raise GeneratorExit
		self.pos+=1
		return self[self.pos-1]
	next = __next__
	
	def __iter__(self):
		while 1:
			try:
				yield next(self)
			except GeneratorExit:
				break
		self.pos = 0

# oscilator
class signal(object):
	
	step = None # step function, function that returns specific value for some time interval and phase
	phase = 0
	time_stamp = 0
	
	def __init__(self,freq,start_time=None):
		self.value = float(freq)
		self.clock = timeRange(1, 1.0/(self.value*10),0)
		
		if start_time is None:
			self.start_time = 0
		else:
			self.start_time = float(start_time)
			self.clock.start += self.start_time
			self.clock.end += self.start_time
		
		
	def establish_sample_rate(self,freq):
		if self.value*2 >= freq: raise AliasingError('Aliasing occurs for {} '.format(freq) )
		self.clock.increment = float(1.0/freq)
	
	def establish_function(self,funct):
		if type(funct).__name__ not in [ 'function','staticmethod','classmethod' ]:
			raise TypeError( '{} element must a function type, got {}'.format(funct,type(funct).__name__) )
		if funct.__code__.co_argcount != 3: 
			raise RuntimeError( '{} must recept 3 arguments in form of frequency,time signature, phase' )
		self.step = funct
	
	def establish_phase(self,phase,unit='radian'):
		if unit not in [ 'radian' , 'degrees' ]:
			raise ValueError( '{} unit must be a degree or radian' )
		
		if unit=='degrees':
			unit = radians(phase)
		self.phase = phase
	
	def __len__(self): return len(self.clock)
	
	def flush(self):
		self.clock.increment = 1.0/(self.value*10)
		self.clock.end 		 = self.start_time+1
		self.time_stamp      = 0
	
	def __getitem__(self,key):
		return self.step( self.value, self.clock.increment*key, self.phase )
	
	__delitem__ = __setitem__  = None
	
	def __next__(self):
		return self.step( self.value, next(self.clock), self.phase )
	next = __next__
	
	def __iter__(self):
		while 1:
			try:
				yield next(self)
			except GeneratorExit:
				break
		self.flush()
		self.clock.pos = 0
	
	def duration(self,time=None,sample_rate=None):
		if time is not None:
			self.end = float(time)
		if sample_rate is not None:
			self.establish_sample_rate(sample_rate)
		
		while 1:
			try:
				yield next(self)
			except GeneratorExit:
				break
		self.flush()
		self.clock.pos = 0
	
	def __str__(self):
		return '\n{} Hz, end time {}s, time increment {}s'.format( self.value, self.time_end, self.timeRangerement )
	
	def flip_negative(self,time=None,sample_rate=None):
		return ( abs(x) for x in self )
	
	def filter_negative(self,time=None,sample_rate=None):
		return ( x if x>=0 else 0 for x in self )
	
	def get_data(self,time=None,sample_rate=None):
		return {
			'tm':self.clock.end,
			't0':self.clock.start,
			'ti':self.clock.increment,
			'w' : [ x for x in self.duration(time,sample_rate) ]
		}
	
	def sync_sample_rate(self,other):
		if not isinstance(other,signal):
			raise TypeError('{} not a signal class type'.format(other))
		t_inc =max( self.value,other.value ) 
		other.timeRangerement = self.timeRangerement = 1/( t_inc*2+10 )

a = color(hex_i=0x020202)
print( list( zip( a, color(hex_i=0x0f0f0f) ) ) )

print( 1*a )
print( 0.5*a )
print( (1,0xf,0xff)*a )
print(  color( hex_i=0x0f0f0f )*a )
print( '-'*60 )
a*=1
print(a)
