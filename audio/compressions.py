#!/usr/bin/env python
#-*- coding: utf-8 -*-
# compression algorythms
from __future__ import absolute_import, division, print_function,with_statement
from sys import path
from os.path import dirname,abspath 
path.append( dirname( abspath( __file__ ) ) )

#--------------------------------------------------------------------------------------------------#
#-----------------------------------------------HEAD-----------------------------------------------#
#--------------------------------------------------------------------------------------------------#


## WAVE FILE IMPORTING------------------------------------------------------------------------------
from struct import pack,unpack

## WAVE FILE CLEANUP -------------------------------------------------------------------------------
##>> METADATA
__author__ = 'Danilo Mitrovic ,'
__credits__ = ''
__copyrights__ =''
__licence__ = 'GNU'
__version__ = '1.01'
__maintainer__ = __author__
__email__ = 'adewdda@gmail.com'
__status__ = 'Development'
__contact__ = 'not yet'

## WAVE FILE GLOBAL VARIABLES-----------------------------------------------------------------------
BITMASK = 1
NIBMASK = 0XF
BYTMASK = 0XFF

NIBSHIFT= 4
BYTSHIFT= 8

## WAVE FILE DEF FUNCTIONS--------------------------------------------------------------------------

def least_sagnificant_bit(int_numb): ##returns position of the bit not the value of the bit
    if int_numb == 0 : return 0
    pos = 0
    while 1:
        if int_numb&(BITMASK<<pos)!=0:return pos+1
        pos+=1

def most_sagnificant_bit(int_numb):
    
    BYTSHIFT = 8
    mask    = 0x8000000000000000
    chk_msk = 0xff00000000000000
    pos = 64
    while 1:
        
        if int_numb&chk_msk==0:
            chk_msk     >>= BYTSHIFT
            mask        >>= BYTSHIFT
            pos         -=  BYTSHIFT
        else:
            
            if int_numb&mask==0:
                mask >>= BITMASK
                pos   -= BITMASK
            else:
                break
        
        if pos == 0:break
    return pos

def bytemask(int_numb,mask=None):
    msk = 0
    i = 0
    while 1:
        
        msk += BYTMASK<<(i*8)
            
        if int_numb&msk == int_numb:
            return msk
        i+=1

def twos_compliment(int_numb):
    if not int_numb: return ~int_numb
    
    lsb = least_sagnificant_bit(int_numb)
    msb = most_sagnificant_bit(int_numb)
    mask = ( 1<<lsb )-1
    mask ^= ( 1<<msb )-1
    return int_numb^mask

## WAVE FILE GLOBAL FUNCTIONS-----------------------------------------------------------------------

# :D unpacking
u_signed_8bit_l = lambda *x: unpack( '<'+'h'*len(x), *x ) if len(x)==1 \
                                        else unpack( '<'+'h'*len(x), *x )[0]
u_unsgnd_8bit_l = lambda *x: unpack( '<'+'H'*len(x), *x ) if len(x)==1 \
                                        else unpack( '<'+'H'*len(x), *x )[0]
u_unsgnd_16bt_l = lambda *x: unpack( '<'+'I'*len(x), *x ) if len(x)==1 \
                                        else unpack( '<'+'I'*len(x), *x )[0]

# :D packing
p_signed_8bit_l = lambda *x: pack( '<'+'h'*len(x), *x ) if len(x)==1 \
                                        else pack( '<'+'h'*len(x), *x )[0]
p_unsgnd_8bit_l = lambda *x: pack( '<'+'H'*len(x), *x ) if len(x)==1 \
                                        else pack( '<'+'H'*len(x), *x )[0]
p_unsgnd_16bt_l = lambda *x: pack( '<'+'I'*len(x), *x ) if len(x)==1 \
                                        else pack( '<'+'I'*len(x), *x )[0]

# :D byte conversion
bit_to_int = lambda x: ord(x) if type(x) != int else x

