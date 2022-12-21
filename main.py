# ref: https://askubuntu.com/questions/1345561/how-can-i-get-absolute-touchpad-coordinates

from evdev import InputDevice
#SET THIS TO YOUR DEVICE
device = InputDevice('/dev/input/event17')

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
        

for event in device.read_loop():
    get_xy_coords(event)
    print(x, "  ",y)
