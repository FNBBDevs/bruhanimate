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
from .base_effect import BaseEffect
from ..bruhutil import Buffer


class NoiseEffect(BaseEffect):
    """
    A noise effect that adds random pixels to the screen with a specified intensity.
    """

    def __init__(self, buffer: Buffer, background: str, intensity: int = 200, color: bool = False):
        """
        Initializes the NoiseEffect class with a specified buffer, background color, noise intensity, and whether to use colors.

        Args:
            buffer (Buffer): Effect buffer to push updates tol.
            background (str): Character or string for background.
            intensity (int, optional): How offten the nosie should update. Defaults to 200.
            color (bool, optional): Whether or not the effect should use color. Defaults to False.
        """
        super(NoiseEffect, self).__init__(buffer, background)

        self.intensity = (
            intensity / 1000 if intensity and 1 <= intensity <= 999 else 200 / 1000
        )

        self.noise = " !@#$%^&*()_+1234567890-=~`qazwsxedcrfvtgbyhnujmik,ol.p;/[']\QAZXSWEDCVFRTGBNHYUJM<KIOL>?:P{\"}|"
        self.noise_length = len(self.noise)
        self.color = color

    def update_intensity(self, intensity: int):
        """
        Function to update the intensity of the effect
        :param intensity: new intensity
        """
        self.intensity = (
            intensity / 1000 if intensity and 1 <= intensity <= 999 else 200 / 1000
        )

    def update_color(self, color: bool, characters: str):
        """
        Function to update the color and character set for the noise.

        Args:
            color (bool): Whether or not the noise should use color.
            characters (str): The set of characters that can be used for noise generation.
        """
        self.color = color
        self.characters = characters

    def render_frame(self, frame_number: int):
        """
        Function to render the frame with noise effect applied.

        Args:
            frame_number (int): The current frame number being rendered.
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
