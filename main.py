from evdev import InputDevice
import argparse
import os
import threading
import subprocess
import time


def find_device(name):
    for f in os.listdir("/dev/input"):
        if f.startswith("event"):
            output = subprocess.check_output(["udevadm", "info", "-a", "/dev/input/"+f])
            if "ATTRS{name}==\""+name+"\"" in output.decode():
                return f
    return None


def start_thread(func, *args):
    # func(*args)
    threading.Thread(
        target = func,
        args = args,
        daemon = True
    ).start()


def send_actions(actions):
    # os.system(b"echo \""+ (b"\n".join(actions)) +b"\" | dotoolc")
    for x in actions:
        os.system(b"echo \"" + x + b"\" | dotoolc")
        time.sleep(1 / 60)

def get_move(prev_x, prev_y, x, y):
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

    prev_sx = None
    prev_sy = None
    last_cl = None

    for event in device.read_loop():
        if event.code == 53:
            tx = event.value
        elif event.code == 54:
            ty = event.value

            sx = tx/max_tx
            sy = ty/max_ty

            press = prev_sx is None

            actions = []

            now = time.time()

            if prev_sx is not None and prev_sy is not None and last_cl is not None:
                if ((abs(sx - prev_sx) * max_tx) * (abs(sy - prev_sy) * max_ty) > 20 * 20 or \
                        now - last_cl > 0.5) and now - last_cl > 0.1:
                    actions.append(get_button_up())
                    press = True
    
            actions.append(get_move(prev_sx, prev_sy, sx, sy))

            if press:
                actions.append(get_button_down())

            start_thread(send_actions, actions)

            prev_sx = sx
            prev_sy = sy
            last_cl = now


if __name__ == "__main__":
    main()
