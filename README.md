# Touchpaddraw

This is a simple python script that converts touchpad to graphics tablet...


## how to use

clone this repo
```
git clone https://github.com/Vaisakhkm2625/touchpaddraw.git
```
or
```
git clone git@github.com:Vaisakhkm2625/touchpaddraw.git
```

install `evtest`

Run `sudo evtest` and find the event of your touchpad

```
/dev/input/event8:	MSFT0001:01 06CB:CE2D Touchpad
```
means you have `event8`

install python packages
```
sudo pip install evdev 
sudo pip install pynput
```
TODO: (libevdev or evdev)

then run

```bash
sudo python main.py -d event8

```
accouding to your event number