checkNIB = lambda x: '{0:04b}'.format(x) if x else '0000'
checkBYT = lambda x: '-'.join( map( checkNIB, [ (x>>4)&0xf, x&0xf] ) ) 
checkBTS = lambda x: ' '.join( [ checkBYT( ( x>>(shift*8) )&0xff ) for shift in reversed( range(4) ) ])

def hex_byte(int_d):
    int_d = checkBYT(int_d) if isinstance(int_d,int) else int_d
    int_d = int_d.split('-')
    int_d = map( lambda x: int(x,2),int_d )
    int_d = map( '{0:X}'.format, int_d )
    return ''.join(int_d)

def hex_bytes(int_d):
    return '-'.join(map( hex_byte ,checkBTS(int_d).split(' ') ))

####################################################################################################
################################################MAIN################################################
####################################################################################################

## :D G.711 µ LAw
# :D MULAW decoding from 8bit integer to 16bit integer
def u_law_d(i8bit):
    i8bit &= 0xff # marginalising data larger than byte
    i8bit ^= 0xff #flipping back bytes
    sign = False
    
    if i8bit&0x80==0x80: # if it is signed negative 1000 0000
        sign = True # bool option since sign is not really used
        i8bit &= 0x7f # removing the sign of value
    
    
    pos = ( (i8bit&0xf0) >> 4 )+5 # grabing initial value for mantisa
    
    # generating decoded data
    decoded = i8bit&0xf # grabing 1st nibble from 8 bit integer
    decoded <<= pos-4   # shifting by position -4 aka generating mantisa for 16 bit integer
    decoded |= 1 << ( pos-5 ) # OR gate for specific bit
    decoded |= 1<<pos   # OR gate for another specific bit
    decoded -= 0x21 # removing the 10 0001 from value to generate exact value
    
    if not sign:
        return decoded  # if positive number will be returned as is
    else:
        return -decoded # if negative the number will be returned inverted

# :D MULAW encoding from 16bit integer to 8bit integer
def u_law_e(i16bit): 
    i16bit &= 0x3fff # strips data bigger than 14 bits
    pos = 12        # position is 12 since we are not calculating sign bit and 0 value so 14 - sign == 13; so 13 bits, - 0 value ... 12 bits
    msk = 0x1000    # mask 1 0000 0000 0000 # bitwise mask for singular bits
    
    sign = 0x80 if i16bit&0x2000 else 0 # generating 8bit sign from 14 bit number 
    
    if sign == 0x80: # if sign is present
        i16bit = twos_compliment(i16bit) # twos_compliment 
        i16bit &= 0x3ffe               # strips all bits larger than 14 bits
    
    i16bit+=0b100001                    # adds 33, 0x21 = 10 0001
    
    if i16bit > 0x1fff: i16bit = 0x1fff # if number is over maximum ... it becomes maximum
    
    for x in reversed( range(pos) ):    # this number has least significant bits, not bit... so they have often size of 4 bits, that is why it must be larger than 5
        if (i16bit & msk)!=msk and pos>=5:
            pos = x
            msk >>=1
        
    LSBTS = ( i16bit >> (pos-4) )&0xf # grabbing mantissa from 16 bit integer
    
    
    encoded = sign          # sign
    encoded += (pos-5)<<4    # exponent
    encoded += LSBTS        # mantisa
    
    return encoded^0xff # inverting all bits
     

ulaw_Data = [-0x1fdf,-0xfef,-0x0001, 0x0000, 0x0001,0xfef, 0x1fdf]

form = lambda x: '{0}\t:>\t{1}\t||\t{2}'.format( x, hex_bytes(x), checkBTS(x) )


print('-'*120)
print('-'*120)

for data in ulaw_Data:
    
    print('')
    
    data &= 0x3fff
    print( 'normal :\t'+form(data) )
    
    e_data = u_law_e(data)
    print( 'encoded:\t'+form(e_data) )
    
    d_data = u_law_d(e_data)
    print( 'decoded:\t'+form(d_data) )
    
    print('-'*120)

print('-'*120)












