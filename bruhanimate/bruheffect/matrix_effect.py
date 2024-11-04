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
import string

from bruhcolor import bruhcolored
from .base_effect import BaseEffect
from ..bruhutil import Buffer


class MatrixEffect(BaseEffect):
    """
    Effect to mimic the cliche coding backgroud with falling random characters.
    """

    def __init__(
        self,
        buffer: Buffer,
        background: str,
        chracter_halt_range: tuple[int] = (1, 2),
        color_halt_range: tuple[int] = (1, 2),
        character_randomness_one: float = 0.70,
        character_randomness_two: float = 0.60,
        color_randomness: float = 0.50,
        gradient_length: int = 1,
    ):
        """
        Initialize the MatrixEffect class.

        Args:
            buffer (Buffer): Effect buffer to push changes to.
            background (str): Character or string used for the background.
            chracter_halt_range (tuple[int], optional): Halt range. Defaults to (1, 2).
            color_halt_range (tuple[int], optional): Halt range. Defaults to (1, 2).
            character_randomness_one (float, optional): Frequency to update a character. Defaults to 0.70.
            character_randomness_two (float, optional): Frequency to update a character. Defaults to 0.60.
            color_randomness (float, optional): Frequency to move the color gradient. Defaults to 0.50.
            gradient_length (int, optional): Length of the color gradient. Defaults to 1.
        """
        super(MatrixEffect, self).__init__(buffer, background)
        self.__character_choices = (
            string.ascii_letters + "1234567890!@#$%^&*()_+-=<>,.:\";'{}[]?/"
        )
        self.__character_halt_range = chracter_halt_range
        self.__color_halt_range = color_halt_range
        self.__character_halts = [
            random.randint(
                self.__character_halt_range[0], self.__character_halt_range[1]
            )
            for _ in range(self.buffer.height())
        ]
        self.__color_halts = [
            random.randint(self.__color_halt_range[0], self.__color_halt_range[1])
            for _ in range(self.buffer.height())
        ]
        self.__character_randomness_one = character_randomness_one
        self.__character_randomness_two = character_randomness_two
        self.__color_randomness = color_randomness
        self.__gradient_length = gradient_length
        self.__base_gradient = [
            232,
            233,
            234,
            235,
            236,
            237,
            238,
            239,
            240,
            241,
            242,
            243,
            244,
            245,
            246,
            247,
            248,
            249,
            250,
            251,
            252,
            253,
            254,
            255,
        ]
        self.__gradient = [
            color
            for color in self.__base_gradient
            for _ in range(self.__gradient_length)
        ]
        self.__character_frame_numbers = [0 for _ in range(self.buffer.height())]
        self.__color_frame_numbers = [0 for _ in range(self.buffer.height())]
        self.__buffer_characters = [
            [" " for x in range(self.buffer.width())]
            for y in range(self.buffer.height())
        ]

    def set_matrix_properties(
        self,
        chacter_halt_range: tuple[int] = (1, 2),
        color_halt_range: tuple[int] = (1, 2),
        character_randomness_one: float = 0.70,
        character_randomness_two: float = 0.60,
        color_randomness: float = 0.50,
        gradient_length: int = 1,
    ):
        """
        Set the matrix properties for the MatrixEffect.

        Args:
            chracter_halt_range (tuple[int], optional): Halt range. Defaults to (1, 2).
            color_halt_range (tuple[int], optional): Halt range. Defaults to (1, 2).
            character_randomness_one (float, optional): Frequency to update a character. Defaults to 0.70.
            character_randomness_two (float, optional): Frequency to update a character. Defaults to 0.60.
            color_randomness (float, optional): Frequency to move the color gradient. Defaults to 0.50.
            gradient_length (int, optional): Length of the color gradient. Defaults to 1.
        """
        self.__character_randomness_one = character_randomness_one
        self.__character_randomness_two = character_randomness_two
        self.__color_randomness = color_randomness
        self.__character_halt_range = chacter_halt_range
        self.__color_halt_range = color_halt_range
        self.__gradient_length = gradient_length
        self.__gradient = [
            color
            for color in self.__base_gradient
            for _ in range(self.__gradient_length)
        ]
        self.__character_halts = [
            random.randint(
                self.__character_halt_range[0], self.__character_halt_range[1]
            )
            for _ in range(self.buffer.height())
        ]
        self.__color_halts = [
            random.randint(self.__color_halt_range[0], self.__color_halt_range[1])
            for _ in range(self.buffer.height())
        ]

    def set_matrix_gradient(self, gradient: list[int]):
        """
        Set the base gradient of the matrix. This will reset the current gradient and recreate it based on the new base gradient.

        Args:
            gradient (list[int]): List of colors.
        """
        self.__base_gradient = gradient
        self.__gradient = [
            color
            for color in self.__base_gradient
            for _ in range(self.__gradient_length)
        ]

    def get_gradient(self):
        """
        Get the current gradient.

        Returns:
            list[int]: The current gradient.
        """
        return self.__base_gradient

    def __initialize_buffer(self):
        """
        Initialize the buffer with characters and colors based on the current settings.
        """
        for y in range(self.buffer.height()):
            for x in range(self.buffer.width()):
                self.__buffer_characters[y][x] = random.choice(self.__character_choices)
            for x in range(self.buffer.width()):
                self.buffer.put_char(
                    x,
                    y,
                    bruhcolored(
                        self.__buffer_characters[y][x],
                        self.__gradient[x % len(self.__gradient)],
                    ).colored,
                )

    def render_frame(self, frame_number: int):
        """
        Render a single frame of the matrix effect.

        Args:
            frame_number (int): The current frame number.
        """
        if frame_number == 0:
            self.__initialize_buffer()
        else:
            for y in range(self.buffer.height()):
                if (
                    frame_number % self.__character_halts[y] == 0
                    and random.random() < self.__character_randomness_one
                ):
                    self.__character_frame_numbers[y] += 1
                    for x in range(self.buffer.width()):
                        if random.random() < self.__character_randomness_two:
                            self.__buffer_characters[y][x] = random.choice(
                                self.__character_choices
                            )

                if (
                    frame_number % self.__color_halts[y] == 0
                    and random.random() < self.__color_randomness
                ):
                    self.__color_frame_numbers[y] += 1
                    for x in range(self.buffer.width()):
                        self.buffer.put_char(
                            x,
                            y,
                            bruhcolored(
                                self.__buffer_characters[y][x],
                                color=self.__gradient[
                                    (x - self.__color_frame_numbers[y])
                                    % len(self.__gradient)
                                ],
                            ),
                        )
