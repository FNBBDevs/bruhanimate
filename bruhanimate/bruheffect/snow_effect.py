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
    def __init__(
        self,
        buffer: Buffer,
        background,
        img_start_x=None,
        img_start_y=None,
        img_width=None,
        img_height=None,
        collision=False,
        show_info=False,
    ):
        super(SnowEffect, self).__init__(buffer, background)
        self.image_present = (True if img_start_x and img_start_y and img_width and img_height else False)
        self.collision = collision
        self.total_ground_flakes = 0
        self.show_info = show_info
        self.flakes = []
        self.ground_flakes = [[0 for _ in range(buffer.width())] for _ in range(buffer.height())]
        self.image_flakes = [None for _ in range(self.buffer.width())]
        self.smart_transparent = False

    def update_collision(
        self,
        img_start_x,
        img_start_y,
        img_width,
        img_height,
        collision,
        smart_transparent,
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

    def set_show_info(self, show_info: bool):
        self.show_info = show_info

    def generate_snowflake(self, x: int):
        snowflake_type = random.choice(list(SNOWFLAKE_TYPES.keys()))
        snowflake_char = bruhcolored(snowflake_type, SNOWFLAKE_COLORS[snowflake_type])
        self.flakes.append({"x": x, "y": 0, "type": snowflake_type, "colored": snowflake_char, "fall_delay": 0})

    def can_stack(self, x, y):
        if y >= self.buffer.height():
            return False
        return self.ground_flakes[y][x] >= 18

    def is_colliding(self, x: int, y: int):
        if self.image_present:
            if self.image_x_boundaries[0] < x < self.image_x_boundaries[1] and self.image_y_boundaries[0] < y < self.image_y_boundaries[1]:
                return True
        return False

    def handle_snowflake_landing(self, x: int, y: int):
        self.ground_flakes[y][x] += 1
        weight = self.ground_flakes[y][x]
        for w, char in sorted(FLAKE_WEIGHT_CHARS.items(), reverse=True):
            if weight >= w:
                self.buffer.put_char(x, y, char)
                break
        if weight > 18 and y > 0:
            self.ground_flakes[y - 1][x] += 1

    def add_info(self):
        self.buffer.put_at(0, 0, f"Total Snow Flakes: {len(self.flakes)}")
        self.buffer.put_at(0, 1, f"Total Flakes on Ground: {sum([sum([1 for v in row if v > 0]) for row in self.ground_flakes])}")

    def render_frame(self, frame_number):
        """
        Function to render the next frame of the snow effect into it's buffer.
        :param frame_number: The current frame number (used to determine the animation state).
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
