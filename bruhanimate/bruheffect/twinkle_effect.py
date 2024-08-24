import random

from bruhcolor import bruhcolored
from ..bruhutil import TWINKLE_COLORS
from .base_effect import BaseEffect


class TWINKLE_SPEC:
    def __init__(self, char, value):
        self.char = char
        self.value = value
        self.fade = bruhcolored(self.char, TWINKLE_COLORS[self.value])
        self.mode = random.choice([1, -1])

    def __str__(self):
        return self.fade.colored

    def __repr__(self):
        return self.fade.colored

    def __len__(self):
        return 1

    def next(self):
        if self.value >= 23:
            self.mode = -1
        elif self.value <= 0:
            self.mode = 1

        self.value = self.value + self.mode

        self.fade = bruhcolored(self.char, TWINKLE_COLORS[self.value])
        return self

    def copy(self):
        new_TWINKLE_SPEC = TWINKLE_SPEC(self.char, self.value)
        new_TWINKLE_SPEC.mode = self.mode
        return new_TWINKLE_SPEC


class TwinkleEffect(BaseEffect):
    def __init__(self, buffer, background):
        super(TwinkleEffect, self).__init__(buffer, background)
        self.specs = []

    def render_frame(self, frame_number):
        if frame_number == 0:
            for y in range(self.buffer.height()):
                for x in range(self.buffer.width()):
                    if random.random() < 0.05:
                        new_TWINKLE_SPEC = TWINKLE_SPEC(".", random.randint(0, 23))
                        self.buffer.put_char(x, y, new_TWINKLE_SPEC)
                        self.specs.append((x, y))
        else:
            for x, y in self.specs:
                spec = self.buffer.get_char(x, y)
                self.buffer.put_char(x, y, spec.next().copy())
                del spec
