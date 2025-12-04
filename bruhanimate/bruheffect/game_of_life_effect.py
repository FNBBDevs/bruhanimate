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

from ..bruhutil import LIFE_COLORS, LIFE_SCALES, Buffer
from .base_effect import BaseEffect


class GameOfLifeEffect(BaseEffect):
    """
    Effect ot simulate Conway's Game of Life
    """

    def __init__(
        self,
        buffer: Buffer,
        background: str,
        decay: bool = False,
        color: bool = False,
        color_type: str = None,
        scale: str = "random",
    ):
        """
        Initialize the Game of Life effect with a buffer and background color.

        Args:
            buffer (Buffer): Effect buffer to push updates to.
            background (str): Character of string to use as the background.
            decay (bool, optional): Whether or not cells should decay. Defaults to False.
            color (bool, optional): Whether or not the decay should use color. Defaults to False.
            color_type (str, optional): Type of color scale to use. Defaults to None.
            scale (str, optional): Type of gray scale to use. Defaults to "random".
        """
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
        Function to set the attributes of the effect.
        """
        self.grey_scale = (
            LIFE_SCALES[random.choice(list(LIFE_SCALES.keys()))]
            if self.decay and self.scale == "random"
            else LIFE_SCALES[self.scale]
            if self.decay
            else " o"
        )
        self.colors = [232, 231] if not self.decay else LIFE_COLORS[self.color_type]
        self.ALIVE = len(self.grey_scale) - 1
        self.DEAD = 0
        self.mappings = {i: self.grey_scale[i] for i in range(len(self.grey_scale))}

    def update_decay(
        self, decay: bool, color_type: str = "GREYSCALE", scale: str = "random"
    ):
        """
        Function to enable the decay and select the color map.

        Args:
            decay (bool): Whether or not the cell should decay
            color_type (str, optional): Type of color to use. Defaults to "GREYSCALE".
            scale (str, optional): Type of scale to use. Defaults to "random".
        """
        self.decay = decay
        self.scale = scale
        if color_type:
            self.color_type = color_type
        self._set_attributes()

    def update_rules(self, life_rule: list[int], death_rule: list[int]):
        """
        Function to update the rules for life and death.

        Args:
            life_rule (list[int]): Lower and upper bound for number of neighbors that lead to life.
            death_rule (list[int]): Lower and upper bound for number of neighbors that lead to death.
        """
        self.rules["life"] = life_rule
        self.rules["death"] = death_rule

    def render_frame(self, frame_number: int):
        """
        Function to render the next frame of the GOL effect.

        Args:
            frame_number (int): The current frame number to render.
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
