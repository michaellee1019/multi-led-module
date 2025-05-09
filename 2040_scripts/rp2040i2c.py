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
from adafruit_led_animation.sequence import AnimationSequence

from adafruit_led_animation.helper import PixelMap
from adafruit_neopxl8 import NeoPxl8

first_led_pin = board.NEOPIXEL0

class PixelStrand:
    # Animation settings
    speed: float = 0.1
    colors = [RED]
    tail_length: int = 10
    bounce: bool = False
    size: int = 1
    spacing: int = 1
    period: int = 1
    num_sparkles: int = 1
    step: int = 1
    animation_name = "comet"

    def __init__(self, strand) -> None:
        self.strand = strand
        self.active_animation = RainbowComet(
                self.strand,
                speed=self.speed,
                tail_length=self.tail_length,
                bounce=self.bounce,
            )

    def handle_command(self, params: dict) -> None:
        should_set_anim = True
        anim_name = self.animation_name
        for name, args in params.items():
            if name == "set_animation":
                self.strand.fill((0, 0, 0))
                self.strand.show()
                anim_name = args
            elif name == "speed":
                self.speed = float(args)
            elif name == "color":
                if type(args) is str:
                    color = self.get_color(args)
                    self.colors = [color]
                else:
                    self.colors = [(args[0], args[1], args[2])]
            elif name == "colors":
                self.colors = self.parse_colors(args)
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
            elif name == "num_sparkles":
                self.num_sparkles = int(args)
            elif name == "step":
                self.step = int(args)
            elif name == "set_pixel_colors":
                should_set_anim = False
                # clear active animation if we're explicitly setting pixel colors and zero all pixels if switching from animation to manual mode
                if self.active_animation is not None:
                    self.strand.fill((0, 0, 0))
                    self.strand.show()
                self.active_animation = None
                self.animation_name = ""
                self.set_pixel_colors(args)
            elif name == "sequence":
                should_set_anim = False
                self.handle_sequence(args)

            else:
                raise ValueError(f"invalid arg: {name}")
        if should_set_anim:
            self.set_animation(anim_name)
        self.strand.show()
    #TODO: refactor this to pass in all attributes as parameters
    # something like self.active_animation = handleAnimationName()
    # call this from handle sequence to make this easier, need to figure out
    # classy parsing.
    def set_animation(self, animation_name: str):
        print(f"animation name: {animation_name}")
        self.active_animation = self.handle_animation_name(
            animation_name,
            self.strand,
            self.speed,
            self.colors,
            self.tail_length,
            self.bounce,
            self.size,
            self.spacing,
            self.period,
            self.num_sparkles,
            self.step
        )
        self.animation_name = animation_name

    @classmethod
    def handle_animation_name(cls, animation_name, strand, speed, colors, tail_length,
                            bounce, size, spacing, period, num_sparkles, step):
        if animation_name == "blink":
            return Blink(strand, speed=speed, color=colors[0])
        elif animation_name == "colorcycle":
            return ColorCycle(strand, speed=speed, colors=colors)
        elif animation_name == "comet":
            return Comet(
                strand,
                speed=speed,
                color=colors[0],
                tail_length=tail_length,
                bounce=bounce,
            )
        elif animation_name == "chase":
            return Chase(
                strand,
                speed=speed,
                size=size,
                spacing=spacing,
                color=colors[0],
            )
        elif animation_name == "pulse":
            return Pulse(
                strand, speed=speed, period=period, color=colors[0]
            )
        elif animation_name == "sparkle":
            return Sparkle(
                strand,
                speed=speed,
                color=colors[0],
                num_sparkles=num_sparkles,
            )
        elif animation_name == "solid":
            return Solid(strand, color=colors[0])
        elif animation_name == "rainbow":
            return Rainbow(
                strand, speed=speed, period=period
            )
        elif animation_name == "sparkle_pulse":
            return SparklePulse(
                strand, speed=speed, period=period, color=colors[0]
            )
        elif animation_name == "rainbow_comet":
            return RainbowComet(
                strand,
                speed=speed,
                tail_length=tail_length,
                bounce=bounce,
            )
        elif animation_name == "rainbow_chase":
            return RainbowChase(
                strand,
                speed=speed,
                size=size,
                spacing=spacing,
                step=step,
            )
        elif animation_name == "rainbow_sparkle":
            return RainbowSparkle(
                strand, speed=speed, num_sparkles=num_sparkles
            )
        elif animation_name == "custom_color_chase":
            return CustomColorChase(
                strand,
                speed=speed,
                size=size,
                spacing=spacing,
                colors=colors,
            )
        else:
            raise ValueError("invalid animation name")

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

    def parse_colors(self, color_args):
        new_colors = []
        for color in color_args:
            if type(color) is str:
                new_colors.append(self.get_color(color))
            else:
                new_colors.append((color[0], color[1], color[2]))
        return new_colors

    def set_pixel_colors(self, pixel_colors: dict):
        for pixel, color in pixel_colors.items():
            # convert from floats to ints
            self.strand[int(pixel)] = [int(y) for y in color]
        self.strand.show()

    def get_active_animation(self) -> Animation:
        return self.active_animation

    def handle_sequence(self, sequence: dict):
        print("handling sequence")
        animations = []
        for animation in sequence.get("animations", []):
            animation_name = animation["set_animation"]
            speed = float(animation.get("speed", self.speed))
            tail_length = int(animation.get("tail_length", self.tail_length))
            bounce = int(animation.get("bounce", self.bounce))
            size = int(animation.get("size", self.size))
            spacing = int(animation.get("spacing", self.spacing))
            period = int(animation.get("period", self.period))
            num_sparkles = int(animation.get("num_sparkles", self.num_sparkles))
            step = int(animation.get("step", self.step))

            colors = animation.get("colors", [])
            if len(colors) == 0:
                colors = self.colors
            else:
                colors = self.parse_colors(colors)
            animations.append(self.handle_animation_name(animation_name, self.strand, speed, colors, tail_length, bounce, size, spacing, period, num_sparkles, step))

        sequence = AnimationSequence(*animations, advance_interval=float(sequence.get("duration", 0)), auto_clear=True)
        self.active_animation = sequence
        self.animation_name = "sequence"




