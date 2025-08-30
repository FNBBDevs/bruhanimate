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

from .base_renderer import BaseRenderer
from ..bruhutil import Screen
from ..bruhutil.bruhtypes import EffectType


class CenterRenderer(BaseRenderer):
    """
    A renderer to load an image in the center of the screen.
    Updates the image_buffer only
    """

    def __init__(
        self,
        screen: Screen,
        img: list[str],
        frames: int = 100,
        frame_time: float = 0.1,
        effect_type: EffectType = "static",
        background: str = " ",
        transparent: bool = False,
        collision: bool = False
    ):
        super(CenterRenderer, self).__init__(
            screen, frames, frame_time, effect_type, background, transparent, collision
        )
        self.background = background
        self.transparent = transparent

        # Image attributes
        self.img = img
        self.img_height = len(self.img)
        self.img_width = len(self.img[0])
        self.img_y_start = (self.height - self.img_height) // 2
        self.img_x_start = (self.width - self.img_width) // 2
        self.current_img_x = self.img_x_start
        self.current_img_y = self.img_y_start
        self.none_fill_char = None
        
    def render_img_frame(self, frame_number):
        """
        Renders the image at its center position in each frame.

        Args:
            frame_number (int): The current frame number.
        """
        # Image is only rendered once, on frame 0
        if frame_number == 0:
            if self.smart_transparent:
                for y in range(self.height):
                    for x in range(self.width):
                        if (
                            y >= self.img_y_start
                            and y < self.img_y_start + self.img_height
                            and x >= self.img_x_start
                            and x < self.img_x_start + self.img_width
                        ):
                            self.image_buffer.put_char(
                                x,
                                y,
                                self.img[y - self.img_y_start][x - self.img_x_start],
                            )
                # Now process spaces from left-to-right till a non-space character is hit.
                # Then do the same right-to-left. Place these spaces with None
                for y in range(self.height):
                    if y >= self.img_y_start and y < self.img_y_start + self.img_height:
                        for x in range(self.width):
                            if (
                                x >= self.img_x_start
                                and x < self.img_x_start + self.img_width
                            ):
                                if self.image_buffer.get_char(x, y) != " ":
                                    break
                                else:
                                    self.image_buffer.put_char(x, y, None)
                            else:
                                self.image_buffer.put_char(x, y, None)
                        for x in range(self.width - 1, -1, -1):
                            if (
                                x >= self.img_x_start
                                and x < self.img_x_start + self.img_width
                            ):
                                if self.image_buffer.get_char(x, y) != " ":
                                    break
                                else:
                                    self.image_buffer.put_char(x, y, None)
                            else:
                                self.image_buffer.put_char(x, y, None)
                    else:
                        for x in range(self.width):
                            self.image_buffer.put_char(x, y, None)
            else:
                for y in range(self.height):
                    if y >= self.img_y_start and y < self.img_y_start + self.img_height:
                        self.image_buffer.put_at_center(
                            y,
                            self.img[y - self.img_y_start],
                            transparent=self.transparent,
                        )