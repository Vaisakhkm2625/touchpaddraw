# ref: https://askubuntu.com/questions/1345561/how-can-i-get-absolute-touchpad-coordinates
#1224 804 -> 20 15

import math
import os
import time

#get trackpad absolute coords
from evdev import InputDevice
 
import argparse
 
from pynput import mouse
from pynput.mouse import Button
 
# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("-d", "--device", help = "device (event*)")
 
# Read arguments from command line
args = parser.parse_args()

#SET THIS TO YOUR DEVICE
device = InputDevice('/dev/input/'+ args.device if args.device else 'event7')

touchpad_x_max = 1224
touchpad_y_max = 804

max_x = 1920
max_y = 1080

x = 0
y = 0

def get_xy_coords(e):
    #you may need to change this number here; i don't know
    if e.code == 53:
        global x
        x = e.value
    #this one too
    if e.code == 54:
        global y
        y = e.value
        
def mapFromTo(x,a,b,c,d):
   # y=(x-a)//(b-a)*(d-c)+c
   y=(x-a)/(b-a)*(d-c)+c
   return y

x_pos =0
y_pos =0

mouse_controller = mouse.Controller()
for event in device.read_loop():
    #rows, cols = stdscr.getmaxyx()
    get_xy_coords(event)
    if event.code == 54:
        prev_x_pos = x_pos 
        prev_y_pos = y_pos 
        x_pos =math.floor(mapFromTo(x,0,touchpad_x_max,0,max_x))
        y_pos =math.floor(mapFromTo(y,0,touchpad_y_max,0,max_y))
        if (abs(prev_x_pos-x_pos)>15 or abs(prev_y_pos-y_pos)>15):
            mouse_controller.release(Button.left)
            mouse_controller.position = (x_pos,y_pos);
        mouse_controller.press(Button.left)
        mouse_controller.position = (x_pos,y_pos);

      #stdscr.addstr(math.floor(mapFromTo(y,0,touchpad_y_max,0,max_y)),math.floor(mapFromTo(x,0,touchpad_x_max,0,max_x)),char)

