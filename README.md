Dimmer
======

Dimmer is a tool to control the brightness of the screen in GNU/Linux down to the lowest possible values — and even further. It uses `/sys/class/backlight` to dim as low as hardware allows and then makes the screen even darker decreasing `xrandr` brightness value.

The script outputs the brightness value in 0–100 range, which can be used to display brightness change pop-up, e. g. in KDE it can be done using D-Bus:
```
qdbus org.kde.plasmashell /org/kde/osdService org.kde.osdService.brightnessChanged $(sudo dimmer increase)
```

The script should be executed with root privileges. It can be easily done with `sudo` by creating the file in `/etc/sudoers.d/` containing a line like this:
```
your_user ALL=(ALL) NOPASSWD:/path/to/dimmer.py
```
