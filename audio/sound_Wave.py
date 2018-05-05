#!/usr/bin/env python
#-*- coding: utf-8 -*-
#base classes
from __future__ import absolute_import, division, print_function,with_statement
from sys import path
from os.path import dirname,abspath 
curPath = dirname( abspath( __file__ ) )
path.append(curPath)

# https://en.wikipedia.org/wiki/G.711
# http://einstein.informatik.uni-oldenburg.de/rechnernetze/pcm.htm
# http://web.archive.org/web/19991115123323/http://www.borg.com/~jglatt/tech/wave.htm
# https://sites.google.com/site/musicgapi/technical-documents/wav-file-format#fact
# https://www.lpi.tel.uva.es/~nacho/docencia/ing_ond_1/trabajos_03_04/sonificacion/cabroa_archivos/img/wave1.gif
# http://www.recordingblogs.com/wiki/data-chunk-of-a-wave-file
# https://stackoverflow.com/questions/18345900/itu-t-g-711-c-source-code-to-java-jni
# http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/WAVE.html
# https://github.com/gcc9108/Audio-Compression/blob/ab8958cc24dc8565d493c2753d917225b7703a92/Formula/mulaw.c


from struct import unpack,pack

testpath = 'H:\\pyDMmod\\py_assist\\audio\\audio-alphabet\\A.wav'

ununsignedShort = lambda x: unpack('H',x)
unsignedInt = lambda x: unpack('<I',x)
signedShort = lambda x: unpack('h',x)[0]

