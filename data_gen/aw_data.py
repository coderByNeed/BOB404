#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function,with_statement
from sys import path
from os.path import dirname,abspath,exists
curPath = dirname( abspath( __file__ ) )
path.append(curPath)
del dirname,abspath,path
#:? end of header of audio data

# usable info :https://docs.python.org/2/reference/datamodel.html

#:> meta
__author__ = 'DM <email@email.com'
__licence__	= 'GNU'
__version__ = '0.1'
#:? end of meta

#:> constants
BYTE_MASK 	= 0xff
BYTE		= 8
#:? end of constants

#:> quick functions
chckNIB = lambda n: None if n>0xf else '{3}{2}{1}{0}'.format( *((n>>i)&1 for i in range(4)) ) 
chckBYT = lambda n: chckNIB( (n>>4)&0xf ) + '-' + chckNIB( n&0xf )
lsb_byte					= lambda x,m=0x01:				None if x>0xff \
																	else 0 if x==0 \
																	else m if x&m==m \
																	else lsb_byte( x, m<<1 )
msb_byte					= lambda x,m=0x80:				None if x>0xff \
																	else 0 if x==0 \
																	else m if x&m==m \
																	else msb_byte( x, m>>1 )
unary_2scmp 				= lambda n:						None if n>0xff else n^( 0xff^( ( lsb_byte(n) << 1 )-1 ) )
#:? end of quick functions

#:> errors
class SignedTypeError( TypeError ):pass
class SignedInitError( Exception ):pass
class SignedGetError( Exception ):pass
class SignedFormatError( Exception ):pass
#:? end of errors

#:> functions
LSB = lambda x,m=1: LSB(x,m<<1) if x&m!=m else m
#:? end of functions

