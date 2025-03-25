from evdev import InputDevice
import argparse
import os
import threading
import subprocess
import time
import math


def find_device(name):
    for f in os.listdir("/dev/input"):
        if f.startswith("event"):
            output = subprocess.check_output(["udevadm", "info", "-a", "/dev/input/"+f])
            if "ATTRS{name}==\""+name+"\"" in output.decode():
                return f
    return None


def start_thread(func, *args):
    threading.Thread(
        target = func,
        args = args,
        daemon = True
    ).start()


def send_actions(actions):
    os.system(b"echo \""+ (b"\n".join(actions)) +b"\" | dotoolc")

def get_move(x, y):
    return f"mouseto {x} {y}".encode()

def get_button_down():
    return b"buttondown left"

def get_button_up():
    return b"buttonup left"


def main():
    parser = argparse.ArgumentParser()
 
    parser.add_argument("-d", "--device")
    parser.add_argument("-W", "--touchpad-width")
    parser.add_argument("-H", "--touchpad-height")

    args = parser.parse_args()

    device_path = '/dev/input/' + (find_device(args.device) or "event7")

    max_tx = int(args.touchpad_width) or 1744
    max_ty = int(args.touchpad_height) or 1266


    device = InputDevice(device_path)
    device.grab()

    start_thread(lambda: os.system("dotoold") and exit())

    tx = None
    ty = None

    prev_x = None
    prev_y = None
    last_time = None

    for event in device.read_loop():
        if event.code == 53:
            tx = event.value
        elif event.code == 54:
            ty = event.value

            x = tx / max_tx
            y = ty / max_ty

            actions = [get_button_down(), get_move(x, y), get_button_up()]

            now = time.time()

            if last_time is not None:
                distance = math.sqrt(abs(x - prev_x) * max_tx + abs(y - prev_y) * max_ty)

                if distance > 15 and now - last_time > 0.1 or now - last_time > 0.5:
                    actions = [actions[1]]
                
            start_thread(send_actions, actions)

            prev_x = x
            prev_y = y
            last_time = now


if __name__ == "__main__":
    main()
