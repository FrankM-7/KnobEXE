# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import rotaryio
import board
import digitalio
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

button = digitalio.DigitalInOut(board.GP2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

encoder = rotaryio.IncrementalEncoder(board.GP0, board.GP1)

cc = ConsumerControl(usb_hid.devices)

button_state = None
last_position = encoder.position

kbd = Keyboard(usb_hid.devices)

while True:
    current_position = encoder.position
    position_change = current_position - last_position
    if position_change > 0:
        kbd.send(Keycode.SHIFT, Keycode.F8)
        print(current_position)
    elif position_change < 0:
        kbd.send(Keycode.SHIFT, Keycode.F7)
        print(current_position)
    last_position = current_position
    if not button.value and button_state is None:
        button_state = "pressed"
    if button.value and button_state == "pressed":
        print("Button pressed.")
        cc.send(ConsumerControlCode.PLAY_PAUSE)
        button_state = None
