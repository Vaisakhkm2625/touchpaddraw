# ref: https://askubuntu.com/questions/1345561/how-can-i-get-absolute-touchpad-coordinates
#1224 804 -> 20 15

import math
import os
import time

from evdev import InputDevice
 
import argparse
 
 
# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("-d", "--device", help = "device (event*)")
 
# Read arguments from command line
args = parser.parse_args()

#SET THIS TO YOUR DEVICE
if args.device:
    device = InputDevice('/dev/input/event6')

device = InputDevice('/dev/input/'+ args.device if args.device else 'event7')

# width =  80
# height =  30

width =  160
height =  60
x = 0
y = 0

mat = [ [' ']*width for i in range(height)]

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


def draw(mat):
    os.system('clear')
    for i in mat:
        for j in i:
            print(j, end='')
        print()
    # time.sleep(20)

for event in device.read_loop():
    get_xy_coords(event)

    if event.code == 54:
        mat[math.floor(mapFromTo(y,0,804,0,height-1))][math.floor(mapFromTo(x,0,1224,0,width-1))] = '#'
        # mat[mapFromTo(y,0,804,0,height-1)][mapFromTo(x,0,1224,0,width-1)] = '#'
        draw(mat)
