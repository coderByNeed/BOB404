CODE DOCUMENTATION
TESTED PY VERSION : 2.7 & 3.5
MODULE: color.py
AUTHOR: Danilo Mitrovic
EMAIL: adewdda@gmail.com 



Purpose of this module is to help and manage color manipulation with complex-ish software. Such module is designed to support virtual assistant application but is built to manage large divirsety of other color type specification

This module is built to support color declaration, color arithmetic manipulation,blending, compression and byte read/write elements. 

LITERATURE:
    wikia :
        -Additive color mix : https://en.wikipedia.org/wiki/Additive_color
        -RGB color model    : https://en.wikipedia.org/wiki/RGB_color_model
        -RGBA color space   : https://en.wikipedia.org/wiki/RGBA_color_space
        -Alpha composting   : https://en.wikipedia.org/wiki/Alpha_compositing
        
    other :
        - Reddit : HEX 3x8bit representation to 3x4bit representation : https://www.reddit.com/r/learnpython/comments/6uyrku/dabefa_to_xxx_representation_hex_color_code/

INSTALATION:
    stand alone module, so just copy or download it from github and use/change it at will. But have in mind next: I am not responsible with any user changes that may oncur. If code is not documented, i can not help anyone who needs clarification or implementation advice.

LICENCE for color.py
GNU opensource licence

##########################################################################################################################################################################################

FUNCTION: range_multiplier:

INPUT: int: r1,r2 > maximum value of 2 ranges
RETURN: floating number in range 0-1
ONFALSE: returns -1

NOTE: The use of this function is so we can get relations between ranges, so we can easly translate values from 1 range to another one

##########################################################################################################################################################################################

FUNCTION: range_coeficient:

INPUT: number: range,value > maximum value of some range as reference point, and value of such range
RETURN: floating number in range 0-1
ONFALSE: returns -1

NOTE: Another way of translation of value, returns relation of value in proportion to the range

##########################################################################################################################################################################################

FUNCTION: bit_range:

INPUT: int: number of bits
RETURN: integer
formula : pow(2,number of bits)
ONFALSE: returns None

NOTE: This function returns possible number of element values in specific number of bit places

##########################################################################################################################################################################################

FUNCTION: bit_max_val
INPUT: int: number of bits
RETURN: integer
formula : pow(2,number of bits)-1
ONFALSE: returns None

NOTE: The function returns maximum value for number of bits presented

##########################################################################################################################################################################################

OBJECT CLASS: color
RETURN: color object
CHANNELS: RGBA = red, green, blue, alpha

INITIALISATION

    DEFAULT INITIALISATION:
        black = color() # 0,0,0 :1
        
    ARGUEMNTED INITIALISATION:
        -> args =>> color(*args)
        -> input range from int,float,bool,complex,bytes,list,tuple,str,unicode,dict
       
        # default full gray
        collor = color(input) 
            RESULT: collor = color(red=input,green=input,blue=input,alpha=1)
        
        # default color difference
        collor = color(input1,input2,input3,input4)
            RESULT: collor = color(red=input1,blue=input2,blue=input3,alpha=input4)

    KEY WORD ARGUEMNTED INITIALISATION:
        -> kwargs =>> color(**kwargs) kwargs in dict
        -> input range from int,float,bool,complex,bytes,list,tuple,str,unicode,dict
        
        # default color difference
        collor = color(red=input1,green=input2,blue=input3,alpha=input4)
        
        NOTE: Can not initialise easly default gray this way

SPECIFIC FUNCTIONS:
    
    -------------------------
    FUNCTION: manage_input
    INPUT: input: int,float,bool,complex,bytes,list,tuple,str,unicode,dict
    RETURN: integer in range 0-255 + float derivatives
    formula : LOGIC CONVERSION BASED, in passed tuple,list,dict : returns 
    ONFALSE: returns 0

    NOTE: This is conversion based function, have no large contribution outside class.Also uses manage_external
    
    -------------------------
    FUNCTION: manage_external
    INPUT: input: list,tuple,dict
    RETURN: color
    formula : LOGIC CONVERSION BASED
    ONFALSE: returns 0
        
    -------------------------
    FUNCTION: implement_opacity
    INPUT: NOTHING, VOID
    RETURN: color copy
    formula : setting implementation opacity with attributes
    ONFALSE: VOID function - NO_FALSE
        
    -------------------------
    FUNCTION: values
    INPUT: NOTHING, VOID
    RETURN: list of color values : function copied from dict 
    formula : foreach x in color
    ONFALSE: VOID function - NO_FALSE
        
    -------------------------
    FUNCTION: keys
    INPUT: NOTHING, VOID
    RETURN: list of color attributes : function copied from dict 
    formula : foreach xatr in color
    ONFALSE: VOID function - NO_FALSE
        
    -------------------------
    FUNCTION: items
    INPUT: NOTHING, VOID
    RETURN: list of tuples in tuple form of xatr:xvalue
    formula : foreach x,y in color
    ONFALSE: VOID function - NO_FALSE
        
    -------------------------
    FUNCTION: values
    INPUT: NOTHING, VOID
    RETURN: list of color values : function copied from dict 
    formula : foreach x in color
    ONFALSE: VOID function - NO_FALSE
    
    -------------------------
    FUNCTION: has_key
    INPUT: STR: attribute name
    RETURN: BOOL: True/False
    formula : bool getitem
    ONFALSE: FALSE
    NOTE: for checking value , equivelent is __contain__ in syntax xval in color
        
    -------------------------
    FUNCTION: web_color
    INPUT: BOOL: SHORT
    RETURN: STR: HEX representation
    formula : foreach x in color
    ONFALSE: NO_FALSE simple conversion
          
    -------------------------
    FUNCTION: common_denominator : aka step
    INPUT: INT: DENOMINATOR = None
    RETURN: COLOR
    formula : converts color values to elements of INPUT
    ONFALSE: NO_FALSE simple conversion  
          
    -------------------------
    FUNCTION: mix_over : additive mix
    INPUT: COLOR: OTHER
    RETURN: COLOR
    formula : additive blend of 2 colors, 
    ONFALSE: NO_FALSE simple conversion  

    
    