#:> objects
# base for analog wave objects
class signed_nth(object):
	
	'''
		implementing signed data type, need bit limited data type to ensure that signal values are confided per compression rules
	'''
	
	pos = 0
	
	def __init__(self,value=None,bits=8):		
		
		self.bit_length = 8 if bits is None else int(bits)
		self.mask_sign  = 2**(self.bit_length-1)
		self.mask_value = 2**(self.bit_length-1)-1
		self.mask_whole = (2**self.bit_length) - 1
		
		try:
			self.value = 0 if value is None \
									else value if isinstance(value,signed_nth) \
									else int( value )&self.mask_whole
		except: raise SignedInitError
		
	def __str__(self):
		return '{0}{1}'.format( '-' if self.value&self.mask_sign==self.mask_sign else ' ' , self.value&self.mask_value )
	
	def __repr__(self):
		return 'signed_nth( bits={}, value={})'.format( self.bit_length, self.value
		)
	
	def __len__(self): return int( self.bit_length/BYTE ) + ( 1 if self.bit_length%BYTE!=0 else 0 )
	
	def __bool__(self):
		return self.value&self.mask_value != 0 and self.value&self.mask_sign!=self.mask_sign
	__nonzero__ = __bool__
	
	def __abs__(self):
		return signed_nth( value = self.value^self.mask_sign, bits=self.bit_length )
	
	def sign(self): return self.value&self.mask_sign
	def __hash__(self): hash( (self.value,self.mask_value,self.mask_sign) )
	
	def __getitem__(self,key):
		if key == 'sign': return self.value&self.mask_sign
		if key == 'value': return self.value
		if key < len(self):
			key = (len(self)-key-1)*BYTE
			return ( self.value&( BYTE_MASK<<key ) )>>key
		raise SignedGetError(' index {} out of bounds {}'.format(key, range(len(self)) ) )
	__setitem__ = __delitem__ = None
	__set__ = __get__ = None
	def __del__	(self):
		del self
	
	def __next__(self):
		if self.pos == len(self): raise GeneratorExit
		self.pos += 1
		return self[self.pos-1]
	next = __next__
	
	def __iter__(self):
		while 1:
			try:
				yield next(self)
			except GeneratorExit: break
		self.pos = 0

	## boolean logic
	
	def __lt__(self,other): return self.value	 <		 ( other.value if hasattr(other,'value') else other )
	def __le__(self,other): return self.value	 <=		 ( other.value if hasattr(other,'value') else other )
	def __gt__(self,other): return self.value	 >		 ( other.value if hasattr(other,'value') else other )
	def __ge__(self,other): return self.value	 >=		 ( other.value if hasattr(other,'value') else other )
	def __eq__(self,other): return self.value	 ==		 ( other.value if hasattr(other,'value') else other )
	def __ne__(self,other): return not self 	 == 	 other
	def __cmp__(self,other): return -1 if self < other else 0 if self == other else 1
	
	#bitwise operators
	
	def __and__(self,other) : 	
		if isinstance(other,signed_nth):return signed_nth( bits= max( self.bit_length, other.bit_length ), value = self.value&other.value )
		else:							return signed_nth( value = self.value&( other&self.mask_whole), bits = self.bit_length )
	def __rand__(self,other): 	return self&other
	def __iand__(self,other): 	return self&other
	
	def __or__(self,other) : 	return signed_nth( value = self.value|( ( other.value if hasattr(other,'value') else other )&self.mask_whole), bits = self.bit_length )
	def __ror__(self,other): 	return self|other
	def __ior__(self,other): 	return self|other
	
	def __xor__(self,other) : 	return signed_nth( value = self.value^( ( other.value if hasattr(other,'value') else other )&self.mask_whole), bits = self.bit_length )
	def __rxor__(self,other):	return self^other
	def __ixor__(self,other): 	return self^other 
	
	def __lshift__(self,other) :return signed_nth( value = ( self.value<< ( other.value if hasattr(other,'value') else other ) )&self.mask_whole, bits = self.bit_length )
	def __rlshift__(self,other):return self<<other
	def __ilshift__(self,other):return self<<other
	
	def __rshift__(self,other) :return signed_nth( value = ( self.value>> ( other.value if hasattr(other,'value') else other ) )&self.mask_whole, bits = self.bit_length )
	def __rrshift__(self,other):return self>>other
	def __irshift__(self,other):return self>>other
	
	#arithmetic operators
	
	def __add__(self,other)		: return signed_nth( bits = self.bit_length, value = self.value + ( other.value if hasattr(other,'value') else other ) )
	def __radd__(self,other)	: return self+other
	def __iadd__(self,other)	: return self+other
	
	def __sub__(self,other)		: return signed_nth( bits = self.bit_length, value = self.value - ( other.value if hasattr(other,'value') else other ) )
	def __rsub__(self,other)	: return self-other
	def __isub__(self,other)	: return self-other
	
	def __mul__(self,other)		:
		other = other.value if hasattr(other,'value') else other 
		other = self.value*other
		other = other if other <= self.mask_whole else self.mask_value
		if self.value&self.mask_sign == self.mask_sign:
			other += self.mask_sign if other&self.mask_sign != self.mask_sign else 0
		
		return signed_nth( bits = self.bit_length, value = other )
	def __rmul__(self,other)	: return self*other
	def __imul__(self,other)	: return self*other
	
	def __truediv__(self,other)		:
		other = other.value if hasattr(other,'value') else other 
		other = int( self.value/float(other) )
		other = other if other <= self.mask_whole else self.mask_value
		if self.value&self.mask_sign == self.mask_sign:
			other += self.mask_sign if other&self.mask_sign != self.mask_sign else 0
		
		return signed_nth( bits = self.bit_length, value = other )
	def __rtruediv__(self,other)	: return self/other
	def __itruediv__(self,other)	: return self/other
	
	def __floordiv__(self,other)	:
		other = other.value if hasattr(other,'value') else other 
		other = int( self.value//float(other) )
		other = other if other <= self.mask_whole else self.mask_value
		if self.value&self.mask_sign == self.mask_sign:
			other += self.mask_sign if other&self.mask_sign != self.mask_sign else 0
		
		return signed_nth( bits = self.bit_length, value = other )
	def __rfloordiv__(self,other)	: return self//other
	def __ifloordiv__(self,other)	: return self//other
	
	def __mod__(self,other)			: return signed_nth( bits = self.bit_length, value = self.value%( other.value if hasattr(other,'value') else other ) )
	def __rmod__(self,other)		: return self%other
	def __imod__(self,other)		: return self%other
	
	def __divmod__(self,other)		: return self//other, self%other
	def __rdivmod__(self,other)		: return divmod(self,other)
	def __idivmod__(self,other)		: return divmod(self,other)
	
	def __pow__(self,other,zeta=None)	: 
		if zeta is None:	return  self**other
		else:				return 	(self**other)%zeta
	def __rpow__(self,other,zeta=None)  : return self.__pow__(other,zeta)
	def __ipow__(self,other,zeta=None)	: return self.__pow__(other,zeta)
	
	#formating operators
	
	def __format__(self,spec):
		return ('{0:'+spec+'}').format( ( self.value^self.mask_sign if not spec.endswith('b') else self.value ) )
	
	#independant operators
	
	def __invert__(self):
		global LSB
		val = LSB(self.value)<<1
		val -= 1
		val = self.mask_value^val
		val = self.value^val
		return signed_nth( bits= self.bit_length, value = val )
	
	def __neg__(self):
		if self.sign() != self.mask_sign: self.value ^= self.mask_sign
		return self
	
	def __abs__(self):
		if self.sign() == self.mask_sign: self.value ^= self.mask_sign
		return self
	
	def __pos__(self):
		if self.sign() == self.mask_sign: self.value ^= self.mask_sign
		return self

# analog wave 8 bit object
class aw_byte(signed_nth):
	
	def __init__(self,signal_value):
		signed_nth.__init__( bits=8, value=signal_value )

# analog wave 8 bit object
class aw_short(signed_nth):
	
	def __init__(self,signal_value):
		signed_nth.__init__( bits=16, value=signal_value )

class aw_long(signed_nth):
	
	def __init__(self,signal_value):
		signed_nth.__init__( bits=24, value=signal_value )
	
