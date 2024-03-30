"""
Copyright 2023 Ethan Christensen
Line Drawing Copied, Guided, and Adapted from Asciimatics <https://github.com/peterbrittain/asciimatics/blob/master/asciimatics/screen.py>

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
import string
import random
import pyaudio
import numpy as np
from abc import abstractmethod
from bruhcolor import bruhcolored


_LIFE_COLORS = {
    "GREYSCALE": [232, 235, 239, 241, 244, 247, 248, 250, 254, 231],
    "GREYSCALE_r": [232, 235, 239, 241, 244, 247, 248, 250, 254, 231][::-1],
    "GREYSCALE_MUTED": [232, 235, 235, 239, 239, 241, 241, 244, 244, 231],
    "RAINBOW": [232, 202, 208, 190, 112, 27, 105, 129, 161, 231],
    "RAINBOW_r": [231, 196, 208, 190, 112, 27, 105, 129, 161, 201][::-1],
}

_LIFE_SCALES = {
    "default": " .:-=+*%#@",
    ".": " .........",
    "o": " ooooooooo",
    "0": " 000000000",
}

_PLASMA_COLORS = {
    2: [[232, 231]],
    8: [[150, 93, 11, 38, 181, 250, 143, 12], [142, 167, 216, 161, 59, 228, 148, 219]],
    10: [[232, 16, 53, 55, 89, 91, 126, 163, 197, 196][::-1]],
    16: [[232,16,53,55,56,89,90,91,125,126,163,199,198,197,196,39,81,231][::-1],
        [195, 106, 89, 176, 162, 180, 201, 233, 124, 252, 104, 181, 2, 182, 4, 170]],
}

_PLASMA_VALUES = [
    [43, 15, 8, 24],
    [15, 42, 47, 23],
    [35, 29, 31, 27],
    [10, 26, 19, 41]
]

_GRADIENTS = [
    [21, 57, 93, 129, 165, 201, 165, 129, 93, 57],
]

_VALID_DIRECTIONS = ["right", "left"]

_OLD_GREY_SCALES = [" .:;rsA23hHG#9&@"]

_GREY_SCALES = [" .,:ilwW", " .,:ilwW%@", " .:;rsA23hHG#9&@"]

_WIND_DIRECTIONS = ["east", "west", "none"]

_NOISE = "!@#$%^&*()_+1234567890-=~`qazwsxedcrfvtgbyhnujmik,ol.p;/[']\QAZXSWEDCVFRTGBNHYUJM<KIOL>?:P{\"}|"

_FLAKES = {1: "*", 3: "+", 7: "."}

_FLAKE_COLORS = {1: 253, 3: 69, 7: 31}

_FLAKE_JUMPS = {
    1: [1, 2, 3],
    3: [1, 2, 3],
    7: [1, 2],
}

_NEXT_FLAKE_MOVE = {
    ("center", "right"): 1,
    ("center", "left"): -1,
    ("left", "center"): 1,
    ("right", "center"): -1,
    ("right", "left"): None,  # not valid
    ("left", "right"): None,  # not valid
}

_FLAKE_WEIGHT_CHARS = {1: ",", 4: ";", 7: "*", 12: "@", 18: "#"}

_FLAKE_FLIPS = {
    1: ["*", "1"],
    3: ["+", "3"],
    7: [".", "7"],
}


class BaseEffect:
    """
    Class for keeping track of an effect, and updataing it's buffer
    """

    def __init__(self, buffer, background):
        self.buffer = buffer
        self.background = background
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
        """
        Renders the background to the screen
        """
        for y in range(self.buffer.height()):
            self.buffer.put_at(
                0,
                y,
                self.background
                * (
                    self.buffer.width() // self.background_length
                    + self.background_length
                ),
            )


class OffsetEffect(BaseEffect):
    """
    Class for generating an offset-static backgorund.
    :new-param direction: which way the offset should go.
    """

    def __init__(self, buffer, background, direction="right"):
        super(OffsetEffect, self).__init__(buffer, background)
        self.direction = direction if direction in _VALID_DIRECTIONS else "right"

    def update_direction(self, direction):
        """
        Function to update the direction of the offset
        :param direction: East / West
        """
        self.direction = direction if direction in _VALID_DIRECTIONS else "right"
        self.buffer.clear_buffer()

    def render_frame(self, frame_number):
        """
        Function to render the next frame of the Offset effect
        """
        for y in range(self.buffer.height()):
            row = (
                self.background[y % self.background_length :]
                + self.background[: y % self.background_length]
            ) * (self.buffer.width() // self.background_length + self.background_length)
            if self.direction == "right":
                self.buffer.put_at(0, y, row[::-1])
            else:
                self.buffer.put_at(0, y, row)


class NoiseEffect(BaseEffect):
    """
    Class for generating noise.
    :param intensity: randomness for the noise, higher the value the slower the effect (due to computation).
                      Will be a value 1 - 999
    :param color: whether or not ro color the noise
    """

    def __init__(self, buffer, background, intensity=200, color=False):
        super(NoiseEffect, self).__init__(buffer, background)

        self.intensity = (
            intensity / 1000 if intensity and 1 <= intensity <= 999 else 200 / 1000
        )

        self.noise = " !@#$%^&*()_+1234567890-=~`qazwsxedcrfvtgbyhnujmik,ol.p;/[']\QAZXSWEDCVFRTGBNHYUJM<KIOL>?:P{\"}|"
        self.noise_length = len(self.noise)
        self.color = color

    def update_intensity(self, intensity):
        """
        Function to update the intensity of the effect
        :param intensity: new intensity
        """
        self.intensity = (
            intensity / 1000 if intensity and 1 <= intensity <= 999 else 200 / 1000
        )

    def update_color(self, color, characters):
        """
        Function to enable / disable color for the effect
        :param color: True / False
        :param character: True / False to make characters visable
        """
        self.color = color
        self.characters = characters

    def render_frame(self, frame_number):
        """
        Function to render the next frame of the Noise effect
        """
        if self.color:
            for y in range(self.buffer.height()):
                for x in range(self.buffer.width()):
                    if random.random() < self.intensity:
                        if self.characters:
                            self.buffer.put_char(
                                x,
                                y,
                                bruhcolored(
                                    self.noise[
                                        random.randint(0, self.noise_length - 1)
                                    ],
                                    on_color=random.randint(0, 255),
                                ).colored,
                            )
                        else:
                            self.buffer.put_char(
                                x,
                                y,
                                bruhcolored(
                                    " ", on_color=random.randint(0, 255)
                                ).colored,
                            )
        else:
            for y in range(self.buffer.height()):
                for x in range(self.buffer.width()):
                    if random.random() < self.intensity:
                        self.buffer.put_char(
                            x, y, self.noise[random.randint(0, self.noise_length - 1)]
                        )


class StarEffect(NoiseEffect):
    """
    Class for rendering out a blinking star effect. This is just a Noise effect with a predefined intensity.
    Ideally the background would be ' ' for the best effect, but the choice is yours.
    """

    def __init__(self, buffer, background, color_type="GREYSCALE"):
        super(StarEffect, self).__init__(buffer, background)

        self.stars = f"{background*(100 // self.background_length)}.*+"
        self.stars_length = len(self.stars)
        self.color_type = color_type

    def update_color_type(self, color_type):
        """
        Function to update the color of the stars
        :param color_type: color map
        """
        self.color_type = color_type

    def update_background(self, background):
        """
        Function to update the background of the efffect
        :param background: the new background
        """
        self.background = background
        self.background_length = len(background)
        self.stars = f"{background*(100 // self.background_length)}.*+"
        self.stars_length = len(self.stars)

    def render_frame(self, frame_number):
        """
        Function to update the next frame of the Stars effect
        """
        for y in range(self.buffer.height()):
            for x in range(self.buffer.width()):
                if random.random() < self.intensity:
                    self.buffer.put_char(
                        x,
                        y,
                        bruhcolored(
                            self.stars[random.randint(0, self.stars_length - 1)],
                            color=_LIFE_COLORS[self.color_type][
                                random.randint(
                                    0, len(_LIFE_COLORS[self.color_type]) - 1
                                )
                            ],
                        ).colored,
                    )


class PlasmaEffect(BaseEffect):
    """
    Function to generate a plasma like effect
    """

    def __init__(self, buffer, background):
        super(PlasmaEffect, self).__init__(buffer, background)
        self.info = False
        self.random = False
        self.scale = random.choice(_GREY_SCALES)
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
                [scale for scale in _GREY_SCALES if len(scale) == size]
            )
            if not self.random:
                self.colors = random.choice(_PLASMA_COLORS[size])
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
            self.colors = _PLASMA_COLORS[len(self.scale)][0]
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


class GameOfLifeEffect(BaseEffect):
    """
    Effect ot simulate Conway's Game of Life
    """

    def __init__(
        self,
        buffer,
        background,
        decay=False,
        color=False,
        color_type=None,
        scale="random",
    ):
        super(GameOfLifeEffect, self).__init__(buffer, background)
        self.decay = decay
        self.scale = scale
        self.color = color
        self.color_type = color_type
        self._set_attributes()
        self.direcitons = [
            [1, 0],
            [0, 1],
            [-1, 0],
            [0, -1],
            [1, 1],
            [1, -1],
            [-1, 1],
            [-1, -1],
        ]
        self.rules = {"life": [2, 3], "death": [3, 3]}
        self.board = [
            [" " for _ in range(self.buffer.width())]
            for __ in range(self.buffer.height())
        ]

    def _set_attributes(self):
        """
        Function to set the attributes of the effect
        """
        self.grey_scale = (
            _LIFE_SCALES[random.choice(list(_LIFE_SCALES.keys()))]
            if self.decay and self.scale == "random"
            else _LIFE_SCALES[self.scale]
            if self.decay
            else " o"
        )
        self.colors = [232, 231] if not self.decay else _LIFE_COLORS[self.color_type]
        self.ALIVE = len(self.grey_scale) - 1
        self.DEAD = 0
        self.mappings = {i: self.grey_scale[i] for i in range(len(self.grey_scale))}

    def update_decay(self, decay, color_type="GREYSCALE", scale="random"):
        """
        Function to enable to decay and select the color map
        :param decay: True / False
        :param color_type: color map for the effect
        """
        self.decay = decay
        self.scale = scale
        if color_type:
            self.color_type = color_type
        self._set_attributes()

    def update_rules(self, life_rule, death_rule):
        self.rules["life"] = life_rule
        self.rules["death"] = death_rule

    def render_frame(self, frame_number):
        """
        Function to render the next frame of the GOL effect
        """
        if frame_number == 0:  # INITIALIZE THE GAME
            for y in range(self.buffer.height()):
                for x in range(self.buffer.width()):
                    if random.random() < 0.1:
                        self.buffer.put_char(
                            x,
                            y,
                            bruhcolored(
                                self.grey_scale[self.ALIVE],
                                color=self.colors[self.ALIVE],
                            ).colored,
                        )
                        self.board[y][x] = (
                            bruhcolored(
                                self.grey_scale[self.ALIVE],
                                color=self.colors[self.ALIVE],
                            ),
                            self.ALIVE,
                        )
                    else:
                        self.buffer.put_char(
                            x,
                            y,
                            bruhcolored(
                                self.grey_scale[self.DEAD], color=self.colors[self.DEAD]
                            ).colored,
                        )
                        self.board[y][x] = (
                            bruhcolored(
                                self.grey_scale[self.DEAD], color=self.colors[self.DEAD]
                            ),
                            0,
                        )
        else:  # RUN THE GAME
            all_neighbors = [
                [0 for _ in range(self.buffer.width())]
                for __ in range(self.buffer.height())
            ]
            for y in range(len(all_neighbors)):
                for x in range(len(all_neighbors[y])):
                    neighbors = 0
                    for direction in self.direcitons:
                        if (
                            0 <= y + direction[0] < self.buffer.height()
                            and 0 <= x + direction[1] < self.buffer.width()
                            and self.board[y + direction[0]][x + direction[1]][1]
                            == self.ALIVE
                        ):
                            neighbors += 1
                    all_neighbors[y][x] = neighbors
            for y in range(self.buffer.height()):
                for x in range(self.buffer.width()):
                    if self.board[y][x][1] == self.ALIVE:  # ALIVE
                        if (
                            self.rules["life"][0]
                            <= all_neighbors[y][x]
                            <= self.rules["life"][1]
                        ):  # STAY ALIVE
                            pass
                        else:  # MOVE TO THE FIRST DECAY STAGE
                            self.buffer.put_char(
                                x,
                                y,
                                bruhcolored(
                                    self.grey_scale[self.ALIVE - 1],
                                    color=self.colors[self.ALIVE - 1],
                                ).colored,
                            )
                            self.board[y][x] = (
                                bruhcolored(
                                    self.grey_scale[self.ALIVE - 1],
                                    color=self.colors[self.ALIVE - 1],
                                ),
                                self.ALIVE - 1,
                            )
                    else:  # DEAD
                        if (
                            self.rules["death"][0]
                            <= all_neighbors[y][x]
                            <= self.rules["death"][1]
                        ):  # COME BACK TO LIFE
                            self.buffer.put_char(
                                x,
                                y,
                                bruhcolored(
                                    self.grey_scale[self.ALIVE],
                                    color=self.colors[self.ALIVE],
                                ).colored,
                            )
                            self.board[y][x] = (
                                bruhcolored(
                                    self.grey_scale[self.ALIVE],
                                    color=self.colors[self.ALIVE],
                                ),
                                self.ALIVE,
                            )
                        else:  # MOVE TO THE NEXT STAGE --> IF AT 0 STAY AT 0 i.e. don't decrement
                            current_greyscale_position = self.board[y][x][1]
                            current_greyscale_position = (
                                current_greyscale_position - 1
                                if current_greyscale_position > 0
                                else 0
                            )
                            self.buffer.put_char(
                                x,
                                y,
                                bruhcolored(
                                    self.grey_scale[current_greyscale_position],
                                    color=self.colors[current_greyscale_position],
                                ).colored,
                            )
                            self.board[y][x] = (
                                bruhcolored(
                                    self.grey_scale[current_greyscale_position],
                                    color=self.colors[current_greyscale_position],
                                ),
                                current_greyscale_position,
                            )


class RainEffect(BaseEffect):
    """
    Effect to emmulate the look of rain
    """

    def __init__(
        self,
        buffer,
        background,
        img_start_x=None,
        img_start_y=None,
        img_width=None,
        img_height=None,
        collision=False,
        intensity=1,
        swells=False,
        wind_direction="none",
    ):
        super(RainEffect, self).__init__(buffer, background)

        self.image_present = (
            True if img_start_x and img_start_y and img_width and img_height else False
        )
        self.collision = collision
        self.intensity = intensity
        self.swells = swells
        self.swell_direction = 1
        self.multiplier = 1
        self.wind_direction = (
            wind_direction if wind_direction in _WIND_DIRECTIONS else "none"
        )
        self.wind_mappings = {
            "east": [".\\", -1, ["\\", "."]],
            "none": [".|", 0, ["|", "."]],
            "west": ["./", 1, ["/", "."]],
        }
        self._set_rain()

    def update_multiplier(self, val):
        """
        Update the multiplier value that relates to shift amount
        :param val: value to set the multiplier to
        """
        self.multiplier = val

    def update_wind_direction(self, direction):
        """
        Update the direction of the rain
        :param dircetion: direction for the rain to fall (east, west, none)
        """
        if direction in _WIND_DIRECTIONS:
            self.wind_direction = direction
            self._set_rain()

    def _set_rain(self):
        """
        Function set the rain based on the intensity and wind direction
        """
        self.rain = f"{' ' * (1000 - self.intensity)}"
        if self.intensity > 50:
            self.rain += "."
        if self.intensity > 250:
            self.rain += "."
        if self.intensity > 500:
            self.rain += self.wind_mappings[self.wind_direction][0]
        self.rain_length = len(self.rain)

    def update_intensity(self, intensity):
        """
        Function to update the intensity of the rain
        :param intensity: intentisy value
        """
        if self.swells:
            if self.intensity == 900:
                self.swell_direction = -1
            if self.intensity == 0:
                self.swell_direction = 1
            self.intensity += self.swell_direction
        else:
            self.intensity = intensity if intensity < 1000 else 999
        self._set_rain()

    def update_collision(
        self,
        img_start_x,
        img_start_y,
        img_width,
        img_height,
        collision,
        smart_transparent=False,
        image_buffer=None,
    ):
        """
        Function to set whether or not to visually see the rain collide with the ground
        or images if they are present
        :param img_start_x: where the image starts on the screen
        :param img_start_y: where the image starts on the screen
        :param img_width:   the width of the image
        :param img_height:  the height of the image
        :param collision:   update collision variable
        :param smart_transparent: update smart_transparent
        :param image_buffer: the buffer that contains the image
        """
        self.image_present = (
            True if img_start_x and img_start_y and img_width and img_height else False
        )
        self.collision = collision
        if self.image_present:
            self.img_start_x = img_start_x
            self.img_start_y = img_start_y
            self.img_height = img_height
            self.img_width = img_width
            self.smart_transparent = smart_transparent
            self.image_buffer = image_buffer
        else:
            self.image_buffer = None

    def update_swells(self, swells):
        """
        Function to set whether the intensity should evolve on it's own
        :param swells: True / False
        """
        self.swells = swells

    def render_frame(self, frame_number):
        """
        Function to render the next frame of the Rain Effect
        """
        if self.swells:
            self.update_intensity(None)
        if frame_number == 0:
            self.buffer.put_at(
                0,
                0,
                "".join(
                    [
                        self.rain[random.randint(0, self.rain_length - 1)]
                        for _ in range(self.buffer.width())
                    ]
                ),
            )
        else:
            self.buffer.shift(
                self.wind_mappings[self.wind_direction][1] * self.multiplier
            )
            self.buffer.scroll(-1 * self.multiplier)
            self.buffer.put_at(
                0,
                0,
                "".join(
                    [
                        self.rain[random.randint(0, self.rain_length - 1)]
                        for _ in range(self.buffer.width())
                    ]
                ),
            )

            if self.collision:
                for y in range(self.buffer.height()):
                    for x in range(self.buffer.width()):
                        # Wipe prior frames impact
                        if self.buffer.get_char(x, y) == "v":
                            self.buffer.put_char(x, y, " ")
                        else:
                            if self.image_present:
                                # if we are inscope of the image we need to process impacts
                                if self.image_buffer:
                                    if 0 <= y + 1 < self.buffer.height():
                                        if (
                                            not self.image_buffer.buffer[y + 1][x]
                                            in [" ", None]
                                            and self.buffer.get_char(x, y)
                                            in self.wind_mappings[self.wind_direction][
                                                2
                                            ]
                                        ):
                                            self.buffer.put_char(x, y, "v")

                            # impacting the bottom
                            if y == self.buffer.height() - 1:
                                if (
                                    self.buffer.get_char(x, y)
                                    in self.wind_mappings[self.wind_direction][2]
                                ):
                                    self.buffer.put_char(x, y, "v")


class MatrixEffect(BaseEffect):
    """
    Effect to mimic the cliche coding backgroud with falling random characters
    """

    def __init__(self, buffer, background, chracter_halt_range = (1, 2), color_halt_range = (1, 2), character_randomness_one = 0.70, character_randomness_two = 0.60, color_randomness = 0.50, gradient_length = 1):
        super(MatrixEffect, self).__init__(buffer, background)
        self.__character_choices = string.ascii_letters + "1234567890!@#$%^&*()_+-=<>,.:\";'{}[]?/"
        self.__character_halt_range = chracter_halt_range
        self.__color_halt_range = color_halt_range
        self.__character_halts = [random.randint(self.__character_halt_range[0], self.__character_halt_range[1]) for _ in range(self.buffer.height())]
        self.__color_halts = [random.randint(self.__color_halt_range[0], self.__color_halt_range[1]) for _ in range(self.buffer.height())]
        self.__character_randomness_one = character_randomness_one
        self.__character_randomness_two = character_randomness_two
        self.__color_randomness = color_randomness
        self.__gradient_length = gradient_length
        self.__base_gradient = [232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]
        self.__gradient = [color for color in self.__base_gradient for _ in range(self.__gradient_length)]
        self.__character_frame_numbers = [0 for _ in range(self.buffer.height())]
        self.__color_frame_numbers = [0 for _ in range(self.buffer.height())]
        self.__buffer_characters = [[" " for x in range(self.buffer.width())] for y in range(self.buffer.height())]
    
    def set_matrix_properties(self, chacter_halt_range = (1, 2), color_halt_range = (1, 2), character_randomness_one = 0.70, character_randomness_two = 0.60, color_randomness = 0.50, gradient_length = 1):
        self.__character_randomness_one = character_randomness_one
        self.__character_randomness_two = character_randomness_two
        self.__color_randomness = color_randomness
        self.__character_halt_range = chacter_halt_range
        self.__color_halt_range = color_halt_range
        self.__gradient_length = gradient_length
        self.__gradient = [color for color in self.__base_gradient for _ in range(self.__gradient_length)]
        self.__character_halts = [random.randint(self.__character_halt_range[0], self.__character_halt_range[1]) for _ in range(self.buffer.height())]
        self.__color_halts = [random.randint(self.__color_halt_range[0], self.__color_halt_range[1]) for _ in range(self.buffer.height())]
        
        
    def set_matrix_gradient(self, gradient):
        self.__base_gradient = gradient
        self.__gradient = [color for color in self.__base_gradient for _ in range(self.__gradient_length)]
    
    def get_gradient(self):
        return self.__base_gradient
    
    def __initialize_buffer(self):
        for y in range(self.buffer.height()):
            for x in range(self.buffer.width()):
                self.__buffer_characters[y][x] = random.choice(self.__character_choices)
            for x in range(self.buffer.width()):
                self.buffer.put_char(x, y, bruhcolored(self.__buffer_characters[y][x], self.__gradient[x % len(self.__gradient)]).colored)
        
    def render_frame(self, frame_number):
        """
        Renders the next frame for the Matrix effect into the effect buffer
        """
        if frame_number == 0:
            self.__initialize_buffer()
        else:
            for y in range(self.buffer.height()):
                if frame_number % self.__character_halts[y] == 0 and random.random() < self.__character_randomness_one:
                    self.__character_frame_numbers[y] += 1
                    for x in range(self.buffer.width()):
                        if random.random() < self.__character_randomness_two:
                            self.__buffer_characters[y][x] = random.choice(self.__character_choices)
                
                if frame_number % self.__color_halts[y] == 0 and random.random() < self.__color_randomness:
                    self.__color_frame_numbers[y] += 1
                    for x in range(self.buffer.width()):
                        self.buffer.put_char(x, y, bruhcolored(self.__buffer_characters[y][x], color=self.__gradient[(x - self.__color_frame_numbers[y]) % len(self.__gradient)]))
                        

class Line:
    def __init__(self, start_point, end_point):
        if start_point and end_point:
            self.start_point = (start_point[0] * 2, start_point[1] * 2)
            self.end_point = (end_point[0] * 2, end_point[1] * 2)
        else:
            self.start_point = None
            self.end_point = None

    def update_points(self, start_point, end_point):
        self.start_point = (start_point[0], start_point[1])
        self.end_point = (end_point[0], end_point[1])

    def get_points(self):
        return self.start_point, self.end_point


class DrawLines(BaseEffect):
    def __init__(self, buffer, background, char=None, thin=False):
        super(DrawLines, self).__init__(buffer, background)
        self.lines = []
        self.char = char
        self.thin = thin

    def add_line(self, start_point, end_point):
        self.lines.append(Line(start_point, end_point))

    def render_frame(self, frame_number):
        if frame_number == 0 and len(self.lines) > 0:
            for y in range(self.buffer.height()):
                self.buffer.put_at(0, y, self.background * self.buffer.width())
            for line in self.lines:
                if (
                    (line.start_point[0] < 0 and line.end_point[0]) < 0
                    or (
                        line.start_point[0] >= self.buffer.width() * 2
                        and line.end_point[0] > self.buffer.width() * 2
                    )
                    or (line.start_point[1] < 0 and line.end_point[1] < 0)
                    or (
                        line.start_point[1] >= self.buffer.height() * 2
                        and line.end_point[1] >= self.buffer.height() * 2
                    )
                ):
                    return

                line_chars = " ''^.|/7.\\|Ywbd#"
                dx = abs(line.end_point[0] - line.start_point[0])
                dy = abs(line.end_point[1] - line.start_point[1])

                cx = -1 if line.start_point[0] > line.end_point[0] else 1
                cy = -1 if line.start_point[1] > line.end_point[1] else 1

                def get_start(x, y):
                    c = self.buffer.get_char(x, y)
                    if c is not None:
                        return line_chars.find(c)
                    return 0

                def x_draw(ix, iy):
                    err = dx
                    px = ix - 2
                    py = iy - 2
                    next_char = 0
                    while ix != line.end_point[0]:
                        if ix < px or ix - px >= 2 or iy < py or iy - py >= 2:
                            px = ix & ~1
                            py = iy & ~1
                            next_char = get_start(px // 2, py // 2)
                        next_char |= 2 ** abs(ix % 2) * 4 ** (iy % 2)
                        err -= 2 * dy
                        if err < 0:
                            iy += cy
                            err += 2 * dx
                        ix += cx

                        if self.char is None:
                            self.buffer.put_char(
                                px // 2, py // 2, line_chars[next_char]
                            )
                        else:
                            self.buffer.put_char(px // 2, py // 2, self.char)

                def y_draw(ix, iy):
                    err = dy
                    px = ix - 2
                    py = iy - 2
                    next_char = 0

                    while iy != line.end_point[1]:
                        if ix < px or ix - px >= 2 or iy < py or iy - py >= 2:
                            px = ix & ~1
                            py = iy & ~1
                            next_char = get_start(px // 2, py // 2)
                        next_char |= 2 ** abs(ix % 2) * 4 ** (iy % 2)
                        err -= 2 * dx
                        if err < 0:
                            ix += cx
                            err += 2 * dy
                        iy += cy

                        if self.char is None:
                            self.buffer.put_char(
                                px // 2, py // 2, line_chars[next_char]
                            )
                        else:
                            self.buffer.put_char(px // 2, py // 2, self.char)

                if dy == 0 and self.thin and self.char is None:
                    pass
                elif dx > dy:
                    x_draw(line.start_point[0], line.start_point[1] + 1)
                else:
                    y_draw(line.start_point[0] + 1, line.start_point[1])


class _FLAKE:
    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.weight = 1
        self.color = _FLAKE_COLORS[index]
        self.char = bruhcolored(_FLAKES[index], color=self.color).colored
        self.current_position = "center"
        self.on_ground = False
        self.full = False

    def flip_flake(self):
        if self.char == _FLAKE_FLIPS[self.index][0]:
            self.char = _FLAKE_FLIPS[self.index][1]
        else:
            self.char = _FLAKE_FLIPS[self.index][0]

    def next_position(self, frame_number):
        if self.on_ground:
            return

        if frame_number % self.index != 0:
            return

        if random.random() < 0.10:
            return

        self.prev_x = self.x
        self.prev_y = self.y

        self.y = self.y + random.choice(_FLAKE_JUMPS[self.index])

        next_position = random.choice(["left", "center", "right"])

        next_flake_move = (
            _NEXT_FLAKE_MOVE[(self.current_position, next_position)]
            if self.current_position != next_position
            else None
        )

        if next_flake_move:
            self.x = self.x + next_flake_move
            self.current_position = next_position

    def update_position(self, x, y):
        self.prev_x = self.x
        self.prev_y = self.y
        self.x = x
        self.y = y

    def set_to_on_ground(self):
        self.weight = 1
        self.on_ground = True
        self.color = 190 if random.random() < 0.01 else 255
        self.char = bruhcolored(
            _FLAKE_WEIGHT_CHARS[self.weight], color=self.color
        ).colored

    def increment_flake_weight(self):
        if self.weight < 18:
            self.weight += 1
            
        self.update_ground_flake()
        
        if self.weight == 18:
            self.full = True

    def update_ground_flake(self):
        if not self.full:
            if self.char != list(_FLAKE_WEIGHT_CHARS.values())[-1]:
                if self.weight in _FLAKE_WEIGHT_CHARS.keys():
                    self.char = bruhcolored(
                        _FLAKE_WEIGHT_CHARS[self.weight], color=self.color
                    ).colored

    def __str__(self):
        return self.char

    def __repr__(self):
        return self.char

    def __len__(self):
        return 1

    def __eq__(self, other):
        return self.char == other

    def copy(self):
        new_flake = _FLAKE(index=self.index, x=self.x, y=self.y)
        new_flake.weight = self.weight
        new_flake.char = self.char
        new_flake.current_position = self.current_position
        new_flake.color = self.color
        new_flake.on_ground = self.on_ground
        new_flake.x = self.x
        new_flake.y = self.y
        new_flake.prev_x = self.prev_x
        new_flake.prev_y = self.prev_y
        new_flake.full = self.full
        return new_flake


class SnowEffect(BaseEffect):
    def __init__(
        self,
        buffer,
        background,
        img_start_x=None,
        img_start_y=None,
        img_width=None,
        img_height=None,
        collision=False,
        show_info=False,
    ):
        super(SnowEffect, self).__init__(buffer, background)
        self.image_present = (
            True if img_start_x and img_start_y and img_width and img_height else False
        )
        self.collision = collision
        self.total_ground_flakes = 0
        self._show_info = show_info
        self._flakes = []
        self._ground_flakes = [[None for _ in range(self.buffer.width())] for __ in range(self.buffer.height())]
        self._image_collide_flakes = [None for _ in range(self.buffer.width())]

    def update_collision(
        self,
        img_start_x,
        img_start_y,
        img_width,
        img_height,
        collision,
        image_buffer=None,
    ):
        """
        Function to set whether or not to visually see the snow collide with the ground
        or images if they are present
        :param img_start_x: where the image starts on the screen
        :param img_start_y: where the image starts on the screen
        :param img_width:   the width of the image
        :param img_height:  the height of the image
        :param collision:   update collision variable
        """
        self.image_present = (
            True if img_start_x and img_start_y and img_width and img_height else False
        )
        self.collision = collision
        if self.image_present:
            self.img_start_x = img_start_x
            self.img_start_y = img_start_y
            self.img_height = img_height
            self.img_width = img_width
            self.img_end_y = img_start_y + img_height
            self.image_buffer = image_buffer
            self.image_x_boundaries = (img_start_x, img_start_x + img_width)
            self.image_y_boundaries = (img_start_y, img_start_y + img_height)
        else:
            self.image_buffer = None
        
    def show_info(self, show_info: bool):
        self._show_info = show_info

    def render_frame(self, frame_number):
        # calc each flakes next position
        for flake in self._flakes:
            flake.next_position(frame_number)

        # generate the next set of flakes
        for x in range(self.buffer.width()):
            if random.random() < 0.01:
                flake = _FLAKE(index=random.choice([1, 3, 7]), x=x, y=0)
                self._flakes.append(flake)
        
        if self.smart_transparent and frame_number == 0 and self.image_present:
            self.smart_boundLine = {}
            for x in range(self.img_width):
                tmp_flag = False
                for y in range(self.img_height):
                    if self.image_buffer.buffer[y + self.img_start_y][x + self.img_start_x] not in [" ", None]:
                        self.smart_boundLine[x + self.img_start_x] = y + self.img_start_y - 1
                        tmp_flag = True
                        break
                if not tmp_flag:
                    self.smart_boundLine[x + self.img_start_x] = None

        # determine what flakes are hitting the ground or need to be deleted
        for idx, flake in enumerate(self._flakes):
            # ground flake
            if (
                flake.x >= 0
                and flake.x < self.buffer.width()
                and flake.y >= self.buffer.height() - 1
            ):
                # true_y = flake.y
                
                # need to set the y value to be the actual net available y val
                # what isn't a valid y value? 
                # a -> value that exceeds the buffer height
                # b -> value that intercepts a full flake in the column
                true_y = None
                for y in range(self.buffer.height()-1, -1, -1):
                    if self._ground_flakes[y][flake.x] is None or not self._ground_flakes[y][flake.x].full:
                        true_y = y
                        break
                
                if true_y is None:
                    break
                               
                if isinstance(self._ground_flakes[true_y][flake.x], _FLAKE) and not self._ground_flakes[true_y][flake.x].full:
                    ground_flake: _FLAKE = self._ground_flakes[true_y][flake.x]
                    ground_flake.increment_flake_weight()
                    self._ground_flakes[true_y][flake.x] = ground_flake.copy()
                    del ground_flake
                elif isinstance(self._ground_flakes[true_y][flake.x], _FLAKE):
                    tmp_flake = flake.copy()
                    tmp_flake.set_to_on_ground()
                    tmp_flake.y = true_y - 1
                    self._ground_flakes[true_y - 1][flake.x] = tmp_flake
                else:
                    tmp_flake = flake.copy()
                    tmp_flake.set_to_on_ground()
                    tmp_flake.y = true_y
                    self._ground_flakes[true_y][flake.x] = tmp_flake
                self._flakes[idx] = None
                self.buffer.put_char(flake.prev_x, flake.prev_y, " ")
            elif (
                flake.x < 0
                or flake.x >= self.buffer.width()

            ):
                self._flakes[idx] = None
                self.buffer.put_char(flake.prev_x, flake.prev_y, " ")
            else:
                # image collision flake
                if not self.smart_transparent:
                    if (
                        self.image_present and
                        flake.x >= self.image_x_boundaries[0] and
                        flake.x <= self.image_x_boundaries[1] and
                        flake.y >= self.image_y_boundaries[0] and
                        flake.y <= self.image_y_boundaries[1]
                    ):
                        # colliding with image
                        if isinstance(self._image_collide_flakes[flake.x], _FLAKE):
                            ground_flake: _FLAKE = self._image_collide_flakes[flake.x].copy()
                            ground_flake.increment_flake_weight()
                            self._image_collide_flakes[flake.x] = ground_flake
                            del ground_flake
                        else:
                            tmp_flake = flake.copy()
                            tmp_flake.set_to_on_ground()
                            tmp_flake.y = self.image_y_boundaries[0] - 1
                            self._image_collide_flakes[flake.x] = tmp_flake
                        self._flakes[idx] = None
                        self.buffer.put_char(flake.prev_x, flake.prev_y, " ")
                elif frame_number != 0:
                    if self.image_present and flake.x in self.smart_boundLine.keys():
                        if start_bound := self.smart_boundLine[flake.x]:
                            if (
                                flake.y >= start_bound and
                                flake.y <= self.img_end_y
                            ):
                                # colliding with image
                                self._flakes[idx] = None
                                self.buffer.put_char(flake.prev_x, flake.prev_y, " ")

                                if isinstance(self.buffer.get_char(flake.x, start_bound), _FLAKE):
                                    ground_flake: _FLAKE = self._image_collide_flakes[flake.x].copy()
                                    ground_flake.increment_flake_weight()
                                    self._image_collide_flakes[flake.x] = ground_flake
                                    del ground_flake
                                else:
                                    tmp_flake = flake.copy()
                                    tmp_flake.set_to_on_ground()
                                    tmp_flake.y = start_bound
                                    self._image_collide_flakes[flake.x] = tmp_flake

        
        self._flakes = [flake for flake in self._flakes if flake]

        # place the flakes into the buffer
        for flake in self._flakes:
            self.buffer.put_char(flake.x, flake.y, flake)
            self.buffer.put_char(flake.prev_x, flake.prev_y, " ")

        # place the ground flakes
        if self.collision:
            for y in range(self.buffer.height()):
                for x in range(self.buffer.width()):
                    flake = self._ground_flakes[y][x]
                    if flake:
                        self.buffer.put_char(flake.x, flake.y, flake)
            for flake in self._image_collide_flakes:
                if flake:
                    self.buffer.put_char(flake.x, flake.y, flake)

        if self._show_info:
            self.buffer.put_at(0, 1, f"Width: {self.buffer.width()}")
            self.buffer.put_at(0, 2, f"Height: {self.buffer.height()}")
            self.buffer.put_at(0, 3, f"Collision Enabled: {self.collision}")
            self.buffer.put_at(0, 4, f"Total  flakes: {len(self._flakes):3d}")
            self.buffer.put_at(
                0, 5, f"Ground flakes: {sum([sum([1 for x in range(len(self._ground_flakes[0])) if self._ground_flakes[y][x]]) for y in range(len(self._ground_flakes))]):3d}"
            )
            self.buffer.put_at(0, 6, f"Full flakes: {sum([1 for flake in [j for sub in self._ground_flakes for j in sub] if flake and flake.full]):3d}")
            self.buffer.put_at(0, 7, f"Image present: {self.image_present}")
            if self.image_present:
                self.buffer.put_at(0, 8, f"Total flakes on image: {len([0 for _ in self._image_collide_flakes if _]):3d}")
                self.buffer.put_at(0, 9, f"Image x boundaries: {self.image_x_boundaries}")
                self.buffer.put_at(0, 10, f"Image y boundaries: {self.image_y_boundaries}")
                self.buffer.put_at(0, 11, f"Image y bottom: {self.img_end_y}")

        # for flake in [j for sub in self._ground_flakes for j in sub]:
        #     if flake:
        #         print(f"{flake.weight} - {flake.char} - {flake.full}")


_TWINKLE_COLORS = {idx:val for idx, val in enumerate(range(232, 256))}

class _TWINKLE_SPEC:
    def __init__(self, char, value):
        self.char = char
        self.value = value
        self.fade = bruhcolored(self.char, _TWINKLE_COLORS[self.value])
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
        
        self.fade = bruhcolored(self.char, _TWINKLE_COLORS[self.value])
        return self
    
    def copy(self):
        new_TWINKLE_SPEC = _TWINKLE_SPEC(self.char, self.value)
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
                        new_TWINKLE_SPEC = _TWINKLE_SPEC(".", random.randint(0, 23))
                        self.buffer.put_char(x, y, new_TWINKLE_SPEC)
                        self.specs.append((x, y))   
        else:
            for x, y in self.specs:
                spec = self.buffer.get_char(x, y)
                self.buffer.put_char(x, y, spec.next().copy())
                del spec
                
                
class AudioEffect(BaseEffect):
    def __init__(self, buffer, background: str, num_bands: int = 24, audio_halt: int = 10):
        super(AudioEffect, self).__init__(buffer, background)
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.BANDS = num_bands
        self.audio_halt = audio_halt
        self.bands = []
        self.p = pyaudio.PyAudio()
        self.upper_band_bound = self.buffer.height()
        self.band_ranges = self.generate_even_ranges(self.BANDS, 0, self.buffer.width())
        self.colors = [random.randint(0, 255) for _ in range(self.BANDS)]
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK, stream_callback=self.process_audio)
        self.gradient_mode = "extend"
        self.base_gradient = [232, 233, 235, 237, 239, 241, 243, 245, 247, 249, 251, 253, 255]
        self.gradient = [color for color in self.base_gradient for _ in range(self.BANDS)]
        self.true_gradient = [self.gradient[idx] for idx in range(self.buffer.width())]
        self.use_gradient = True
        self.non_gradient_color = 27
        self.orientation = "top"
        self.subtract_y = self.buffer.height()
    
    def set_audio_properties(self, num_bands = 24, audio_halt = 10, use_gradient = True, non_gradient_color=27):
        self.BANDS = num_bands
        self.audio_halt = audio_halt
        self.band_ranges = self.generate_even_ranges(self.BANDS, 0, self.buffer.width())
        self.colors = [random.randint(0, 255) for _ in range(self.BANDS)]
        self.use_gradient = use_gradient
        self.non_gradient_color = non_gradient_color
    
    def evenly_distribute_original_values(self, original_list, desired_width):
        repeat_count = desired_width // len(original_list)
        extra_elements = desired_width % len(original_list)
        expanded_list = []
        for value in original_list:
            expanded_list.extend([value] * repeat_count)
            if extra_elements > 0:
                expanded_list.append(value)
                extra_elements -= 1
        return expanded_list
    
    def set_orientation(self, orientation):
        if orientation in ["top", "bottom"]:
            self.orientation = orientation
            if self.orientation == "bottom":
                self.subtract_y = self.buffer.height()
            else:
                self.subtract_y = 0
    
    def set_audio_gradient(self, gradient=[232, 233, 235, 237, 239, 241, 243, 245, 247, 249, 251, 253, 255], mode="extend"):
        self.base_gradient = gradient
        self.gradient_mode = mode
        if self.gradient_mode == "repeat":
            self.gradient = []
            for _ in range(self.BANDS):
                self.gradient += self.base_gradient
            self.true_gradient = [self.gradient[idx] for idx in range(self.buffer.width())]
        else:
            self.gradient = self.evenly_distribute_original_values(gradient, self.buffer.width())
            self.true_gradient = [self.gradient[idx] for idx in range(self.buffer.width())]
    
    def process_audio(self, data, frame_count, time_info, status):
        audio_array = np.frombuffer(data, dtype=np.int16)
        fft_result = np.fft.rfft(audio_array)
        magnitudes = np.abs(fft_result)
        band_width = len(magnitudes) // self.BANDS
        self.bands = [np.mean(magnitudes[i*band_width:(i+1)*band_width]) for i in range(self.BANDS)]
        return (data, pyaudio.paContinue)

    def map_bands_to_range(self, N):
        min_band = min(self.bands)
        max_band = max(self.bands)
        rand_band = max_band - min_band if max_band != min_band else 1
        normalized_bands = [(band - min_band) / rand_band for band in self.bands]
        scaled_bands = [int(band * N) for band in normalized_bands]
        return scaled_bands

    def generate_even_ranges(self, groups, start, end):
        approximate_group_size = round((end - start) / groups)
        intervals = []
        for i in range(groups):
            group_start = start + i * approximate_group_size
            group_end = group_start + approximate_group_size
            intervals.append((group_start, min(group_end, end)))
        return intervals
    
    def render_frame(self, frame_number):        
        if frame_number == 0: self.stream.start_stream()
        
        if frame_number % self.audio_halt == 0:
            try:
                self.buffer.clear_buffer()
                mapped_bands = self.map_bands_to_range(self.upper_band_bound)
                for idx, band_group in enumerate(zip(mapped_bands, self.band_ranges)):
                    band, band_range = band_group
                    for y_change in range(band):
                        for x_change in range(*band_range):
                            if self.use_gradient:
                                self.buffer.put_char(x_change, abs(self.subtract_y - y_change), bruhcolored(" ", on_color=self.true_gradient[x_change]).colored, False)
                            else:
                                self.buffer.put_char(x_change, abs(self.subtract_y - y_change), bruhcolored(" ", on_color=self.non_gradient_color).colored, False)
            except:
                pass
    
        