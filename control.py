'''
File calls the motors using keyboard events
@author Mbeleke Nguefack, Jan 2013
@license GPLv3 
'''
from Tkinter import *
import serial
import time

root = Tk()
start = chr(255)
H_position=0
V_position=0

MAX_V = 71;
MIN_V = 21;

def locate(d,p):
    global start
    ser = serial.Serial(
    port="COM2",
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
    );
    ser.close()
    ser.open()
    packet = ''.join([start, chr(d), chr(p)])
    ser.write(packet)
    ser.close()
    
def left_Key(event):
    global H_position
    H_position = H_position - 2
    locate(0,H_position)
    print 'Horizontal:', H_position
    
def right_Key(event):
    global H_position
    H_position = H_position + 2
    locate(0,H_position)
    print 'Horizontal:', H_position

def up_Key(event):
    global V_position
    global MAX_V

    if(V_position > MAX_V):
        return;
    
    V_position = V_position + 2
    locate(1,V_position)
    print 'Vertical:', V_position

def down_Key(event):
    global V_position
    global MIN_V

    if(V_position < MIN_V):
        return;
    V_position = V_position - 2
    locate(1,V_position)
    print 'Vertical:', V_position

V_position = MAX_V;
locate(0, 0);
locate(1, V_position);

frame = Frame(root, width=100, height=100)

frame.bind("<Left>", left_Key)
 
frame.bind("<Right>", right_Key)

frame.bind("<Up>", up_Key)
 
frame.bind("<Down>", down_Key)




frame.pack()

frame.focus_set()




root.mainloop()
