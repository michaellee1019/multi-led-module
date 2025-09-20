# multi-led-module

## Board setup
NOTE: The latest version of circuit python has a [bug in it](https://github.com/adafruit/circuitpython/issues/10362) that makes it incompatible with this module. Please download version [9.2.4](https://adafruit-circuit-python.s3.amazonaws.com/bin/adafruit_feather_rp2040_scorpio/en_US/adafruit-circuitpython-adafruit_feather_rp2040_scorpio-en_US-9.2.4.uf2) for the time being.

The board must first be flashed by following adafruit's [install CircuitPython guide](https://learn.adafruit.com/introducing-feather-rp2040-scorpio/install-circuitpython).

Then, the board's lib folder must be populated with the CircuitPython Libraries. After the board is flashed with the `.uf2` file you will see that the   `lib` folder in the mounted drive is empty. Go to [Circuit Python's library page](https://circuitpython.org/libraries) and download the **Bundle for Version 9.x**. Expand the zip archive and copy the `lib` folder into the mounted `CIRCUITPY` drive. The transfer will take about 30 minutes. Detailed instructions are on the [Feather RP2040 SCORPIO tutorial](https://learn.adafruit.com/introducing-feather-rp2040-scorpio/circuitpython-libraries).

Once the board has been flashed with 9.2.7, replace the contents of the board's `code.py` with this repository's [rp2040i2c.py](https://github.com/vijayvuyyuru/multi-led-module/blob/main/2040_scripts/rp2040i2c.py) file.


