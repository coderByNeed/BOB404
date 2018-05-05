#!/usr/bin/env python
#-*- coding: utf-8 -*-
#wave format manipulation
from __future__ import absolute_import, division, print_function,with_statement
from sys import path
from os.path import dirname,abspath 
path.append( dirname( abspath( __file__ ) ) )

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
        if int_numb&(1<<pos)!=0:return pos+1
        pos+=1

def most_sagnificant_bit(int_numb):
    
    byte = 8
    mask    = 0x8000000000000000
    chk_msk = 0xff00000000000000
    pos = 64
    while 1:
        
        if int_numb&chk_msk==0:
            chk_msk     >>= byte
            mask        >>= byte
            pos         -= 8
        else:
            
            if int_numb&mask==0:
                mask >>= 1
                pos   -= 1
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

def twos_compliment_bytesized(int_numb):
    mask = bytemask(int_numb)
    lsb = least_sagnificant_bit(int_numb)
    return int_numb^(mask^( (lsb<<1) -1 ))

def isAscii(byte_s):
    try:
        byte_s.decode('ascii')
        return True
    except:
        return False

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


####################################################################################################
################################################MAIN################################################
####################################################################################################


compression_format = {
    0x0000:         'UNKNOWN',                  # Microsoft Corporation #
    0x0001:         'PCM',                      # defaultPCM
    0x0002:         'ADPCM',                        # Microsoft Corporation #
    0x0003:         'IEEE_FLOAT',                   # Microsoft Corporation #
    0x0004:         'VSELP',                      # Compaq Computer Corp. #
    0x0005:         'IBM_CVSD',                   # IBM Corporation #
    0x0006:         'ALAW',                       # Microsoft Corporation #
    0x0007:         'MULAW',                      # Microsoft Corporation #
    0x0008:         'DTS',                        # Microsoft Corporation #
    0x0010:         'OKI_ADPCM',                  # OKI #
    0x0011:         'DVI_ADPCM',                  # Intel Corporation #
    0x0012:         'MEDIASPACE_ADPCM',           # Videologic #
    0x0013:         'SIERRA_ADPCM',               # Sierra Semiconductor Corp #
    0x0014:         'G723_ADPCM',                 # Antex Electronics Corporation #
    0x0015:         'DIGISTD',                    # DSP Solutions, Inc. #
    0x0016:         'DIGIFIX',                    # DSP Solutions, Inc. #
    0x0017:         'DIALOGIC_OKI_ADPCM',         # Dialogic Corporation #
    0x0018:         'MEDIAVISION_ADPCM',          # Media Vision, Inc. #
    0x0019:         'CU_CODEC',                   # Hewlett-Packard Company #
    0x0020:         'YAMAHA_ADPCM',               # Yamaha Corporation of America #
    0x0021:         'SONARC',                     # Speech Compression #
    0x0022:         'DSPGROUP_TRUESPEECH',        # DSP Group, Inc #
    0x0023:         'ECHOSC1',                    # Echo Speech Corporation #
    0x0024:         'AUDIOFILE_AF36',             # Virtual Music, Inc. #
    0x0025:         'APTX',                       # Audio Processing Technology #
    0x0026:         'AUDIOFILE_AF10',             # Virtual Music, Inc. #
    0x0027:         'PROSODY_1612',               # Aculab plc #
    0x0028:         'LRC',                        # Merging Technologies S.A. #
    0x0030:         'DOLBY_AC2',                  # Dolby Laboratories #
    0x0031:         'GSM610',                     # Microsoft Corporation #
    0x0032:         'MSNAUDIO',                   # Microsoft Corporation #
    0x0033:         'ANTEX_ADPCME',               # Antex Electronics Corporation #
    0x0034:         'CONTROL_RES_VQLPC',          # Control Resources Limited #
    0x0035:         'DIGIREAL',                   # DSP Solutions, Inc. #
    0x0036:         'DIGIADPCM',                 # DSP Solutions, Inc. #
    0x0037:         'CONTROL_RES_CR10',           # Control Resources Limited #
    0x0038:         'NMS_VBXADPCM',               # Natural MicroSystems #
    0x0039:         'CS_IMAADPCM',                # Crystal Semiconductor IMA ADPCM #
    0x003A:         'ECHOSC3',                    # Echo Speech Corporation #
    0x003B:         'ROCKWELL_ADPCM',             # Rockwell International #
    0x003C:         'ROCKWELL_DIGITALK',          # Rockwell International #
    0x003D:         'XEBEC',                      # Xebec Multimedia Solutions Limited #
    0x0040:         'G721_ADPCM',                 # Antex Electronics Corporation #
    0x0041:         'G728_CELP',                  # Antex Electronics Corporation #
    0x0042:         'MSG723',                     # Microsoft Corporation #
    0x0050:         'MPEG',                       # Microsoft Corporation #
    0x0052:         'RT24',                       # InSoft, Inc. #
    0x0053:         'PAC',                        # InSoft, Inc. #
    0x0055:         'MPEGLAYER3',                 # ISO/MPEG Layer3 Format Tag #
    0x0059:         'LUCENT_G723',                # Lucent Technologies #
    0x0060:         'CIRRUS',                     # Cirrus Logic #
    0x0061:         'ESPCM',                      # ESS Technology #
    0x0062:         'VOXWARE',                    # Voxware Inc #
    0x0063:         'CANOPUS_ATRAC',              # Canopus, co., Ltd. #
    0x0064:         'G726_ADPCM',                 # APICOM #
    0x0065:         'G722_ADPCM',                 # APICOM #
    0x0067:         'DSAT_DISPLAY',               # Microsoft Corporation #
    0x0069:         'VOXWARE_BYTE_ALIGNED',       # Voxware Inc #
    0x0070:         'VOXWARE_AC8',                # Voxware Inc #
    0x0071:         'VOXWARE_AC10',               # Voxware Inc #
    0x0072:         'VOXWARE_AC16',               # Voxware Inc #
    0x0073:         'VOXWARE_AC20',               # Voxware Inc #
    0x0074:         'VOXWARE_RT24',               # Voxware Inc #
    0x0075:         'VOXWARE_RT29',               # Voxware Inc #
    0x0076:         'VOXWARE_RT29HW',             # Voxware Inc #
    0x0077:         'VOXWARE_VR12',               # Voxware Inc #
    0x0078:         'VOXWARE_VR18',               # Voxware Inc #
    0x0079:         'VOXWARE_TQ40',               # Voxware Inc #
    0x0080:         'SOFTSOUND',                  # Softsound, Ltd. #
    0x0081:         'VOXWARE_TQ60',               # Voxware Inc #
    0x0082:         'MSRT24',                     # Microsoft Corporation #
    0x0083:         'G729A',                     # AT&T Labs, Inc. #
    0x0084:         'MVI_MVI2',                   # Motion Pixels #
    0x0085:         'DF_G726',                    # DataFusion Systems (Pty) (Ltd) #
    0x0086:         'DF_GSM610',                  # DataFusion Systems (Pty) (Ltd) #
    0x0088:         'ISIAUDIO',                   # Iterated Systems, Inc. #
    0x0089:         'ONLIVE',                     # OnLive! Technologies, Inc. #
    0x0091:         'SBC24',                      # Siemens Business Communications Sys #
    0x0092:         'DOLBY_AC3_SPDIF',            # Sonic Foundry #
    0x0093:         'MEDIASONIC_G723',            # MediaSonic #
    0x0094:         'PROSODY_8KBPS',              # Aculab plc #
    0x0097:         'ZYXEL_ADPCM',                # ZyXEL Communications, Inc. #
    0x0098:         'PHILIPS_LPCBB',              # Philips Speech Processing #
    0x0099:         'PACKED',                     # Studer Professional Audio AG #
    0x00A0:         'MALDEN_PHONYTALK',           # Malden Electronics Ltd. #
    0x0100:         'RHETOREX_ADPCM',             # Rhetorex Inc. #
    0x0101:         'IRAT',                       # BeCubed Software Inc. #
    0x0111:         'VIVO_G723',                  # Vivo Software #
    0x0112:         'VIVO_SIREN',                 # Vivo Software #
    0x0123:         'DIGITAL_G723',               # Digital Equipment Corporation #
    0x0125:         'SANYO_LD_ADPCM',             # Sanyo Electric Co., Ltd. #
    0x0130:         'SIPROLAB_ACEPLNET',          # Sipro Lab Telecom Inc. #
    0x0131:         'SIPROLAB_ACELP4800',         # Sipro Lab Telecom Inc. #
    0x0132:         'SIPROLAB_ACELP8V3',          # Sipro Lab Telecom Inc. #
    0x0133:         'SIPROLAB_G729',              # Sipro Lab Telecom Inc. #
    0x0134:         'SIPROLAB_G729A',             # Sipro Lab Telecom Inc. #
    0x0135:         'SIPROLAB_KELVIN',            # Sipro Lab Telecom Inc. #
    0x0140:         'G726ADPCM',                  # Dictaphone Corporation #
    0x0150:         'QUALCOMM_PUREVOICE',         # Qualcomm, Inc. #
    0x0151:         'QUALCOMM_HALFRATE',          # Qualcomm, Inc. #
    0x0155:         'TUBGSM',                     # Ring Zero Systems, Inc. #
    0x0160:         'MSAUDIO1',                   # Microsoft Corporation #
    0x0200:         'CREATIVE_ADPCM',             # Creative Labs, Inc #
    0x0202:         'CREATIVE_FASTSPEECH8',       # Creative Labs, Inc #
    0x0203:         'CREATIVE_FASTSPEECH10',      # Creative Labs, Inc #
    0x0210:         'UHER_ADPCM',                 # UHER informatic GmbH #
    0x0220:         'QUARTERDECK',                # Quarterdeck Corporation #
    0x0230:         'ILINK_VC',                   # I-link Worldwide #
    0x0240:         'RAW_SPORT',                  # Aureal Semiconductor #
    0x0250:         'IPI_HSX',                    # Interactive Products, Inc. #
    0x0251:         'IPI_RPELP',                  # Interactive Products, Inc. #
    0x0260:         'CS2',                        # Consistent Software #
    0x0270:         'SONY_SCX',                   # Sony Corp. #
    0x0300:         'FM_TOWNS_SND',               # Fujitsu Corp. #
    0x0400:         'BTV_DIGITAL',                # Brooktree Corporation #
    0x0450:         'QDESIGN_MUSIC',              # QDesign Corporation #
    0x0680:         'VME_VMPCM',                  # AT&T Labs, Inc. #
    0x0681:         'TPC',                       # AT&T Labs, Inc. #
    0x1000:         'OLIGSM',                     # Ing C. Olivetti & C., S.p.A. #
    0x1001:         'OLIADPCM',                   # Ing C. Olivetti & C., S.p.A. #
    0x1002:         'OLICELP',                    # Ing C. Olivetti & C., S.p.A. #
    0x1003:         'OLISBC',                     # Ing C. Olivetti & C., S.p.A. #
    0x1004:         'OLIOPR',                     # Ing C. Olivetti & C., S.p.A. #
    0x1100:         'LH_CODEC',                   # Lernout & Hauspie #
    0x1400:         'NORRIS',                     # Norris Communications, Inc. #
    0x1500:         'SOUNDSPACE_MUSICOMPRESS',    # AT&T Labs, Inc. #
    0x2000:         'DVM',                        # FAST Multimedia AG #
}

