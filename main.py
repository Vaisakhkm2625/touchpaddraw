import evdev 
import argparse
import os
import threading
import subprocess
import time
import math
from dotoolc import send_actions


def list_devices(devices: list[evdev.InputDevice]):
    print("\n".join([f"{i}.{dev.name}" for i,dev in enumerate(devices)]))


def device_menu():

    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    list_devices(devices)

    default_device = find_device()

    try:
        inp = input(f"Select touchpad [0 - {len(devices)}] { f'(default:{default_device.name}): ' if default_device else '' }")

        if inp == '' and default_device :
            return default_device

        id = int(inp)
        if(0 > id or id > len(devices)):
            raise ValueError()

        return devices[id]

    except ValueError as e:
        print(f" Wrong input, kindly enter a number between 0 and {len(devices)}")
        return None


def find_device(name:str|None ="touchpad"):

    if(name == None):
        name = "touchpad"

    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

    for device in devices:
        if name.lower() in device.name.lower():
            return device

    return None

def is_touchpad(device):
    """Check if a given evdev device is a touchpad."""
    try:
        caps = device.capabilities()

        has_touch = evdev.ecodes.EV_ABS in caps and (
            evdev.ecodes.ABS_MT_POSITION_X in caps[evdev.ecodes.EV_ABS] or
            evdev.ecodes.ABS_MT_POSITION_Y in caps[evdev.ecodes.EV_ABS]
        )
        has_finger_tool = evdev.ecodes.EV_KEY in caps and evdev.ecodes.BTN_TOOL_FINGER in caps[evdev.ecodes.EV_KEY]

        return has_touch or has_finger_tool
    except Exception:
        return False



def start_thread(func, *args):
    threading.Thread(
        target = func,
        args = args,
        daemon = True
    ).start()


#def send_actions(actions):
#    os.system(b"echo \""+ (b"\n".join(actions)) +b"\" | dotoolc")

def get_move(x, y):
    return f"mouseto {x} {y}".encode()

def get_button_down():
    return b"buttondown left"

def get_button_up():
    return b"buttonup left"


def main():
    parser = argparse.ArgumentParser()
 
    parser.add_argument("-d", "--device")
    parser.add_argument("-i", "--interative",action="store_true")
    parser.add_argument("-W", "--touchpad-width")
    parser.add_argument("-H", "--touchpad-height")

    args = parser.parse_args()

    #device_path = '/dev/input/' + (find_device(args.device) or "event7")
    #device = evdev.InputDevice(device_path)


    device = find_device(args.device)

    if(args.interative):
        device = device_menu()


    if(not device):
        print("Error: Unable to find a device")
        return

    if(not is_touchpad(device)):
        print("Error: The device choosen doesn't have touchpad capabilities")
        return


    device.grab()

    max_touchpad_x = int(args.touchpad_width) if args.touchpad_width else device.absinfo(evdev.ecodes.ABS_X).max
    max_touchpad_y = int(args.touchpad_height) if args.touchpad_height else device.absinfo(evdev.ecodes.ABS_Y).max
    print(f"touchpad dimention : {max_touchpad_x=} {max_touchpad_y=}")

    start_thread(lambda: os.system("dotoold") and exit())

    touchpad_x = None
    touchpad_y = None

    prev_x = None
    prev_y = None
    last_time = None

    for event in device.read_loop():
        if event.code == 53:
            touchpad_x = event.value
        elif event.code == 54:
            touchpad_y = event.value

            x = touchpad_x / max_touchpad_x
            y = touchpad_y / max_touchpad_y

            actions = [get_button_down(), get_move(x, y), get_button_up()]

            now = time.time()

            if last_time is not None:
                #distance = math.sqrt(abs(x - prev_x) * max_touchpad_x + abs(y - prev_y) * max_touchpad_y)
                #print(f"{distance}=math.sqrt(abs({x} - {prev_x}) * {max_touchpad_x} + abs({y} - {prev_y}) * {max_touchpad_y})")

                distance = abs(x - prev_x)+ abs(y - prev_y) 

                if distance > 0.001  and now - last_time > 0.1 or now - last_time > 0.5:
                #if distance > 0.001:
                    actions = [actions[1]]
                
            start_thread(send_actions, actions)

            prev_x = x
            prev_y = y
            last_time = now


if __name__ == "__main__":
    main()
