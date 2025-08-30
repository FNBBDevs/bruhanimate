"""
Copyright 2023 Ethan Christensen

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import random

from bruhcolor import bruhcolored
from ..bruhutil import TWINKLE_COLORS, Buffer
from .base_effect import BaseEffect


class TWINKLE_SPEC:
    """
    A class to represent a single twinkle character with its color value.
    """

    def __init__(self, char: chr, value: int):
        """
        Initializes the twinkle character with its color value.

        Args:
            char (chr): Character to display.
            value (int): Value assoicated with the color.
        """
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
        """
        Updates the twinkle character's color value and returns it as a string.
        """
        if self.value >= 23:
            self.mode = -1
        elif self.value <= 0:
            self.mode = 1

        self.value = self.value + self.mode

        self.fade = bruhcolored(self.char, TWINKLE_COLORS[self.value])
        return self

    def copy(self):
        """
        Returns a copy of the current twinkle character with its color value.

        Returns:
            TWINKLE_SPEC: Copy of the current twinkle spec.
        """
        new_TWINKLE_SPEC = TWINKLE_SPEC(self.char, self.value)
        new_TWINKLE_SPEC.mode = self.mode
        return new_TWINKLE_SPEC


class TwinkleEffect(BaseEffect):
    """
    Class for the twinkle effect.
    """

    def __init__(
        self, buffer: Buffer, background: str, twinkle_chars: list[str] = ["."]
    ):
        """
        Initializes the twinkle effect class.

        Args:
            buffer (Buffer): Effect buffer to push updates to.
            background (str): Character or string to use as the background.
        """
        super(TwinkleEffect, self).__init__(buffer, background)
        self.density = 0.05
        self.twinkle_chars = twinkle_chars
        self.specs = []
        self._set_specs()

    def set_density(self, density: float):
        """
        Sets the density of the twinkle effect, which determines how many characters will be affected by the effect.

        Args:
            density (float): Density value between 0 and 1, where 0 means no characters are affected and 1 means all characters are affected.
        """
        if isinstance(density, float) and 0 <= density <= 1:
            self.density = density
            self._set_specs()

    def set_twinkle_chars(self, twinkle_chars: list[str]):
        """
        Sets the characters to be used in the twinkle effect.

        Args:
            twinkle_chars (list[str]): List of characters to use for the twinkle effect.
        """
        if isinstance(twinkle_chars, list):
            self.twinkle_chars = twinkle_chars
            self._set_specs()
    
    def _set_specs(self):
        """
        Sets the specs for the twinkle effect.
        This method is called to initialize the specs for the twinkle effect.
        """
        self.specs = []
        self.buffer.clear_buffer()
        for y in range(self.buffer.height()):
            for x in range(self.buffer.width()):
                if random.random() < self.density:
                    new_TWINKLE_SPEC = TWINKLE_SPEC(
                        random.choice(self.twinkle_chars), random.randint(0, 23)
                    )
                    self.buffer.put_char(x, y, new_TWINKLE_SPEC)
                    self.specs.append((x, y))

    def render_frame(self, frame_number: int):
        """
        Renders the next frame of the twinkle effect to the buffer.

        Args:
            frame_number (int): The current frame of the animation.
        """
        for x, y in self.specs:
            spec = self.buffer.get_char(x, y)
            self.buffer.put_char(x, y, spec.next().copy())
            del spec
