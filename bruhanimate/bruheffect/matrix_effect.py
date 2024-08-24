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


class MatrixEffect(BaseEffect):
    """
    Effect to mimic the cliche coding backgroud with falling random characters
    """

    def __init__(
        self,
        buffer,
        background,
        chracter_halt_range=(1, 2),
        color_halt_range=(1, 2),
        character_randomness_one=0.70,
        character_randomness_two=0.60,
        color_randomness=0.50,
        gradient_length=1,
    ):
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
        chacter_halt_range=(1, 2),
        color_halt_range=(1, 2),
        character_randomness_one=0.70,
        character_randomness_two=0.60,
        color_randomness=0.50,
        gradient_length=1,
    ):
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

    def set_matrix_gradient(self, gradient):
        self.__base_gradient = gradient
        self.__gradient = [
            color
            for color in self.__base_gradient
            for _ in range(self.__gradient_length)
        ]

    def get_gradient(self):
        return self.__base_gradient

    def __initialize_buffer(self):
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

    def render_frame(self, frame_number):
        """
        Renders the next frame for the Matrix effect into the effect buffer
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
