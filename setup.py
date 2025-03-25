def check_evdev():
    try:
        import evdev
        return True
    except ImportError:
        return False

def check_libevdev():
    try:
        import ctypes
        ctypes.CDLL("libevdev.so.2")
        return True
    except OSError:
        return False

def check_dotool():
    import shutil
    return shutil.which("dotool") is not None

def main():
    if not check_evdev():
        print("evdev library is not found: install python3-evdev package")
        return

    if not check_libevdev():
        print("libevdev is not found: install libevdev")
        return

    if not check_dotool():
        print("dotool is not found: install dotool")
        return

    import re
    import os
    import subprocess

    devices = {}
    default_device = 1

    print("List of devices:")

    for f in os.listdir("/dev/input"):
        if f.startswith("event"):
            output = subprocess.check_output(["udevadm", "info", "-a", "/dev/input/"+f]).decode()

            pattern = r'ATTRS\{name\}=="(.*?)"'

            match = re.findall(pattern, output)[0]
            devices[f] = match

            if "touchpad" in match.lower():
                default_device = int(f.removeprefix("event"))

            print(f"/dev/input/{f} -> {match}")

    choosed_device = None

    while True:
        choosed_device = "event" + input(f"Enter touchpad event number (default: {default_device}): ")

        if choosed_device == "event":
            choosed_device += str(default_device)
            break

        if choosed_device in devices:
            break

    import evdev
    import threading

    device = evdev.InputDevice("/dev/input/" + choosed_device)
    device.grab()

    x, y = 0, 0
    stop = False

    def find_size():
        nonlocal x, y, stop
          
        print(f"\rPress on the corners to get touchpad size: {x}, {y}", end="")        

        for event in device.read_loop():
            if stop:
                break
            if event.code == 53:
                x = max(x, event.value)
            if event.code == 54:
                y = max(y, event.value)
              
                print(f"\rPress on the corners to get touchpad size: {x}, {y}", end="")        

    threading.Thread(target = find_size, daemon = True).start()

    input()

    stop = True

    print(f"\nHere is your touchpad size: {x}, {y}")

    with open("start.sh", "w") as f:
        f.write(f"python main.py -d \"{devices[choosed_device]}\" -W {x} -H {y}")
        f.close()

    os.system("chmod +x start.sh")

    print("Now, run the script with this command: \"./start.sh\"")

if __name__ == "__main__":
    main()
