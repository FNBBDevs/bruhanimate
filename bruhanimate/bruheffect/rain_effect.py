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

from ..bruhutil import WIND_DIRECTIONS
from .base_effect import BaseEffect


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
            wind_direction if wind_direction in WIND_DIRECTIONS else "none"
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
        if direction in WIND_DIRECTIONS:
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
