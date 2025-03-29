# Touchpaddraw

This is a simple python script that converts touchpad to graphics tablet

## Demo

[![demo yt video for touchpad draw](https://img.youtube.com/vi/jfI_lGY1dHM/0.jpg)](https://www.youtube.com/watch?v=jfI_lGY1dHM)

## how to use

clone this repo
```
git clone https://github.com/Vaisakhkm2625/touchpaddraw.git
```

Install these dependencies:
- `python3`
- `libevdev`
- `python3-evdev`
- `dotool`

```bash
python main.py
```

In case auto-selection of devices is not working,
you can use `-i` for interactive devices selection menu


also, there is a "toggle-script":
```bash
./toggle.sh
```

@MeexReay's sway config uses it like this:
```
bindsym $mod+Shift+g exec bash -c "cd $HOME/touchpaddraw && ./toggle.sh"

```
