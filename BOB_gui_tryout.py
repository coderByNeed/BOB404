from __future__ import absolute_import, division, print_function, unicode_literals,with_statement
from sys import version as maj_ver
from time import sleep
maj_ver = maj_ver[0:3] # establishing major version


if maj_ver == '2.7':
    import Tkinter as TK
    import ttk as ttk_formats
else:
    import tkinter as TK
    from tkinter import ttk as ttk_formats ## contains tkinter inside this module


def color2Hex(val):
    
    if not isinstance(val, (list,tuple) ):
        val = (val,val,val)
    else:pass
    
    val = map( lambda x: x&0xff , val )
    val = map( '{0:02X}'.format, val )
    return '#'+"".join(val)

def hex2Color(val):
    
    if maj_ver == '3.5' and not isinstance(val,str): return val
    elif maj_ver == '2.7' and not isinstance(val,unicode):return val
    else:pass
    
    
    val = val.replace('#','')
    val = ['0x'+val[x:x+2] for x in range( len(val) ) if x%2==0 ]
    val = map( lambda x: int(x,16),val )
    return val if maj_ver == '2.7' else list(val)

class BOB404(object): # need referent system for eye..sort of center point to define it.
        
    def __init__(self):
        # self constants
        self.width = 400
        self.height = 400
        self.background = '#050555'
        self.foreground = '#550FFF'
        
        self._center = ( self.width/2,self.height/2 )
        self._radius_eye = int( (self.height+self.width)/4 )
        self._radius_hole = int( (self.height+self.width)/8 )
        
        self._start_pos = {
            'iris':(self.width/4,self.height/4,self.width*(3/4),self.height*(3/4)),
            'iris_hole':(self.width*(3/8),self.height*(3/8),self.width*(5/8),self.height*(5/8)),
            'top_lid':(self.width/4,0, self.width*(3/4),self.height/8),
            'btmn_lid':(self.width/4,self.height*(7/8), self.width*(3/4),self.height)
        }
        
        #root
        self._root = TK.Tk()
        self._root.title('BOB d_404')
        self._root.resizable(width=False, height=False)
        self._root.geometry( '{}x{}'.format(self.width,self.height) )
        
        #bob
        self.BOB = TK.Canvas( self._root, width=self.width, height=self.width,bg=self.background,highlightthickness=0 )
        
        self.iris = self.BOB.create_oval( fill=self.foreground,outline="", *self._start_pos['iris'] )
        self.iris_hole = self.BOB.create_oval(fill=self.background,outline="", *self._start_pos['iris_hole'] )
        
        self.top_lid = self.BOB.create_rectangle(fill= self.foreground,outline="", *self._start_pos['top_lid'] ) # self.background # ARC BETTER SUITING
        self.btmn_lid = self.BOB.create_rectangle(fill= self.foreground,outline="", *self._start_pos['btmn_lid'] ) # self.background
    
    def _draw_circle(self,origin_x,origin_y,radius=self._radius_eye,**kwargs):
        
        tkinter_dimension = [  origin_x-radius , origin_y-radius , origin_x+radius, origin_y+radius ]
    
    def _start(self):
        self.BOB.pack()
        self._root.mainloop()
    
    def _angry(self):
        
        cur_color = self.BOB.itemcget(self.iris,'fill')
        cur_color = hex2Color(cur_color)
        cur_color[0]+=0xf
        cur_color[1]-=0xf
        cur_color[2]-=0xf
        cur_color = map(abs,cur_color)
        cur_color = list(cur_color)
        
        dims = self.BOB.coords(self.iris_hole)
        self_trick = int( (self.width+self.height)/20 )
        dims[0]+=self_trick/2
        dims[2]-=self_trick/2
        
        self.BOB.itemconfig( self.iris, fill=color2Hex(cur_color) )
        self.BOB.coords( self.iris_hole, *dims )
        action = self._root.after( 50 , self._angry )
        
        if cur_color[0] <= 0xf0:pass
        else:
            self._root.after_cancel(action)

    def normal_look(self):
        self.BOB.itemconfig( self.iris, fill=self.foreground )
        self.BOB.coords( self.iris_hole, *self._start_pos['iris_hole'] )
    
    def look_left(self,function=None):
        
        if function == None:
            tick_dist = 2
        else:
            tick_dist = function(2)
        
        self.BOB.move(self.iris,tick_dist,0)
        self.BOB.move(self.iris_hole,tick_dist,0)
        
        coord_iris = self.BOB.coords(self.iris)[2]
        tick = self._root.after(5,self.look_left,function) # recursive repetition
        
        if int(coord_iris) >= self.width: # repetition cancelation
            self._root.after_cancel(tick)
            self._root.after_cancel(tick)
    
    # to do: reset poisition, look left, look right, look up,look down, movement function

from fractions import gcd

def biggest_step(numb1,numb2):
        
    if numb1 == 0 or numb2 == 0: return 0
        
    mx = numb1 if numb1>numb2 else numb2
    mn = numb1 if numb1<numb2 else numb2
    
    test = lambda x: mx%x==0 and mn%x==0
    
    res = filter(test, range(1,mn+1,1) )
    res = list(res)
    
    if res == []: return 1
    if len(res)==1: return res[0]
    return max(res)
        
    
def hex_tick(col1,col2,desired = None):
    
    med_tupl = lambda x: x[0]-x[1]
    
    col1 = hex2Color(col1)
    col2 = hex2Color(col2)
    
    desired = desired if desired != None else\
            col1 if col1<col2 else col2
    
    if col1 > col2:
        result = map(med_tupl, zip(col1,col2) )
    else:
        result = map(med_tupl, zip(col2,col1))
    
    result = list(desired)
    
    for x,y in zip(result,desired):
        print(x,y, biggest_step(x,y) )

colorLetters = [ x for x in range(0,0xff+1,5) if x!=0 and 0xff%x==0 ]

def funct_col():
    for x in colorLetters:
        for y in colorLetters:
            for z in colorLetters:
                t = color2Hex( (x,y,z) )
                yield t

# for x in funct_col():print(x)

if __name__ == '__main__':
    bob = BOB404()
    # bob._angry()
    bob._start()