wave_format = {
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

def isAscii(bstr):
    return all( ord(b)<128 for b in bstr )

def isCompressed(filepath):
    filepath = open(filepath,mode='rb')
    filepath.seek(20)
    comp = filepath.read(2)
    filepath.close()
    if ununsignedShort( comp ) != 1: return True
    else : False
 
def twos_compliment(int_byte):
    
    if not isinstance(int_byte,int): raise TypeError
    
    if int_byte<=0xff: r = 1
    elif int_byte<=0xffff: r=2
    elif int_byte<=0xffffffff: r  = 4
    elif int_byte<= 0xffffffffffffffff: r = 8
    else: raise TypeError
    
    for nib in range( r*2 ):
        nib*=4
        
        if ( int_byte>>nib )&0xf:
            
            for bit in [1,2,4,8]:
                
                if ( ( int_byte>>nib )&0xf )&bit:
                    nib_shift = nib+bit
                    return ( ~int_byte )^( 2**nib_shift - 1 )

check4bits = '{0:04b}'.format
checkByte = lambda x: '\t'.join( [ check4bits( ( x>>(shift*4) )&0xf ) for shift in reversed( range(2) ) ] )
checkBytes= lambda x: '\t'.join( [ checkByte( ( x>>(shift*8) )&0xff ) for shift in reversed( range(4) ) if ( x>>(shift*8) )&0xff ] )

print( twos_compliment(1) )



##compression

def uLaw_d(i8bit):
    bias = 33
    sign = pos = 0
    decoded = 0
    
    i8bit = ~i8bit
    if i8bit&0x80:
        i8bit &= ~(1<<7)
        sign = -1
    
    pos = ( (i8bit&0xf0) >> 4 ) + 5
    decoded = ((1 << pos) | ((i8bit & 0x0F) << (pos - 4)) | (1 << (pos - 5))) - bias
    return decoded if sign else ~decoded

def uLaw_e(i16bit):
    MAX = 0x1fff
    BIAS = 33
    mask = 0x1000
    sign = lsb = 0
    pos = 12 
    
    if i16bit < 0:
        i16bit = -i16bit
        sign = 0x80
    
    i16bit += BIAS
    
    if ( i16bit>MAX ): i16bit = MAX 
    
    for x in reversed(range(pos)):
        if i16bit&mask != mask and pos>=5:
            pos = x
            break
    
    lsb = ( i16bit>>(pos-4) )&0xf
    return ( ~( sign | ( pos<<4 ) | lsb ) )


    

# get byte places
 
def getRIFF_i(filepath):
    file = open( filepath, mode ='rb' )
    x = file.readline().index(b'RIFF')
    file.close()
    return x

def getWave_i(filepath):
    file = open( filepath, mode = 'rb'  )
    x = file.readline().index(b'fmt')
    file.close()
    return x

def getComp_i(filepath):
    file = open( filepath, mode='rb' )
    x = file.readline().index(b'fact')
    file.close()
    return x
   
def getData_i(filepath):
    file = open( filepath , mode = 'rb' )
    x = file.readline().index(b'data')
    file.close()
    return x

def countData_i(filepath):
    file = open(filepath, mode='rb')
    i = file.readlines()[0].count(b'data')
    file.close()
    return i


# get byte data

def unpackHeader(filepath):
    length = 12
    i = getRIFF_i(filepath)
    
    header = open( filepath, mode = 'rb' )
    header.seek(i)
    header_data = header.read(length)
    header.close()
    
    return { 'ID':header_data[:4], 'SIZE[B]': unsignedInt( header_data[4:8] )[0], 'TYPE': header_data[8:] }

def unpackFormat(filepath):
    i = getWave_i(filepath)
    length = 0x1a
    
    wave = open(filepath, mode='rb')
    wave.seek(i)
    format = wave.read(length)
    wave.close()
    
    return {
        'ID': format[:4],
        'SIZE[B]': unsignedInt( format[4:8] )[0],
        'COMPR': wave_format[ ununsignedShort( format[8:10] )[0] ],
        'CHNLS': ununsignedShort( format[10:12] )[0],
        'S_RATE': unsignedInt( format[12:16] )[0], #sample rate
        'aBPS': unsignedInt( format[16:20] )[0], # avrage bytes per second ## speed
        'B_ALIGN': ununsignedShort( format[20:22] )[0], #block align
        'sBPS': ununsignedShort( format[22:24] )[0],    #significant BPS
        'EXTRA': ununsignedShort( format[24:] )[0]
    }

def unpackCompression(filepath):
    i = getComp_i(filepath)
    length = 12
    
    file = open(filepath, mode='rb')
    file.seek(i)
    comp = file.read(length)
    file.close()
    
    return { 'ID': comp[:4], 'SIZE[B]': unsignedInt(comp[4:8])[0] , 'DATA':unsignedInt(comp[8:])[0] }

def unpackData(filepath,i=None,length=None):
    i = i if i is not None else getData_i(filepath)
    
    file = open(filepath,mode='rb')
    file.seek(i)
    
    ID = file.read(4)
    SIZE = unsignedInt( file.read(4) )[0]
    data = file.read(SIZE)
    
    file.close()
    
    return { 'ID':ID, 'SIZE[B]':SIZE, 'DATA':data}

## write wav file
def packHeader(**kwargs):
    ID = kwargs.get('ID') if kwargs.get('ID') else b'RIFF'
    TYPE = kwargs.get('TYPE') if kwargs.get('TYPE') else b'WAVE'
    return ID+pack( '<I', kwargs.get('SIZE[B]'))+TYPE

def packFormat(**kwargs):

    ID = kwargs.get('ID') if kwargs.get('ID') else b'fmt'
    SIZE = kwargs.get('SIZE[B]')                            #int
    COMPR = [ k for k,v in wave_format.items() if kwargs.get('COMPR')==v ][0] if kwargs.get('COMPR') else 1   #short
    CHNLS = kwargs.get('CHNLS') if kwargs.get('CHNLS') else 1   #short
    S_RATE = kwargs.get('S_RATE')                           #int
    aBPS = kwargs.get('aBPS')                               #int
    B_ALIGN = kwargs.get('B_ALIGN')                         #short
    sBPS = kwargs.get('sBPS')                               #short
    EXTRA = kwargs.get('EXTRA')                              #short
    
    return ID + pack( '<I',SIZE) + pack( '<H',COMPR) + pack( '<H',CHNLS) + pack( '<I',S_RATE) + pack( '<I',aBPS) + pack( '<H',B_ALIGN) + pack( '<H',sBPS) + pack( '<H',EXTRA)                         

def pack_Linear_Data(*data):
    ID = b'data'
    data = pack( '<'+'h'*len(data), *data )
    SIZE = len(data) #RAW linear data is short int aka 2 bytes
    return ID + pack( '<I', SIZE ) + data

new_header = unpackHeader(testpath)
new_format = unpackFormat(testpath)
new_format['COMPR']='PCM'
new_data = unpackData(testpath)

data = map(lambda x: x if isinstance(x,int) else ord(x),new_data['DATA'])
data = map( uLaw_d, data )
data = list(data) if not isinstance(data,list) else data
new_data_length = len( list(data) )

# import wave
# #succes!!!
# file = wave.open('new_A.wav',mode='wb')
# file.setcomptype('NONE','PCM')
# file.setnchannels(1)
# file.setframerate(8000)
# file.setsampwidth(2)
# file.writeframesraw( pack( '<'+'h'*new_data_length, *data ) )


# file.close()

from winsound import PlaySound,SND_FILENAME

# PlaySound( testpath,SND_FILENAME)
