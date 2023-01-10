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
import time
import random
from abc import ABC, abstractmethod

_VALID_DIRECTIONS = ["right", "left"]
_GREY_SCALES = [' .:-=+*%#@', ' .:;rsA23hHG#9&@']
_WIND_DIRECTIONS = ["east", "west", "none"]
_NOISE = "!@#$%^&*()_+1234567890-=~`qazwsxedcrfvtgbyhnujmik,ol.p;/[']\QAZXSWEDCVFRTGBNHYUJM<KIOL>?:P{\"}|"


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
        for y in range(self.buffer.height()):
            self.buffer.put_at(0, y, self.background * (self.buffer.width() //
                               self.background_length + self.background_length))


class OffsetEffect(BaseEffect):
    """
    Class for generating an offset-static backgorund.
    :new-param direction: which way the offset should go.
    """

    def __init__(self, buffer, background, direction="right"):
        super(OffsetEffect, self).__init__(buffer, background)

        self.direction = direction if direction in _VALID_DIRECTIONS else "right"

    def update_direction(self, direction):
        self.direction = direction if direction in _VALID_DIRECTIONS else "right"
        self.buffer.clear_buffer()

    def render_frame(self, frame_number):
        for y in range(self.buffer.height()):
            row = (self.background[y % self.background_length:] + self.background[:y % self.background_length]) * (
                self.buffer.width() // self.background_length + self.background_length)
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

        self.intensity = intensity / \
            1000 if intensity and 1 <= intensity <= 999 else 200 / 1000

        self.noise = " !@#$%^&*()_+1234567890-=~`qazwsxedcrfvtgbyhnujmik,ol.p;/[']\QAZXSWEDCVFRTGBNHYUJM<KIOL>?:P{\"}|"
        self.noise_length = len(self.noise)

    def update_intensity(self, intensity):
        self.intensity = intensity / \
            1000 if intensity and 1 <= intensity <= 999 else 200 / 1000

    def render_frame(self, frame_number):
        for y in range(self.buffer.height()):
            self.buffer.put_at(0, y, ''.join([self.noise[random.randint(0, self.noise_length - 1)] if random.random(
            ) < self.intensity else self.buffer.get_char(_, y) for _ in range(self.buffer.width())]))


class StarEffect(NoiseEffect):
    """
    Class for rendering out a blinking star effect. This is just a Noise effect with a predefined intensity.
    Ideally the background would be ' ' for the best effect, but the choice is yours.
    """

    def __init__(self, buffer, background):
        super(StarEffect, self).__init__(buffer, background)

        self.stars = f"{background*(100 // self.background_length)}.*+"
        self.stars_length = len(self.stars)

    def update_background(self, background):
        self.background = background
        self.background_length = len(background)
        self.stars = f"{background*(100 // self.background_length)}.*+"
        self.stars_length = len(self.stars)

    def render_frame(self, frame_number):
        for y in range(self.buffer.height()):
            self.buffer.put_at(0, y, ''.join([self.stars[random.randint(0, self.stars_length - 1)] if random.random(
            ) < self.intensity else self.buffer.get_char(_, y) for _ in range(self.buffer.width())]))


class PlasmaEffect(BaseEffect):
    def __init__(self, buffer, background):
        super(PlasmaEffect, self).__init__(buffer, background)

        self.scale = random.choice(_GREY_SCALES)
        self.ayo = 0
        self.vals = [random.randint(1, 50), random.randint(
            1, 50), random.randint(1, 50), random.randint(1, 50)]

    def update_background(self, background):
        self.background = background
        self.background_length = len(self.background)

    def update_plasma_values(self, a=random.randint(1, 50), b=random.randint(1, 50), c=random.randint(1, 50), d=random.randint(1, 50)):
        self.vals = [a, b, c, d]

    def shuffle_plasma_values(self):
        self.vals = [random.randint(1, 50), random.randint(
            1, 50), random.randint(1, 50), random.randint(1, 50)]

    def render_frame(self, frame_number):
        self.ayo += 1
        for y in range(self.buffer.height()):
            for x in range(self.buffer.width()):
                value = abs(self.func(x + self.ayo / 3, y, 1/4, 1/3, self.vals[0]) + self.func(x, y, 1/8, 1/5, self.vals[1])
                            + self.func(x, y + self.ayo / 3, 1/2, 1/5, self.vals[2]) + self.func(x, y, 3/4, 4/5, self.vals[3])) / 4.0
                self.buffer.put_char(
                    x, y, self.scale[int((len(self.scale) - 1) * value)])
        for i in range(4):
            self.buffer.put_at(0, i, f"VAL {i+1}: {str(self.vals[i]):>3s} ")

    def func(self, x, y, a, b, n):
        return math.sin(math.sqrt((x - self.buffer.width() * a) ** 2 + 4 * ((y - self.buffer.height() * b)) ** 2) * math.pi / n)


class GameOfLifeEffect(BaseEffect):
    def __init__(self, buffer, background, decay=False):
        super(GameOfLifeEffect, self).__init__(buffer, background)
        self.decay = decay
        self._set_attributes()
        self.direcitons = [
            [1, 0],
            [0, 1],
            [-1, 0],
            [0, -1],
            [1, 1],
            [1, -1],
            [-1, 1],
            [-1, -1]
        ]

    def _set_attributes(self):
        self.grey_scale = _GREY_SCALES[0] if self.decay else " O"
        self.ALIVE = len(self.grey_scale) - 1
        self.DEAD = 0
        self.mappings = {i: self.grey_scale[i]
                         for i in range(len(self.grey_scale))}

    def set_decay(self, decay):
        self.decay = decay
        self._set_attributes()

    def render_frame(self, frame_number):
        if frame_number == 0:  # INITIALIZE THE GAME
            for y in range(self.buffer.height()):
                for x in range(self.buffer.width()):
                    if random.random() < 0.1:
                        self.buffer.put_char(x, y, self.grey_scale[self.ALIVE])
                    else:
                        self.buffer.put_char(x, y, self.grey_scale[self.DEAD])
        else:  # RUN THE GAME
            all_neighbors = []
            for y in range(self.buffer.height()):
                row_neighbors = [0 for _ in range(self.buffer.width())]
                for x in range(self.buffer.width()):
                    for direction in self.direcitons:
                        if 0 <= y+direction[0] < self.buffer.height() and 0 <= x+direction[1] < self.buffer.width():
                            if self.grey_scale.index(self.buffer.get_char(x+direction[1], y+direction[0])) == self.ALIVE:
                                row_neighbors[x] += 1
                all_neighbors.append(row_neighbors)

            for y in range(self.buffer.height()):
                for x in range(self.buffer.width()):
                    if self.grey_scale.index(self.buffer.get_char(x, y)) == self.ALIVE:  # ALIVE
                        if 2 <= all_neighbors[y][x] <= 3:  # STAY ALIVE
                            pass
                        else:  # MOVE TO THE FIRST DECAY STAGE
                            self.buffer.put_char(
                                x, y, self.grey_scale[self.ALIVE - 1])
                    else:  # DEAD
                        if all_neighbors[y][x] == 3:  # COME BACK TO LIFE
                            self.buffer.put_char(
                                x, y, self.grey_scale[self.ALIVE])
                        else:  # MOVE TO THE NEXT STAGE --> IF AT 0 STAY AT 0 i.e. don't decrement
                            current_greyscale_position = self.grey_scale.index(
                                self.buffer.get_char(x, y))
                            current_greyscale_position = current_greyscale_position - \
                                1 if current_greyscale_position > 0 else 0
                            self.buffer.put_char(
                                x, y, self.grey_scale[current_greyscale_position])


class RainEffect(BaseEffect):
    def __init__(self, buffer, background, img_start_x=None, img_start_y=None, img_width=None, img_height=None, collision=False, intensity=1, swells=False, wind_direction="none"):
        super(RainEffect, self).__init__(buffer, background)

        self.img_present = True if img_start_x and img_start_y and img_width and img_height else False
        self.collision = collision
        self.intensity = intensity
        self.swells = swells
        self.swell_direction = 1
        self.wind_direction = wind_direction if wind_direction in _WIND_DIRECTIONS else "none"
        self.wind_mappings = {
            "east": [".\\", -1, ["\\", "."]],
            "none": [".|",   0, ["|", "."]],
            "west": ["./",   1, ["/", "."]]
        }
        self._set_rain()

    def update_wind_direction(self, direction):
        if direction in _WIND_DIRECTIONS:
            self.wind_direction = direction
            self._set_rain()

    def _set_rain(self):
        self.rain = f"{' ' * (1000 - self.intensity)}"
        if self.intensity > 50:
            self.rain += "."
        if self.intensity > 250:
            self.rain += "."
        if self.intensity > 500:
            self.rain += self.wind_mappings[self.wind_direction][0]
        self.rain_length = len(self.rain)

    def update_intensity(self, intensity):
        if self.swells:
            if self.intensity == 900:
                self.swell_direction = -1
            if self.intensity == 0:
                self.swell_direction = 1
            self.intensity += self.swell_direction
        else:
            self.intensity = intensity if intensity < 1000 else 999
        self._set_rain()

    def update_collision(self, img_start_x, img_start_y, img_width, img_height, collision, smart_transparent=False, image_buffer=None):
        self.img_present = True if img_start_x and img_start_y and img_width and img_height else False
        self.collision = collision
        if self.img_present:
            self.img_start_x = img_start_x
            self.img_start_y = img_start_y
            self.img_height = img_height
            self.img_width = img_width
            self.smart_transparent = smart_transparent
            self.image_buffer = image_buffer

    def update_swells(self, swells):
        self.swells = swells

    def render_frame(self, frame_number):
        if self.swells:
            self.update_intensity(None)
        if frame_number == 0:
            self.buffer.put_at(0, 0, ''.join([self.rain[random.randint(
                0, self.rain_length - 1)] for _ in range(self.buffer.width())]))
        else:
            self.buffer.shift(self.wind_mappings[self.wind_direction][1])
            self.buffer.scroll(-1)
            self.buffer.put_at(0, 0, ''.join([self.rain[random.randint(
                0, self.rain_length - 1)] for _ in range(self.buffer.width())]))

            if self.collision:
                for y in range(self.buffer.height()):
                    for x in range(self.buffer.width()):
                        # Wipe prior frames impact
                        if self.buffer.get_char(x, y) == "v":
                            self.buffer.put_char(x, y, " ")
                        else:
                            if self.img_present:
                                # if we are inscope of the image we need to process impacts
                                if self.image_buffer:
                                    if 0 <= y + 1 < self.buffer.height():
                                        if not self.image_buffer.buffer[y+1][x] in [" ", None] and self.buffer.get_char(x, y) in self.wind_mappings[self.wind_direction][2]:
                                            self.buffer.put_char(x, y, "v")

                            # impacting the bottom
                            if y == self.buffer.height() - 1:
                                if self.buffer.get_char(x, y) in self.wind_mappings[self.wind_direction][2]:
                                    self.buffer.put_char(x, y, "v")


class MatrixEffect(BaseEffect):
    def __init__(self, buffer, background):
        super(MatrixEffect, self).__init__(buffer, background)
        self.col = self.buffer.width() // 2
        self.c_count = 0
        self.s_count = 0
        self.chars = random.randint(0, self.buffer.height() - 30)
        self.spaces = self.buffer.height() - self.chars

    def render_frame(self, frame_number):
        if frame_number == 0:
            self.buffer.put_at(0, 0, ''.join([_NOISE[random.randint(0, len(
                _NOISE) - 1)] if random.random() < 0.2 else " " for _ in range(self.buffer.width())]))
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
            self.p1 = (p1[0]*2, p1[1]*2)
            self.p2 = (p2[0]*2, p2[1]*2)
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
                self.buffer.put_at(0, y,  self. background*self.buffer.width())
            for line in self.lines:
                if ((line.p1[0] < 0 and line.p2[0]) < 0 or (line.p1[0] >= self.buffer.width() * 2 and line.p2[0] > self.buffer.width() * 2)
                        or (line.p1[1] < 0 and line.p2[1] < 0) or (line.p1[1] >= self.buffer.height() * 2 and line.p2[1] >= self.buffer.height() * 2)):
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
                                px // 2, py // 2, line_chars[next_char])
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
                                px // 2, py // 2, line_chars[next_char])
                        else:
                            self.buffer.put_char(px // 2, py // 2, self.char)
                if dy == 0 and self.thin and self.char is None:
                    pass
                elif dx > dy:
                    x_draw(line.p1[0], line.p1[1]+1)
                else:
                    y_draw(line.p1[0]+1, line.p1[1])
