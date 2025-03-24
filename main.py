from evdev import InputDevice
import argparse
import os
import threading

parser = argparse.ArgumentParser()
 
parser.add_argument("-d", "--device", help = "device (event*)")
parser.add_argument("-W", "--touchpad-width")
parser.add_argument("-H", "--touchpad-height")

args = parser.parse_args()

device = InputDevice('/dev/input/' + (args.device or "event7"))

max_tx = args.touchpad_width or 1744
max_ty = args.touchpad_height or 1266

tx = None
ty = None

prev_sx = None
prev_sy = None

device.grab()

threading.Thread(
    target = lambda: os.system("dotoold"),
    daemon = True
).start()

def send_mouse(prev_x, prev_y, x, y):
    os.system(f"echo \"mouseto {x} {y}\" | dotoolc".encode())

def send_thread_mouse(*args):
    threading.Thread(
        target = send_mouse,
        args = args,
        daemon = True
    ).start()

for event in device.read_loop():
    if event.code == 53:
        tx = event.value
    if event.code == 54:
        ty = event.value

        sx = tx/max_tx
        sy = ty/max_ty
    
        send_thread_mouse(prev_sx, prev_sy, sx, sy)
