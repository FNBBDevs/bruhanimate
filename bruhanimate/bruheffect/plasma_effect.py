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

import math
import random

from bruhcolor import bruhcolored
from ..bruhutil import PLASMA_COLORS, GREY_SCALES, Buffer
from .base_effect import BaseEffect


class PlasmaEffect(BaseEffect):
    """
    Function to generate a plasma like effect
    """

    def __init__(self, buffer: Buffer, background: str):
        """
        Initializes the plasma effect class.

        Args:
            buffer (Buffer): Effect buffer to push updates to.
            background (str): Character or string to use as the background.
        """
        super(PlasmaEffect, self).__init__(buffer, background)
        self.info = False
        self.random = False
        self.scale = random.choice(GREY_SCALES)
        self.ayo = 0
        self.color = False
        self.vals = [
            random.randint(1, 100),
            random.randint(1, 100),
            random.randint(1, 100),
            random.randint(1, 100),
        ]

    def update_info_visibility(self, visible: bool):
        """
        Function to toggle visibility of info text.

        Args:
            visible (bool): Toggle visibility.
        """
        self.info = visible

    def update_grey_scale_size(self, size: int):
        """
        Function to change the size of the grey scale.

        Args:
            size (int): Size of the grey scale to use.

        Raises:
            Exception: If the requested grey scale size is not available.
        """
        if size in [8, 10, 16]:
            self.scale = random.choice(
                [scale for scale in GREY_SCALES if len(scale) == size]
            )
            if not self.random:
                self.colors = random.choice(PLASMA_COLORS[size])
            else:
                self.colors = [random.randint(0, 255) for _ in range(len(self.scale))]
        else:
            raise Exception(
                f"only 8, 10, and 16 are supported grey scale sizes, you provided {size}"
            )

    def update_color_properties(self, color: bool, characters: bool = True, random_color: bool = False):
        """
        Function to update the color properties. random_color overrules other functions.

        Args:
            color (bool): Toggle the use of colors.
            characters (bool, optional): Toggle the use of characters. Defaults to True.
            random_color (bool, optional): Toggle the use of random colors. Defaults to False.
        """
        self.color = color
        self.random = random_color
        if not random_color:
            self.colors = PLASMA_COLORS[len(self.scale)][0]
        else:
            self.colors = [random.randint(0, 255) for _ in range(len(self.scale))]
        self.characters = characters

    def update_color(self, colors: list[int]):
        """
        Function to update the color palette.

        Args:
            colors (list[int]): List of RGB values for the color palette.

        Raises:
            Exception: If the number of colors does not match the length of the scale.
        """
        if not self.random:
            if len(colors) == len(self.scale):
                self.colors = colors
            else:
                raise Exception(
                    f"update_color(..) must be provided a list of {len(self.scale)} colors, you provided {len(colors)}"
                )

    def update_background(self, background: str):
        """
        Function to update the background color or character.

        Args:
            background (str): Character or string to set the background to.
        """
        self.background = background
        self.background_length = len(self.background)

    def update_plasma_values(
        self,
        a: int = random.randint(1, 50),
        b: int = random.randint(1, 50),
        c: int = random.randint(1, 50),
        d: int = random.randint(1, 50),
    ):
        """
        Function to set the plasma values.

        Args:
            a (int, optional): Value a. Defaults to random.randint(1, 50).
            b (int, optional): Value b. Defaults to random.randint(1, 50).
            c (int, optional): Value c. Defaults to random.randint(1, 50).
            d (int, optional): Value d. Defaults to random.randint(1, 50).
        """
        self.vals = [a, b, c, d]

    def shuffle_plasma_values(self):
        """
        Function to shuffle the plasma values randomly.
        """
        self.vals = [
            random.randint(1, 50),
            random.randint(1, 50),
            random.randint(1, 50),
            random.randint(1, 50),
        ]

    def render_frame(self, frame_number: int):
        """
        Function to render the plasma effect frame by frame.

        Args:
            frame_number (int): The current frame number.
        """
        self.ayo += 1
        for y in range(self.buffer.height()):
            for x in range(self.buffer.width()):
                value = (
                    abs(
                        self.func(x + self.ayo / 3, y, 1 / 4, 1 / 3, self.vals[0])
                        + self.func(x, y, 1 / 8, 1 / 5, self.vals[1])
                        + self.func(x, y + self.ayo / 3, 1 / 2, 1 / 5, self.vals[2])
                        + self.func(x, y, 3 / 4, 4 / 5, self.vals[3])
                    )
                    / 4.0
                )
                if self.color:
                    if self.characters:
                        self.buffer.put_char(
                            x,
                            y,
                            bruhcolored(
                                self.scale[int((len(self.scale) - 1) * value)],
                                color=self.colors[int((len(self.scale) - 1) * value)],
                            ).colored,
                        )
                    else:
                        self.buffer.put_char(
                            x,
                            y,
                            bruhcolored(
                                " ",
                                on_color=self.colors[
                                    int((len(self.scale) - 1) * value)
                                ],
                            ).colored,
                        )
                else:
                    self.buffer.put_char(
                        x, y, self.scale[int((len(self.scale) - 1) * value)]
                    )
        if self.info:
            self.buffer.put_at(
                0, 0, f"COLORS: {' '.join([str(val) for val in self.colors])}"
            )
            for i in range(1, 5):
                self.buffer.put_at(0, i, f"VAL {i}: {str(self.vals[i-1]):>3s} ")

    def func(self, x: int, y: int, a: int, b: int, n: int):
        """
        Generates a plasma effect using the Perlin noise algorithm.

        Args:
            x (int): x
            y (int): y
            a (int): a
            b (int): b
            n (int): n

        Returns:
            float: value of the Perlin noise at (x, y)
        """
        return math.sin(
            math.sqrt(
                (x - self.buffer.width() * a) ** 2
                + 4 * ((y - self.buffer.height() * b)) ** 2
            )
            * math.pi
            / n
        )
