from __future__ import absolute_import, division, print_function, unicode_literals,with_statement
from color import rgb_colorSet,cmyk_colorSet,isColor


red,green,blue = rgb_colorSet
cyan,magenta,yellow,key = cmyk_colorSet

wholeSet = rgb_colorSet+cmyk_colorSet
wholeSet+=[red+green+blue]

"""
    
    color representation to bits aka bit places to store 1/0
        needs color_representation value : color_sum or color_channel
        needs bits_range for bit places: max bit value of the range pow(2,place)-1 : removes 0 as value
    
    division:
        needs a form of universal range representation
        needs a form of range translation
        needs a form of color value representation
        
"""

# generate reciprocity
range_multiplier = lambda r1,r2: float(r1)/r2 if r1>r2 else float(r2)/r1
value_range_coeficient = lambda val,range: val/range

#bit range manipulation
bit_max_range = lambda x: 2**x  # calculates the number of elements per bit place
bit_max_value = lambda x: (2**x)-1 # calculates the max value of element per bit place

def define_bit_offset(bit_place,numb_offset=None): # return integer
    
    """
        numb offset aka, RGB places, there fore if number of offsets is not defined, the default number is 3
        
        bit_place : is number of places such bits can hold, max value is 2**bit_place -1
        
    """
    
    
    numb_offset = 3 if numb_offset==None else numb_offset
    bit_place = int(bit_place) #defaulting number of bit offset
    
    # generating minimal offset : int generator
    offset = [ int(bit_place/numb_offset) ]*numb_offset
    
    if bit_place%numb_offset: # if moduo ( remainder ) exists
        # distribute moduo equaly to the next places
        if bit_place%numb_offset == 1:
            offset[0]+=1
        else:
            offset[0]+=1
            offset[1]+=1
    
    # checksum test
    if sum(offset)==bit_place:
        return offset

def shift_value_to_range(value_range,result_range): # return float
    
    """
        generates guessed value for new range
        The logic behind it is derived from existing relation from value and its max range value
            so the basic idea is to generate proportion value within 0 to 1 to represent relation between value and its range
        the return is just multiplying the result range with generated proportion value
        
        input : value_range:
            tuple if int:value , int range:
        input : result_range:
            int result_range
    """
    
    # type errors
    if not isinstance(value_range, (list,tuple) ):
        raise TypeError('{!s} must be tuple or list in formulation of value:range pair'.format(value_range) )
    if not isinstance(result_range,int):
        raise TypeError('{} must be of value integer, since floating ranges dont exist in PC worlds')
    
    # value errors
    if isinstance(value_range, (list,tuple) ) and value_range[0]>value_range[1]:
        raise ValueError('{!r} must have formulation of value:range where value<=range'.format(value_range))
    if len(value_range)>2:
        raise ValueError(' {} != 2 for {!r}, desired formulation must be pair of value:range with length of 2'.format(len(value_range),value_range) )
    
    # if result range and given range is the same no need for unnecessery calculation
    if value_range[0]==value_range[1]: return result_range    
    # said calculation: 
        #:: value_range_coeficient: multiplier of value/range
        #:: result range*coeficient : floatish result
    return value_range_coeficient(*value_range)*result_range

def shift_monocrhome_to_bits(collor,bit_place): # return ints
    
    """
        generate unique value for color then convert it to True/False in bit form 
    """
    
    if not isinstance(bit_place,int):
        raise TypeError("{} must be an int, but got a {}".format( bit_place, type(bit_place).__name__ ) )
    if not isColor(collor):
        raise TypeError('{} must be color, but got a {}'.format(collor,type(collor).__name__) )
    
    v_c = value_range_coeficient(sum(collor.values())/len(collor) , 0xff)
    
    return 0 if v_c<.5 else bit_max_value(bit_place)

def shift_grayscale_to_bits(collor,bit_place):  # return integer
    
    """
    
    confines grayscale color object to the 1 int bit 
    grab color value, generates 1 integer arythmetic sum
    adds multiplier by magic function and then returns integer range
    """
    
    if not isinstance(bit_place,int):
        raise TypeError("{} must be an int, but got a {}".format( bit_place, type(bit_place).__name__ ) )
    if not isColor(collor):
        raise TypeError('{} must be color, but got a {}'.format(collor,type(collor).__name__) )
    
    collor = value_range_coeficient( sum(collor.values())/len(collor), 0xff ) #float < magic function
    collor *=bit_max_value(bit_place) # still float
    
    if ( collor - int(collor) )>=.5: collor+=1
    return int(collor)# returns an integer value

def shift_color_to_bits(collor,bit_place):
    
    # generating neccesery bit places
    b_places = (bit_place,len(collor))
    b_places = define_bit_offset(*b_places)
    b_places = map(int,b_places)
    b_places = list(b_places) if not isinstance(b_places,list) else b_places
    
    # checksum
    if not sum( list(b_places) )==bit_place:
        raise ArithmeticError('error, sum of offsets does not match the places of bits required')
    
    offset = []
    oa = offset.append
    for x in b_places:
        bit_place = bit_place-x
        oa(bit_place)
    
    if not ( max( offset )+max( list(b_places) ) )==sum( list(b_places) ):
        raise ArithmeticError('offset of max values of offset and derived bit places dont equal to inputed bit places')
    
    #generating tuples for color value, bit places, max range
    
    c_val = collor.values() # color value list
    c_val = list(c_val)
    
    c_range = zip( c_val, [255]*len(c_val) )
    c_range = zip( c_range, [ (2**i)-1 for i in b_places ] )
    c_range = map( lambda x: shift_value_to_range(*x) , c_range )
    c_range = map(int,c_range)
       
    result = [ xc<<off for xc,off in zip(c_range,offset) ]
    return sum(result)

## mixing of colors

print( cyan )
print( (cyan/2+magenta/2)&blue )

def mixing_test(colora,colorb):
    
    b = key
    
    for xatr in colora.attributes:
        b[xatr]=(colora[xatr]+colorb[xatr])/2
    return b

