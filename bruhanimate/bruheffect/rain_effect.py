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

from ..bruhutil import WIND_DIRECTIONS, Buffer
from .base_effect import BaseEffect


class RainEffect(BaseEffect):
    """
    Effect to emmulate the look of rain
    """

    def __init__(
        self,
        buffer: Buffer,
        background: str,
        img_start_x: int = None,
        img_start_y: int = None,
        img_width: int = None,
        img_height: int = None,
        collision: bool = False,
        intensity: int = 1,
        swells: bool = False,
        wind_direction: str = "none",
    ):
        """
        Initialize the RainEffect class with given parameters.

        Args:
            buffer (Buffer): Effect buffer to push updates to.
            background (str): Character or string to use for the background.
            img_start_x (int, optional): Where the image starts on the x axis. Defaults to None.
            img_start_y (int, optional): Where the image starts on the y axis. Defaults to None.
            img_width (int, optional): The width of the image. Defaults to None.
            img_height (int, optional): The height of the image. Defaults to None.
            collision (bool, optional): Whether or not the effect should hit the image. Defaults to False.
            intensity (int, optional): How intense should the rain be. Defaults to 1.
            swells (bool, optional): Where or not to increase and deacrease the intensity automatically. Defaults to False.
            wind_direction (str, optional): Which direction the rain should fall. Defaults to "none".
        """
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

    def update_multiplier(self, val: int):
        """
        Update the multiplier value that relates to shift amount.

        Args:
            val (int): multiplier value
        """
        self.multiplier = val

    def update_wind_direction(self, direction: str):
        """
        Update the direction of the rain.

        Args:
            direction (str): Direction the rain should fall.
        """
        if direction in WIND_DIRECTIONS:
            self.wind_direction = direction
            self._set_rain()

    def _set_rain(self):
        """
        Set the rain based on intensity and wind direction.
        """
        self.rain = f"{' ' * (1000 - self.intensity)}"
        if self.intensity > 50:
            self.rain += "."
        if self.intensity > 250:
            self.rain += "."
        if self.intensity > 500:
            self.rain += self.wind_mappings[self.wind_direction][0]
        self.rain_length = len(self.rain)

    def update_intensity(self, intensity: int):
        """
        Function to update the intensity of the rain.

        Args:
            intensity (int): The intensity of the rain.
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
        img_start_x: int,
        img_start_y: int,
        img_width: int,
        img_height: int,
        collision: bool,
        smart_transparent: bool = False,
        image_buffer: Buffer = None,
    ):
        """
        Function to set whether or not to visually see the rain collide with the ground
        or images if they are present.
        Args:
            img_start_x (int): Where the image starts on the screen.
            img_start_y (int): Where the image starts on the screen.
            img_width (int): The width of the image.
            img_height (int): The height of the image.
            collision (bool): Update collision variable.
            smart_transparent (bool): Update smart_transparent. Defaults to False.
            image_buffer (Buffer): The buffer that contains the image. Defaults to None.
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

    def update_swells(self, swells: bool):
        """
        Function to update whether or not there are swells in the rain effect.

        Args:
            swells (bool): Whether or not there are swells in the rain effect.
        """
        self.swells = swells

    def render_frame(self, frame_number: int):
        """
        Function to render the next frame of the Rain Effect.

        Args:
            frame_number (int): The current frame number to render.
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
