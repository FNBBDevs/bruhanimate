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
from ..bruhutil import LIFE_COLORS, Buffer
from .noise_effect import NoiseEffect

class StarEffect(NoiseEffect):
    """
    Class for rendering out a blinking star effect. This is just a Noise effect with a predefined intensity.
    Ideally the background would be ' ' for the best effect, but the choice is yours.
    """

    def __init__(self, buffer: Buffer, background: str, color_type: str = "GREYSCALE"):
        """
        Initializes the Star Effect.

        Args:
            buffer (Buffer): Effect buffer to push updates to.
            background (str): Character or string for the background.
            color_type (str, optional): What color type should be used. Defaults to "GREYSCALE".
        """
        super(StarEffect, self).__init__(buffer, background)

        self.stars = f"{background*(100 // self.background_length)}.*+"
        self.stars_length = len(self.stars)
        self.color_type = color_type

    def update_color_type(self, color_type: str):
        """
        Function to update the color type.

        Args:
            color_type (str): The color type to use for this effect.
        """
        self.color_type = color_type

    def update_background(self, background: str):
        """
        Function to update the background character or string.

        Args:
            background (str): The new background character or string to use.
        """
        self.background = background
        self.background_length = len(background)
        self.stars = f"{background*(100 // self.background_length)}.*+"
        self.stars_length = len(self.stars)

    def render_frame(self, frame_number: int):
        """
        Function to render the next frame of the Stars effect.

        Args:
            frame_number (int): The current frame number to render.
        """
        for y in range(self.buffer.height()):
            for x in range(self.buffer.width()):
                if random.random() < self.intensity:
                    self.buffer.put_char(
                        x,
                        y,
                        bruhcolored(
                            self.stars[random.randint(0, self.stars_length - 1)],
                            color=LIFE_COLORS[self.color_type][
                                random.randint(
                                    0, len(LIFE_COLORS[self.color_type]) - 1
                                )
                            ],
                        ).colored,
                    )
