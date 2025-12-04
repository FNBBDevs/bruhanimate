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

from ..bruhutil import VALID_DIRECTIONS
from ..bruhutil.bruhffer import Buffer
from .base_effect import BaseEffect


class OffsetEffect(BaseEffect):
    """
    Class for generating an offset-static backgorund.
    :new-param direction: which way the offset should go.
    """

    def __init__(self, buffer: Buffer, background: str, direction: str = "right"):
        """
        Initializes the offset effect.

        Args:
            buffer (Buffer): Effect buffer to push updates to.
            background (str): Character or string to use as the background.
            direction (str): Direction for the effect, defaults to right.
        """
        super(OffsetEffect, self).__init__(buffer, background)
        self.direction = direction if direction in VALID_DIRECTIONS else "right"

    def update_direction(self, direction: str):
        """
        Function to update the direction of the offset.

        Args:
            direction (str): Direction the background text should go.
        """
        self.direction = direction if direction in VALID_DIRECTIONS else "right"
        self.buffer.clear_buffer()

    def render_frame(self, frame_number: int):
        """
        Function to render the frame based on the current direction and frame number.

        Args:
            frame_number (int): Current frame number of the animation. Not used by the effect, but required for backwards compatibility.
        """
        for y in range(self.buffer.height()):
            row = (
                self.background[y % self.background_length :]
                + self.background[: y % self.background_length]
            ) * (self.buffer.width() // self.background_length + self.background_length)
            if self.direction == "right":
                self.buffer.put_at(0, y, row[::-1])
            else:
                self.buffer.put_at(0, y, row)
