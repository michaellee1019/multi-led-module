# multi-led-module

## Board setup
NOTE: The latest version of circuit python has a [bug in it](https://github.com/adafruit/circuitpython/issues/10362) that makes it incompatible with this module. Please download version [9.2.7](https://adafruit-circuit-python.s3.amazonaws.com/bin/adafruit_feather_rp2040_scorpio/en_US/adafruit-circuitpython-adafruit_feather_rp2040_scorpio-en_US-9.2.7.uf2) for the time being.

The board must first be flashed by following adafruit's [install CircuitPython guide](https://learn.adafruit.com/introducing-feather-rp2040-scorpio/install-circuitpython).

Once the board has been flashed with 9.2.7, replace the contents of the board's `code.py` with this repository's [rp2040i2c.py](https://github.com/vijayvuyyuru/multi-led-module/blob/main/2040_scripts/rp2040i2c.py) file.


