#!/usr/bin/python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import sys
import math
import subprocess
from functools import reduce

DEVICE_NAME = 'intel_backlight'
SCREEN_NAME = 'eDP-1'
XRANDR_STEP = 0.1


def get_max_sys_brightness(device_name):
    with open('/sys/class/backlight/{}/max_brightness'.format(device_name)) as f:
        return int(f.read())


def get_sys_brightness(device_name):
    with open('/sys/class/backlight/{}/brightness'.format(device_name)) as f:
        return int(f.read())


def set_sys_brightness(device_name, brightness):
    with open('/sys/class/backlight/{}/brightness'.format(device_name), 'w') as f:
        f.write(str(int(brightness)))


def get_xrandr_brightness():
    xrandr = subprocess.check_output(['xrandr', '--verbose']).decode('utf-8')
    brightness_line = [line.strip() for line in xrandr.split('\n') if 'Brightness' in line][0]
    brightness = brightness_line.split(' ')[1]
    return float(brightness)


def set_xrandr_brightness(screen_name, brightness):
    subprocess.check_call(['xrandr', '--output', screen_name, '--brightness', str(brightness)])


def decrease_brightness(device_name, screen_name, step=5, minimal_brightness=1, minimal_step_percent=1):
    current = get_sys_brightness(device_name)
    maximal = get_max_sys_brightness(device_name)
    if current > minimal_brightness:
        decrement = current * 0.25
        min_decrement = minimal_step_percent / 100.0 * maximal
        if decrement < min_decrement:
            decrement = min_decrement
        target = max(current - decrement, minimal_brightness)
        set_sys_brightness(device_name, target)
        return target
    else:
        current_xrandr = get_xrandr_brightness()
        if current_xrandr > 0.25:
            target_xrandr = current_xrandr - XRANDR_STEP
            set_xrandr_brightness(screen_name, target_xrandr)
            return target_xrandr
        else:
            set_sys_brightness(device_name, 0)
            return 0


def increase_brightness(device_name, screen_name, step=5, minimal_brightness=1, minimal_step_percent=1):
    current = get_sys_brightness(device_name)
    maximal = get_max_sys_brightness(device_name)
    if current > minimal_brightness:
        increment = current / 3
        min_increment = minimal_step_percent / 100.0 * maximal
        if increment < min_increment:
            increment = min_increment
        target = min(current + increment, maximal)
        set_sys_brightness(device_name, target)
        return target
    elif current == 0:
        set_sys_brightness(device_name, minimal_brightness)
    else:
        current_xrandr = get_xrandr_brightness()
        if current_xrandr < 1:
            target_xrandr = min(current_xrandr + XRANDR_STEP, 1)
            set_xrandr_brightness(screen_name, min(current_xrandr + XRANDR_STEP, 1))
            return target_xrandr
        else:
            increment = current / 3
            min_increment = minimal_step_percent / 100.0 * maximal
            if increment < min_increment:
                increment = min_increment
            target = min(current + increment, maximal)
            set_sys_brightness(device_name, target)
            return target


if __name__ == '__main__':
    new_brightness = None
    if 'decrease' in sys.argv[1:]:
        new_brightness = decrease_brightness(DEVICE_NAME, SCREEN_NAME)
    elif 'increase' in sys.argv[1:]:
        new_brightness = increase_brightness(DEVICE_NAME, SCREEN_NAME)
    if new_brightness:
        if new_brightness <= 1:
            return_percent = new_brightness * 20
        else:
            max_brightness = get_max_sys_brightness(DEVICE_NAME)
            return_percent = math.sqrt(new_brightness) * 80 / math.sqrt(max_brightness) + 20
        print(int(return_percent))
