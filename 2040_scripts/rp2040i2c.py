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

import rainbowio
import adafruit_ticks
from adafruit_led_animation.color import (
    AMBER,
    AQUA,
    BLACK,
    BLUE,
    GREEN,
    ORANGE,
    PINK,
    PURPLE,
    RED,
    WHITE,
    YELLOW,
    GOLD,
    JADE,
    MAGENTA,
    OLD_LACE,
    TEAL,
)
from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.customcolorchase import CustomColorChase

from adafruit_led_animation.helper import PixelMap
from adafruit_neopxl8 import NeoPxl8
import gc


class PixelStrand:
    # Animation settings
    speed: float = 0.1
    colors = [RED]
    tail_length: int = 1
    bounce: bool = False
    size: int = 1
    spacing: int = 1
    period: int = 1
    num_sparkles: int = 1
    step: int = 1

    def __init__(self, strand) -> None:
        self.strand = strand
        self.active_animation = "blink"
        self.regenerate_animations()

    def set_animation(self, params: dict) -> None:
        for name, args in params.items():
            if name == "set_animation":
                self.active_animation = args
                self.strand.fill((0, 0, 0))
                self.strand.show()
            elif name == "speed":
                self.speed = float(args)
            elif name == "color":
                color = self.get_color(args)
                self.colors = [color]
            elif name == "colors":
                new_colors = []
                for color in args:
                    new_colors.append(self.get_color(color))
                self.colors = new_colors
            elif name == "tail_length":
                self.tail_length = int(args)
            elif name == "bounce":
                self.bounce = int(args)
            elif name == "size":
                self.size = int(args)
            elif name == "spacing":
                self.spacing = int(args)
            elif name == "period":
                self.period = int(args)
            elif name == "speed":
                self.speed = int(args)
            elif name == "num_sparkles":
                self.num_sparkles = int(args)
            elif name == "step":
                self.step = int(args)
            elif name == "set_pixel_colors":
                # clear active animation if we're explicitly setting pixel colors and zero all pixels if switching from animation to manual mode
                if self.active_animation != "":
                    self.strand.fill((0, 0, 0))
                    self.strand.show()
                self.active_animation = ""
                self.set_pixel_colors(args)
            else:
                raise ValueError(f"invalid arg: {name}")
        self.regenerate_animations()

    def get_color(self, color: str) -> adafruit_led_animation.color:
        color_map = {
            "amber": AMBER,
            "aqua": AQUA,
            "black": BLACK,
            "blue": BLUE,
            "green": GREEN,
            "orange": ORANGE,
            "pink": PINK,
            "purple": PURPLE,
            "red": RED,
            "white": WHITE,
            "yellow": YELLOW,
            "gold": GOLD,
            "jade": JADE,
            "magenta": MAGENTA,
            "old_lace": OLD_LACE,
            "teal": TEAL,
        }
        strip_color = color_map.get(color.lower())
        if not strip_color:
            raise ValueError(f"invalid color name {color}")
        return strip_color

    def set_pixel_colors(self, pixel_colors: dict):
        for pixel, color in pixel_colors.items():
            # convert from floats to ints
            self.strand[int(pixel)] = [int(y) for y in color]
        self.strand.show()

    def regenerate_animations(self):
        self.blink = Blink(self.strand, speed=self.speed, color=self.colors[0])
        self.colorcycle = ColorCycle(self.strand, speed=self.speed, colors=self.colors)
        self.comet = Comet(
            self.strand,
            speed=self.speed,
            color=self.colors[0],
            tail_length=self.tail_length,
            bounce=self.bounce,
        )
        self.chase = Chase(
            self.strand,
            speed=self.speed,
            size=self.size,
            spacing=self.spacing,
            color=self.colors[0],
        )
        self.pulse = Pulse(
            self.strand, speed=self.speed, period=self.period, color=self.colors[0]
        )
        self.sparkle = Sparkle(
            self.strand,
            speed=self.speed,
            color=self.colors[0],
            num_sparkles=self.num_sparkles,
        )
        self.solid = Solid(self.strand, color=self.colors[0])
        self.rainbow = Rainbow(self.strand, speed=self.speed, period=self.period)
        self.sparkle_pulse = SparklePulse(
            self.strand, speed=self.speed, period=self.period, color=self.colors[0]
        )
        self.rainbow_comet = RainbowComet(
            self.strand,
            speed=self.speed,
            tail_length=self.tail_length,
            bounce=self.bounce,
        )
        self.rainbow_chase = RainbowChase(
            self.strand,
            speed=self.speed,
            size=self.size,
            spacing=self.spacing,
            step=self.step,
        )
        self.rainbow_sparkle = RainbowSparkle(
            self.strand, speed=self.speed, num_sparkles=self.num_sparkles
        )
        self.custom_color_chase = CustomColorChase(
            self.strand,
            speed=self.speed,
            size=self.size,
            spacing=self.spacing,
            colors=self.colors,
        )
        gc.collect()

    def get_animation(self, animation: str) -> Animation:
        animation_map = {
            "blink": self.blink,
            "colorcycle": self.colorcycle,
            "comet": self.comet,
            "chase": self.chase,
            "pulse": self.pulse,
            "sparkle": self.sparkle,
            "solid": self.solid,
            "rainbow": self.rainbow,
            "sparkle_pulse": self.sparkle_pulse,
            "rainbow_comet": self.rainbow_comet,
            "rainbow_chase": self.rainbow_chase,
            "rainbow_sparkle": self.rainbow_sparkle,
            "custom_color_chase": self.custom_color_chase,
        }
        animationl = animation_map.get(animation.lower())
        if not animationl:
            raise ValueError("invalid animation name")
        return animationl

    def get_active_animation(self) -> Animation:
        if self.active_animation != "":
            return self.get_animation(self.active_animation)


