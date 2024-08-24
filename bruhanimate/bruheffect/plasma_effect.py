import math
import random

from bruhcolor import bruhcolored
from bruhutil import PLASMA_COLORS, GREY_SCALES
from bruheffect import BaseEffect


class PlasmaEffect(BaseEffect):
    """
    Function to generate a plasma like effect
    """

    def __init__(self, buffer, background):
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

    def update_info_visibility(self, visible):
        """
        Function to enable or disable info about the effect
        """
        self.info = visible

    def update_grey_scale_size(self, size):
        """
        Function to change the size of the grey scale
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

    def update_color_properties(self, color, characters=True, random_color=False):
        """
        Function to update the color properties. random_color overrules other functions
        like update greyscale size and update color
        :param color: True / False to enable color
        :param characters: True / False to show the characters
        :param random_color: True / False to generate random colors
        """
        self.color = color
        self.random = random_color
        if not random_color:
            self.colors = PLASMA_COLORS[len(self.scale)][0]
        else:
            self.colors = [random.randint(0, 255) for _ in range(len(self.scale))]
        self.characters = characters

    def update_color(self, colors):
        """
        Function to update the colors used
        """
        if not self.random:
            if len(colors) == len(self.scale):
                self.colors = colors
            else:
                raise Exception(
                    f"update_color(..) must be provided a list of {len(self.scale)} colors, you provided {len(colors)}"
                )

    def update_background(self, background):
        """
        Update the background character(s)
        :param background: the new background
        """
        self.background = background
        self.background_length = len(self.background)

    def update_plasma_values(
        self,
        a=random.randint(1, 50),
        b=random.randint(1, 50),
        c=random.randint(1, 50),
        d=random.randint(1, 50),
    ):
        """
        Function to set the plasma values
        """
        self.vals = [a, b, c, d]

    def shuffle_plasma_values(self):
        """
        Function to generate a new-random set of plasma values
        """
        self.vals = [
            random.randint(1, 50),
            random.randint(1, 50),
            random.randint(1, 50),
            random.randint(1, 50),
        ]

    def render_frame(self, frame_number):
        """
        Function to render the next frame of the Plasma Effect
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

    def func(self, x, y, a, b, n):
        """
        Helper function to calculate the plasma value given the four plasma values
        """
        return math.sin(
            math.sqrt(
                (x - self.buffer.width() * a) ** 2
                + 4 * ((y - self.buffer.height() * b)) ** 2
            )
            * math.pi
            / n
        )