# :D MULAW decoding from 8bit integer to 16bit integer
def u_law_d(i8bit):
    i8bit &= 0xff # marginalising data larger than byte
    i8bit ^= 0xff #flipping back bytes
    sign = False
    
    if i8bit&0x80==0x80: # if it is signed negative 1000 0000
        sign = True
        i8bit &= 0x7f # removing the sign of value
    
    
    pos = ( (i8bit&0xf0) >> 4 )+5 # grabing initial value
    
    # generating decoded data
    decoded = i8bit&0xf
    decoded <<= pos-4
    decoded |= 1 << ( pos-5 )
    decoded |= 1<<pos
    decoded -= 0x21
    
    if not sign:
        return decoded
    else:
        return -decoded
    
    

# :D MULAW encoding from 16bit integer to 8bit integer
def u_law_e(i16bit): 
    i16bit &= 0x1fff # strips data bigger than 14 digits
    pos = 12
    msk = 0x1000
    
    sign = 0x80 if i16bit&0x2000 else 0
    
    if sign != 0:
        i16bit = twos_compliment(i16bit)
        i16bit &= 0x3ffe
        
    i16bit+=0b100001
    
    if i16bit > 0x1fff: i16bit = 0x1fff
    
    for x in reversed( range(pos) ):
        if (i16bit & msk)!=msk and pos>=5:
            pos = x
            msk >>=1
        
    LSBTS = ( i16bit >> (pos-4) )&0xf
    
    encoded = sign
    encoded += (pos-5)<<4
    encoded += LSBTS
    
    return encoded^0xff
    
    

def hex_byte(int_d):
    int_d = checkBYT(int_d) if isinstance(int_d,int) else int_d
    int_d = int_d.split('-')
    int_d = map( lambda x: int(x,2),int_d )
    int_d = map( '{0:X}'.format, int_d )
    return ''.join(int_d)

def hex_bytes(int_d):
    return '-'.join(map( hex_byte ,checkBTS(int_d).split(' ') ))

##http://dystopiancode.blogspot.rs/2012/02/pcm-law-and-u-law-companding-algorithms.html

for data in [-0x1fdf,-0x0001, 0x0000, 0x0001, 0x1fdf]:

    e_data = u_law_e(data)
    d_data = u_law_d(e_data)
    
    print(data)
    print('-'*60)
    
    print( 'normal :{0}\t\t{1}\t\t{2}'.format(data, hex_bytes(data) , checkBTS(data) ) )
    print( 'encoded:{0}\t\t{1}\t\t{2}'.format(e_data, hex_bytes(e_data), checkBTS(e_data) ) )
    # print( 'decoded:{0}\t\t{1}\t\t{2}'.format(d_data, hex_bytes(d_data), checkBTS(d_data) ) )
    print('-'*60)
    print()
