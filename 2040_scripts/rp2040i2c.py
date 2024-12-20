# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython I2C Device Address Scan"""
# If you run this and it seems to hang, try manually unlocking
# your I2C bus from the REPL with
#  >>> import board
#  >>> board.I2C().unlock()

import time
import board
from i2ctarget import I2CTarget
import json

# To use default I2C bus (most boards)
#i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# To create I2C bus on specific pins
#import busio
# i2c = busio.I2C(board.SCL1, board.SDA1)  # QT Py RP2040 STEMMA connector
#i2c = busio.I2C(board.GP1, board.GP0)    # Pi Pico RP2040

num_fetches = 10

with I2CTarget(board.SCL, board.SDA, (0x40,)) as device:
    while True:
        # check if there's a pending device request
        i2c_target_request = device.request()

        if not i2c_target_request:
            # no request is pending
            continue
        with i2c_target_request:
            address = i2c_target_request.address

            if i2c_target_request.is_read:
                print(f"read request to address '0x{address:02x}'")

                # for our emulated device, return a fixed value for the request
                buffer = bytes([0xaa])
                i2c_target_request.write(buffer)
            else:
                
                # transaction is a write request
                full_msg = ""
                for i in range(num_fetches):
                    
                    data = i2c_target_request.read(32)
                    print(f"received data: {data}")
                    if len(data) > 0:
                        full_msg = full_msg + data.decode()
                cleaned_msg = full_msg.replace('\x00', '')
                unserialized = json.loads(cleaned_msg)
                print(unserialized)
