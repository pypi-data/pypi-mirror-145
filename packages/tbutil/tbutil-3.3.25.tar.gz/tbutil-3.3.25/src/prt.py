import time,os
from copy import deepcopy as dc
from tb.std import *

#Screen Config
WIDTH=49
HEIGHT=23
#For limit the size of the output board
#Please let it well
#Best size (for me):49x23

board=[' ']*WIDTH*HEIGHT
cache=[]
board_lmfs='''\
 _          _          _   _________   _________ 
| |        | \        / | |  _______| |  _____  |
| |        |  \      /  | | |         | |     |_|
| |        |   \    /   | | |         | |        
| |        | |\ \  / /| | | |_______  | |_______ 
| |        | | \ \/ / | | |  _______| |_______  |
| |        | |  \__/  | | | |By laman29       | |
| |        | |        | | | |292001748 _      | |
| |______  | |        | | | |         | |_____| |
|________| |_|        |_| |_|         |_________|


'''
def dot(row,col,s):
    board[row*WIDTH+col]=s
def line(row,col,s,trans=False):
    for i in range(len(s)):
        if not(trans and s[i]==' ')and -1<col+i<WIDTH:
            dot(row,col+i,s[i])
def rect(row,col,r,trans=False):
    for i in range(len(r)):
        if -1<row+i<HEIGHT:
            line(row+i,col,r[i],trans=trans)
def flush(*a):
    global board
    _board=dc(board)
    for _layer in cache:
        rect(_layer['row'],_layer['col'],_layer['r'])
    board,_board=_board,board
    x=WIDTH
    y=-1
    _board0=[]
    for i in range(len(_board)):
        if x==WIDTH:
            x=0
            y+=1
            _board0.append([])
        _board0[y].append(_board[i])
        x+=1        
    print('\033[0;0H%s\033[%d;0H'%('\n'.join([''.join(x) for x in _board0]),HEIGHT))
    if len(a):
        time.sleep(a[0])
def fill(sr,sc,er,ec,s):
    rect(sr,sc,[s*(ec-sc)]*(er-sr))
def get(row,col):
    return board[row*WIDTH+col]
def clear():
    global board
    board=[' ']*WIDTH*HEIGHT
    flush()
def screensize(h,w):
    global HEIGHT,WIDTH
    HEIGHT=h
    WIDTH=w
    clear()
def layer_id(name):
    return [i for i in range(len(cache)) if cache[i]['name']==name][0]
def new_layer(name,row,col,r):
    if name in [x['name'] for x in cache]:
        raise NameError("more layers use the same name '%s'"%name)
    cache.append({
        'name':name,
        'row' :row,
        'col' :col,
        'r'   :r
    })
    return name
def del_layer(name):
    cache.pop(check_layer(name))
def pos_layer(name,row,col):
    cache[layer_id(name)]['row']=row
    cache[layer_id(name)]['col']=col
def move_layer(name,row,col):
    cache[layer_id(name)]['row']+=row
    cache[layer_id(name)]['col']+=col
def clone_layer(oldname,newname):
    new=cache[check_layer(oldname)]
    new['name']=newname
    cache.append(new)
def setup():
    cls()
    flush()

if __name__=='__main__':
    for i in (0,16,32):
        for j in range(-6,12):
            rect(j,i+j-5,[
        	        '+--------+',
        	        '| L      |',
        	        '|   M    |',
        	        '|     F  |',
        	        '|       S|',
        	        '+--------+'
            ])
            flush(0.05)
    new_layer(0,10,10,[
        '          ',
        ' +------+ ',
        ' |layer0| ',
        ' +------+ ',
        '          '
    ])
    for i in range(10):
        move_layer(0,-1,2)
        flush(.02)
    for i in range(6):
        move_layer(0,1,0)
        flush(.02)
    import math
    for i in range(300):
        pos_layer(0,6+round(5*math.sin(i*math.pi/50)),20+round(10*math.cos(i*math.pi/50)))
        flush(0.001)
    line(0,0,'Program Finished')
    flush()
    input('Press enter key to exit')