class PixelDisplay:
    num_strands = 0
    strand_length = 0
    first_led_pin = board.NEOPIXEL0
    brightness = 0.0

    pixels = None
    strand_list = []
    has_active_animations = False

    animations: AnimationGroup = None

    def __init__(self, strands, brightness) -> None:
        self.reconfigure(strands, brightness)

    def reconfigure(self, strands:dict, brightness) -> None:
        longest_strand = 0
        for key in strands:
            print(f"key: {key}, value: {strands[key]}")
            self.num_strands = len(strands)
            if strands[key] > longest_strand:
                longest_strand = strands[key]
        self.strand_length = int(longest_strand)
        print("parsed strands")
        if brightness != 0.0:
            self.brightness = brightness
        if self.pixels is not None:
            self.pixels.deinit()
        self.pixels = NeoPxl8(
            first_led_pin,
            self.strand_length * self.num_strands,
            num_strands=self.num_strands,
            auto_write=False,
            brightness=self.brightness,
        )
        print("set pixels")
        strand_list = []
        # Sort the strands by their key (strand number)
        sorted_strands = sorted(strands.items(), key=lambda x: int(x[0]))
        for strand_num, length in sorted_strands:
            # Create a PixelMap for each strand with its specific length
            strand_map = PixelMap(
                self.pixels,
                range(int(strand_num) * int(length), int(strand_num) * int(length) + int(length)),
                individual_pixels=True,
            )
            strand_list.append(PixelStrand(strand_map))
        
        self.strand_list = strand_list
        print("set strand list")
        print(
            f"reconfigured with {self.num_strands} strands and brigthness of {self.brightness}"
        )
        self.regenerate_animation_group()

    def animate(self):
        if self.animations == None:
            self.regenerate_animation_group()
        # animation legnth of 0 is ok, means all pixels are manually setting values.
        if self.has_active_animations:
            self.animations.animate()

    def set_animation(self, strand_index: int, params: dict):
        if strand_index >= len(self.strand_list):
            raise ValueError("index out of bound for configured number of leds")
        self.strand_list[strand_index].handle_command(params)
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

NUM_FETCHES = 75

pixel_display = None

error_text = ""

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

                    # if error_text != "":
                    #     buffer = bytes(error_text.encode("utf-8"))
                    #     i2c_target_request.write(buffer)
                    # else:
                    #     temp = "success"
                    #     i2c_target_request.write(temp.encode("utf-8"))
                else:
                    # transaction is a write request
                    try:
                        full_msg = ""
                        for i in range(NUM_FETCHES):
                            time.sleep(0.001)
                            data = i2c_target_request.read(32)
                            # print(f"received data: {data}")
                            if len(data) > 0:
                                full_msg = full_msg + data.decode()
                        cleaned_msg = full_msg.replace("\x00", "")
                        command = {}
                        command = json.loads(cleaned_msg)
                        print(command)
                        if "reconfigure" in command:
                            sub_command = command["reconfigure"]
                            if pixel_display is not None:
                                pixel_display.reconfigure(
                                    sub_command["strands"],
                                    sub_command["brightness"],
                                )
                            else:
                                pixel_display = PixelDisplay(
                                    sub_command["strands"],
                                    sub_command["brightness"],
                                )
                        else:
                            for key in command:
                                pixel_display.set_animation(int(key), command[key])
                    except Exception as e:
                        print(e)
                        error_text = str(e)

        if pixel_display is not None:
            pixel_display.animate()
