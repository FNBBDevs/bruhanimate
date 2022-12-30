import math
import time
import random
from abc import ABC, abstractmethod

_VALID_DIRECTIONS = ["right", "left"]

class BaseEffect:
    """
    Class for keeping track of an effect, and updataing it's buffer
    """
    def __init__(self, buffer, background):
        self.buffer            = buffer
        self.background        = background
        self.background_length = len(background)
    
    @abstractmethod
    def render_frame(self, frame_number):
        """
        To be defined by each effect
        """


class StaticEffect(BaseEffect):
    """
    Class for generating a static background.
    """
    def __init__(self, buffer, background):
        super(StaticEffect, self).__init__(buffer, background)
    
    def render_frame(self, frame_number):
        for y in range(self.buffer.height()):
            self.buffer.put_at(0, y, self.background * (self.buffer.width() // self.background_length + self.background_length))


class OffsetEffect(BaseEffect):
    """
    Class for generating an offset-static backgorund.
    :new-param direction: which way the offset should go.
    """
    def __init__(self, buffer, background, direction="right"):
        super(OffsetEffect, self).__init__(buffer, background)

        self.direction  = direction if direction in _VALID_DIRECTIONS else "right"
    
    def update_direction(self, direction):
        self.direction  = direction if direction in _VALID_DIRECTIONS else "right"

    def render_frame(self, frame_number):
        for y in range(self.buffer.height()):
            row = (self.background[y%self.background_length:] + self.background[:y%self.background_length]) * (self.buffer.width() // self.background_length + self.background_length)
            if self.direction == "right":
                self.buffer.put_at(0, y, row[::-1])
            else:
                self.buffer.put_at(0, y, row)


class NoiseEffect(BaseEffect):
    """
    Class for generating noise.
    :new-param intensity: randomness for the noise, higher the value the slower the effect (due to computation).
                          Will be a value 1 - 999
    """
    def __init__(self, buffer, background, intensity=200):
        super(NoiseEffect, self).__init__(buffer, background)

        self.intensity         = intensity / 1000 if intensity and 1 <= intensity <= 999 else 200 / 1000

        self.noise        = " !@#$%^&*()_+1234567890-=~`qazwsxedcrfvtgbyhnujmik,ol.p;/[']\QAZXSWEDCVFRTGBNHYUJM<KIOL>?:P{\"}|"
        self.noise_length = len(self.noise)

    def update_intensity(self, intensity):
        self.intensity = intensity / 1000 if intensity and 1 <= intensity <= 999 else 200 / 1000

    def render_frame(self, frame_number):
        for y in range(self.buffer.height()):
            self.buffer.put_at(0, y, ''.join([self.noise[random.randint(0, self.noise_length - 1)] if random.random() < self.intensity else self.buffer.get_char(_, y) for _ in range(self.buffer.width())]))


class StarEffect(NoiseEffect):
    """
    Class for rendering out a blinking star effect. This is just a Noise effect with a predefined intensity.
    Ideally the background would be ' ' for the best effect, but the choice is yours.
    """
    def __init__(self, buffer, background):
        super(StarEffect, self).__init__(buffer, background)

        self.stars        = f"{background*(100 // self.background_length)}.*+"
        self.start_length = len(self.stars)

    def update_background(self, background):
        self.background        = background
        self.background_length = len(background)
        self.stars             = f"{background*(100 // self.background_length)}.*+"
        self.start_length      = len(self.stars)

    def render_frame(self, frame_number):
        for y in range(self.buffer.height()):
            self.buffer.put_at(0, y, ''.join([self.stars[random.randint(0, self.start_length - 1)] if random.random() < self.intensity else self.buffer.get_char(_, y) for _ in range(self.buffer.width())]))


# TESTING
def run_n_frames(effect, n, s):
    for _ in range(n):
        time.sleep(s)
        effect.render_frame(_)
        for y in range(effect.buffer.height()):
            print("".join(effect.buffer.grab_slice(0, y, effect.buffer.width())))
        print()