class PixelDisplay:
    num_strands = 0
    strand_length = 0
    first_led_pin = board.NEOPIXEL0
    brightness = 0.0

    pixels = None
    strand_list = []
    has_active_animations = False

    animations: AnimationGroup = None

    def __init__(self, num_strands, strand_length, brightness) -> None:
        self.reconfigure(num_strands, strand_length, brightness)

    def reconfigure(self, num_strands, strand_length, brightness) -> None:
        if num_strands != 0:
            self.num_strands = num_strands
        if strand_length != 0:
            self.strand_length = strand_length
        if brightness != 0.0:
            self.brightness = brightness
        if self.pixels is not None:
            self.pixels.deinit()
            del self.pixels
        for strand in self.strand_list:
            del strand
        self.pixels = NeoPxl8(
            self.first_led_pin,
            self.strand_length * self.num_strands,
            num_strands=self.num_strands,
            auto_write=False,
            brightness=self.brightness,
        )
        print("set pixels")
        strands = [self.strand(i, self.strand_length) for i in range(self.num_strands)]
        strands_list = []
        for strand in strands:
            strands_list.append(PixelStrand(strand))
        self.strand_list = strands_list
        print("set strand list")
        print(self.strand_list)
        print(
            f"reconfigured with {self.num_strands} strands, {self.strand_length} pixels per strand, and brigthness of {self.brightness}"
        )
        gc.collect()

    def animate(self):
        if self.animations == None:
            self.regenerate_animation_group()
        # animation legnth of 0 is ok, means all pixels are manually setting values.
        if self.has_active_animations:
            self.animations.animate()

    def set_animation(self, strand_index: int, params: dict):
        if strand_index >= len(self.strand_list):
            raise ValueError("index out of bound for configured number of leds")
        self.strand_list[strand_index].set_animation(params)
        self.regenerate_animation_group()

    def regenerate_animation_group(self):
        raw_anim = []
        for pxs in self.strand_list:
            a = pxs.get_active_animation()
            # active animation can be none if we manually set pixel colors
            if a is not None:
                raw_anim.append(a)
        if len(raw_anim) > 0:
            self.animations = AnimationGroup(*raw_anim)
            self.has_active_animations = True
        else:
            self.has_active_animations = False

    def strand(self, n, pixels_count):
        return PixelMap(
            self.pixels,
            range(n * pixels_count, (n + 1) * pixels_count),
            individual_pixels=True,
        )


NUM_FETCHES = 30

pixel_display = None

with I2CTarget(board.SCL, board.SDA, (0x40,)) as device:
    while True:
        # check if there's a pending device request
        i2c_target_request = device.request()

        if i2c_target_request:
            # no request is pending
            with i2c_target_request:
                address = i2c_target_request.address

                if i2c_target_request.is_read:
                    print(f"read request to address '0x{address:02x}'")

                    # for our emulated device, return a fixed value for the request
                    buffer = bytes([0xAA])
                    i2c_target_request.write(buffer)
                else:
                    # transaction is a write request
                    full_msg = ""
                    for i in range(NUM_FETCHES):
                        time.sleep(0.01)
                        data = i2c_target_request.read(32)
                        # print(f"received data: {data}")
                        if len(data) > 0:
                            full_msg = full_msg + data.decode()
                    cleaned_msg = full_msg.replace("\x00", "")
                    command = {}
                    try:
                        command = json.loads(cleaned_msg)
                    except:
                        print("invalid json received")
                        print(cleaned_msg)
                        continue
                    print(command)
                    if "reconfigure" in command:
                        sub_command = command["reconfigure"]
                        if pixel_display is not None:
                            pixel_display.reconfigure(
                                sub_command["num_strands"],
                                sub_command["strand_length"],
                                sub_command["brightness"],
                            )
                        else:
                            pixel_display = PixelDisplay(
                                sub_command["num_strands"],
                                sub_command["strand_length"],
                                sub_command["brightness"],
                            )
                    else:
                        for key in command:
                            pixel_display.set_animation(int(key), command[key])
        if pixel_display is not None:
            pixel_display.animate()
