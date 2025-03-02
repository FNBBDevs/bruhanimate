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
from ..bruhutil import FLAKE_WEIGHT_CHARS, SNOWFLAKE_TYPES, SNOWFLAKE_COLORS, Buffer
from .base_effect import BaseEffect


class SnowEffect(BaseEffect):
    """
    A class to represent a snow effect.
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
        show_info: bool = False,
    ):
        """
        Initializes the SnowEffect class.

        Args:
            buffer (Buffer): Effect buffer to render changes to.
            background (str): Character or string used for the background of the effect.
            img_start_x (int, optional): Where the image starts on the x axis. Defaults to None.
            img_start_y (int, optional): Where the image starts on the y axis. Defaults to None.
            img_width (int, optional): The width of the image. Defaults to None.
            img_height (int, optional): The height of the image. Defaults to None.
            collision (bool, optional): Whether or not the effect should collide with the image. Defaults to False.
            show_info (bool, optional): Whether or not to show snowflake information. Defaults to False.
        """
        super(SnowEffect, self).__init__(buffer, background)
        self.image_present = (True if img_start_x and img_start_y and img_width and img_height else False)
        self.collision = collision
        self.total_ground_flakes = 0
        self.show_info = show_info
        self.flakes = []
        self.ground_flakes = [[0 for _ in range(buffer.width())] for _ in range(buffer.height())]
        self.image_flakes = [None for _ in range(self.buffer.width())]
        self.smart_transparent = False
        self.snow_intensity = 0.01

    def update_collision(
        self,
        img_start_x: int,
        img_start_y: int,
        img_width: int,
        img_height: int,
        collision: bool,
        smart_transparent: bool,
        image_buffer: Buffer = None,
    ):
        """
        Function to set whether or not to visually see the snow collide with the ground
        or images if they are present

        Args:
            img_start_x (int): Start of the image on the x axis.
            img_start_y (int): Start of the image on the y axis.
            img_width (int): Width of the image.
            img_height (int): Height of the image.
            collision (bool): Whether or not the effect should collide with the image.
            smart_transparent (bool): not used . . .
            image_buffer (Buffer, optional): The image buffer in order to find collisions. Defaults to None.
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

    def set_show_info(self, show_info: bool):
        """
        Function to set whether or not to display information about the snow effect

        Args:
            show_info (bool): Whether or not to display information about the snow effect
        """
        self.show_info = show_info

    def set_snow_intensity(self, intensity: float):
        """
        Sets the value to compare random.random() against to determine
        if a snowflake should be created.

        Args:
            intensity (float): The value to check random.random() against
        """
        if 0.01 <= intensity <= 1.0:
            self.snow_intensity = intensity

    def generate_snowflake(self, x: int):
        """
        Generates a new snowflake at the given x position.

        Args:
            x (int): The x position to generate the snowflake at.
        """
        snowflake_type = random.choice(list(SNOWFLAKE_TYPES.keys()))
        snowflake_char = bruhcolored(snowflake_type, SNOWFLAKE_COLORS[snowflake_type])
        self.flakes.append({"x": x, "y": 0, "type": snowflake_type, "colored": snowflake_char, "fall_delay": 0})

    def can_stack(self, x: int, y: int):
        """
        Checks if a snowflake can be stacked at the given position.

        Args:
            x (int): The x position to check.
            y (int): The y position to check.

        Returns:
            bool: True if the snowflake can be stacked, False otherwise.
        """
        if y >= self.buffer.height():
            return False
        return self.ground_flakes[y][x] >= 18

    def is_colliding(self, x: int, y: int):
        """
        Checks if a snowflake is colliding with the ground / snowflake at the given position.

        Args:
            x (int): The x position to check.
            y (int): The y position to check.

        Returns:
            bool: True if the snowflake is colliding with the ground / snowflake, False otherwise.
        """
        if self.image_present:
            if self.image_x_boundaries[0] < x < self.image_x_boundaries[1] and self.image_y_boundaries[0] < y < self.image_y_boundaries[1]:
                return True
        return False

    def handle_snowflake_landing(self, x: int, y: int):
        """
        Handles the snowflake landing at the given position.

        Args:
            x (int): The x position where the snowflake is landing.
            y (int): The y position where the snowflake is landing.
        """
        self.ground_flakes[y][x] += 1
        weight = self.ground_flakes[y][x]
        for w, char in sorted(FLAKE_WEIGHT_CHARS.items(), reverse=True):
            if weight >= w:
                self.buffer.put_char(x, y, char)
                break
        if weight > 18 and y > 0:
            self.ground_flakes[y - 1][x] += 1

    def add_info(self):
        """
        Adds information about the falling and grounded snowflakes.
        """
        self.buffer.put_at(0, 0, f"Total Snow Flakes: {len(self.flakes)}")
        self.buffer.put_at(0, 1, f"Total Flakes on Ground: {sum([sum([1 for v in row if v > 0]) for row in self.ground_flakes])}")

    def render_frame(self, frame_number: int):
        """
        Renders a single frame of the snow effect.

        Args:
            frame_number (int): The current frame number to render.
        """

        # generate a new row of snowflakes
        for idx in range(self.buffer.width()):
            if random.random() < 0.01:
                self.generate_snowflake(idx)
    
        # update the positions of all flakes
        new_flakes = []
        for snowflake in self.flakes:
            x, y, flake_type = snowflake["x"], snowflake["y"], snowflake["type"]
            speed = SNOWFLAKE_TYPES[flake_type]["speed"]

            # clear out the old position of the snowflake
            self.buffer.put_char(x, y, " ")

            if snowflake["fall_delay"] < speed:
                snowflake["fall_delay"] += 1
                new_flakes.append(snowflake)
                continue
            else:
                snowflake["fall_delay"] = 0

            if y + 1 >= self.buffer.height() or self.can_stack(x, y + 1):
                self.handle_snowflake_landing(x, y)
            else:
                dx = random.choice([-1, 0, 1])
                dy = 1

                new_x = max(0, min(self.buffer.width() - 1, x + dx))
                new_y = y + dy
                if new_y < self.buffer.height() and not self.is_colliding(new_x, new_y) and 0 <= new_x < self.buffer.width():
                    snowflake["x"], snowflake["y"] = new_x, new_y
                    new_flakes.append(snowflake)
                else:
                    self.handle_snowflake_landing(x, y)

        self.flakes = new_flakes

        # place the updates into the buffer
        for snowflake in self.flakes:
            x, y, flake_type, colored = snowflake["x"], snowflake["y"], snowflake["type"], snowflake["colored"]
            self.buffer.put_char(x, y, colored.colored)
        
        if self.show_info:
            self.add_info()
