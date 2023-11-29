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
import random
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
                for _ in range(self.buffer.width()):
                    if random.random() < self.intensity:
                        if self.characters:
                            self.buffer.put_char(
                                _,
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
                                _,
                                y,
                                bruhcolored(
                                    " ", on_color=random.randint(0, 255)
                                ).colored,
                            )
        else:
            for y in range(self.buffer.height()):
                for _ in range(self.buffer.width()):
                    if random.random() < self.intensity:
                        self.buffer.put_char(
                            _, y, self.noise[random.randint(0, self.noise_length - 1)]
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
            random.randint(1, 50),
            random.randint(1, 50),
            random.randint(1, 50),
            random.randint(1, 50),
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

    def __init__(self, buffer, background):
        super(MatrixEffect, self).__init__(buffer, background)
        self.col = self.buffer.width() // 2
        self.c_count = 0
        self.s_count = 0
        self.chars = random.randint(0, self.buffer.height() - 30)
        self.spaces = self.buffer.height() - self.chars

    def render_frame(self, frame_number):
        """
        Renders the next frame for the Matrix effect into the effect buffer
        """
        if frame_number == 0:
            self.buffer.put_at(
                0,
                0,
                "".join(
                    [
                        _NOISE[random.randint(0, len(_NOISE) - 1)]
                        if random.random() < 0.2
                        else " "
                        for _ in range(self.buffer.width())
                    ]
                ),
            )
        else:
            row = []
            for _ in range(self.buffer.width()):
                if self.buffer.get_char(_, 0) != " ":
                    # IF THERE IS A CHAR BELOW US THEN RANDOMLY DECIDE TO CONTINUE THE CHAIN
                    if random.random() < 0.5:
                        row.append(_NOISE[random.randint(0, len(_NOISE) - 1)])
                    else:
                        row.append(" ")
                else:
                    if random.random() < 0.01:
                        row.append(_NOISE[random.randint(0, len(_NOISE) - 1)])
                    else:
                        row.append(" ")
            self.buffer.scroll(-1)
            if len(row) > 0:
                self.buffer.put_at(0, 0, "".join(row))


class _LINE:
    def __init__(self, p1, p2):
        if p1 and p2:
            self.p1 = (p1[0] * 2, p1[1] * 2)
            self.p2 = (p2[0] * 2, p2[1] * 2)
        else:
            self.p1 = None
            self.p2 = None

    def update_points(self, p1, p2):
        self.p1 = (p1[0], p1[1])
        self.p2 = (p2[0], p2[1])

    def get_points(self):
        return self.p1, self.p2


class DrawLines(BaseEffect):
    def __init__(self, buffer, background, char=None, thin=False):
        super(DrawLines, self).__init__(buffer, background)
        self.lines = []
        self.char = char
        self.thin = thin

    def add_line(self, p1, p2):
        self.lines.append(_LINE(p1, p2))

    def render_frame(self, frame_number):
        if frame_number == 0 and len(self.lines) > 0:
            for y in range(self.buffer.height()):
                self.buffer.put_at(0, y, self.background * self.buffer.width())
            for line in self.lines:
                if (
                    (line.p1[0] < 0 and line.p2[0]) < 0
                    or (
                        line.p1[0] >= self.buffer.width() * 2
                        and line.p2[0] > self.buffer.width() * 2
                    )
                    or (line.p1[1] < 0 and line.p2[1] < 0)
                    or (
                        line.p1[1] >= self.buffer.height() * 2
                        and line.p2[1] >= self.buffer.height() * 2
                    )
                ):
                    return

                line_chars = " ''^.|/7.\\|Ywbd#"
                dx = abs(line.p2[0] - line.p1[0])
                dy = abs(line.p2[1] - line.p1[1])

                cx = -1 if line.p1[0] > line.p2[0] else 1
                cy = -1 if line.p1[1] > line.p2[1] else 1

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
                    while ix != line.p2[0]:
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

                    while iy != line.p2[1]:
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
                    x_draw(line.p1[0], line.p1[1] + 1)
                else:
                    y_draw(line.p1[0] + 1, line.p1[1])


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

    def flip_flake(self):
        if self.char == _FLAKE_FLIPS[self.index][0]:
            self.char = _FLAKE_FLIPS[self.index][1]
        else:
            self.char = _FLAKE_FLIPS[self.index][0]

    def next_position(self, current_x, current_y, frame_number):
        if self.on_ground:
            return (current_x, current_y)

        if frame_number % self.index != 0:
            return (current_x, current_y)

        if random.random() < 0.10:
            return (current_x, current_y)

        current_y = current_y + random.choice(_FLAKE_JUMPS[self.index])

        next_position = random.choice(["left", "center", "right"])

        next_flake_move = (
            _NEXT_FLAKE_MOVE[(self.current_position, next_position)]
            if self.current_position != next_position
            else None
        )

        if next_flake_move:
            current_x = current_x + next_flake_move
            self.current_position = next_position

        return (current_x, current_y)

    def update_position(self, x, y):
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
        self.weight += 1
        if self.weight > max(_FLAKE_WEIGHT_CHARS.keys()):
            self.weight = max(_FLAKE_WEIGHT_CHARS.keys())
        self.update_ground_flake()

    def update_ground_flake(self):
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

    def copy(self):
        new_flake = _FLAKE(index=self.index, x=self.x, y=self.y)
        new_flake.weight = self.weight
        new_flake.char = self.char
        new_flake.current_position = self.current_position
        new_flake.color = self.color
        new_flake.on_ground = self.on_ground
        return new_flake


class _FLAKEv2:
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
        self.weight += 1
        if self.weight > max(_FLAKE_WEIGHT_CHARS.keys()):
            self.weight = max(_FLAKE_WEIGHT_CHARS.keys())
        self.update_ground_flake()

    def update_ground_flake(self):
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
        new_flake = _FLAKEv2(index=self.index, x=self.x, y=self.y)
        new_flake.weight = self.weight
        new_flake.char = self.char
        new_flake.current_position = self.current_position
        new_flake.color = self.color
        new_flake.on_ground = self.on_ground
        new_flake.x = self.x
        new_flake.y = self.y
        new_flake.prev_x = self.prev_x
        new_flake.prev_y = self.prev_y
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
        self._ground_flakes = [None for _ in range(self.buffer.width())]
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
                flake = _FLAKEv2(index=random.choice([1, 3, 7]), x=x, y=0)
                self._flakes.append(flake)
        
        if self.smart_transparent and frame_number == 0 and self.image_present:
            self.smart_bound_line = {}
            for x in range(self.img_width):
                tmp_flag = False
                for y in range(self.img_height):
                    if self.image_buffer.buffer[y + self.img_start_y][x + self.img_start_x] not in [" ", None]:
                        self.smart_bound_line[x + self.img_start_x] = y + self.img_start_y - 1
                        tmp_flag = True
                        break
                if not tmp_flag:
                    self.smart_bound_line[x + self.img_start_x] = None

        # determine what flakes are hitting the ground or need to be deleted
        for idx, flake in enumerate(self._flakes):
            # ground flake
            if (
                flake.x >= 0
                and flake.x < self.buffer.width()
                and flake.y >= self.buffer.height() - 1
            ):
                if isinstance(self._ground_flakes[flake.x], _FLAKEv2):
                    ground_flake: _FLAKEv2 = self._ground_flakes[flake.x]
                    ground_flake.increment_flake_weight()
                    self._ground_flakes[flake.x] = ground_flake.copy()
                    del ground_flake
                else:
                    tmp_flake = flake.copy()
                    tmp_flake.set_to_on_ground()
                    tmp_flake.y = self.buffer.height() - 1
                    self._ground_flakes[flake.x] = tmp_flake
                self._flakes[idx] = None
                self.buffer.put_char(flake.prev_x, flake.prev_y, " ")
            elif (
                flake.x < 0
                or flake.x >= self.buffer.width()
                or flake.y < 0

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
                        if isinstance(self._image_collide_flakes[flake.x], _FLAKEv2):
                            ground_flake: _FLAKEv2 = self._image_collide_flakes[flake.x].copy()
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
                    if self.image_present and flake.x in self.smart_bound_line.keys():
                        if start_bound := self.smart_bound_line[flake.x]:
                            if (
                                flake.y >= start_bound and
                                flake.y <= self.img_end_y
                            ):
                                # colliding with image
                                self._flakes[idx] = None
                                self.buffer.put_char(flake.prev_x, flake.prev_y, " ")

                                if isinstance(self.buffer.get_char(flake.x, start_bound), _FLAKEv2):
                                    ground_flake: _FLAKEv2 = self._image_collide_flakes[flake.x].copy()
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
            for flake in self._ground_flakes:
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
                0, 5, f"Ground flakes: {len([0 for _ in self._ground_flakes if _]):3d}"
            )
            self.buffer.put_at(0, 6, f"Image present: {self.image_present}")
            if self.image_present:
                self.buffer.put_at(0, 7, f"Total flakes on image: {len([0 for _ in self._image_collide_flakes if _]):3d}")
                self.buffer.put_at(0, 8, f"Image x boundaries: {self.image_x_boundaries}")
                self.buffer.put_at(0, 9, f"Image y boundaries: {self.image_y_boundaries}")
                self.buffer.put_at(0, 10, f"Image y bottom: {self.img_end_y}")

