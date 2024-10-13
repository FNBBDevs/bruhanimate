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

from typing import List, Tuple, Optional
from .base_renderer import BaseRenderer
from ..bruhutil import Screen
from ..bruhutil.bruhtypes import EffectType, PanRendererDirection, valid_pan_renderer_directions
from ..bruhutil.bruherrors import InvalidPanRendererDirectionError


class PanRenderer(BaseRenderer):
    """
    A renderer to pan an image across the screen.
    Updates the image_buffer only.
    """

    def __init__(
        self,
        screen: Screen,
        img: List[str],
        frames: int = 100,
        frame_time: float = 0.1,
        effect_type: EffectType = "static",
        background: str = " ",
        transparent: bool = False,
        collision: bool = False,
        direction: PanRendererDirection = "horizontal",
        shift_rate: int = 1,
        loop: bool = False,
    ) -> None:
        super().__init__(screen, frames, frame_time, effect_type, background, transparent, collision)
        self.direction = self.validate_direction(direction)
        self.img = img
        self.shift_rate = max(1, int(shift_rate))
        self.loop = loop
        if self.img:
            self._set_img_attributes()

    def validate_direction(self, direction: PanRendererDirection) -> PanRendererDirection:
        if direction not in valid_pan_renderer_directions:
            raise InvalidPanRendererDirectionError(
                f"Invalid direction for PanRenderer. Please choose from {valid_pan_renderer_directions}"
            )
        return direction

    def _set_img_attributes(self) -> None:
        """Sets the attributes for the image given it exists."""
        self.render_image = True
        self.img_height = len(self.img)
        self.img_width = len(self.img[0])
        self.img_back = -self.img_width - 1
        self.img_front = -1
        self.img_top = (self.height - self.img_height) // 2
        self.img_bottom = ((self.height - self.img_height) // 2) + self.img_height
        self.current_img_x = self.img_back
        self.current_img_y = self.img_top

    @property
    def img_size(self) -> Tuple[int, int]:
        """Return the current image dimensions."""
        return len(self.img), len(self.img[0]) if self.img else (0, 0)

    def render_img_frame(self, frame_number: int) -> None:
        """Renders out the next frame of the pan animation."""
        if not self.loop and self.img_back > self.width + 1:
            return

        if self.direction == "horizontal":
            self.render_horizontal_frame(frame_number=frame_number)
        elif self.direction == "vertical":
            self.render_vertical_frame(frame_number=frame_number)

    def _set_padding(self, padding_vals: Tuple[int, int]) -> None:
        """Set the padding for the image [DEPRECATED FOR NOW]."""
        if not self.img or len(padding_vals) != 2:
            return

        left_right, top_bottom = padding_vals
        self.padding = (left_right, top_bottom)

        self.img = [" " * self.img_width for _ in range(top_bottom)]
        + [(" " * left_right) + line + (" " * left_right) for line in self.img]
        + [" " * self.img_width for _ in range(top_bottom)]

        self._set_img_attributes()

    def render_horizontal_frame(self, frame_number):
        """
        Renders the next image frame for a horizontal pan
        """
        if self.shift_rate > 0:
            if (
                0 <= frame_number <= self.img_width // self.shift_rate + 1
            ) or not self.loop:
                for y in range(self.height):
                    for x in range(self.width):
                        if (
                            x >= self.img_back
                            and x < self.img_front
                            and y >= self.img_top
                            and y < self.img_bottom
                        ):
                            if (
                                (y - self.img_top) >= 0
                                and (y - self.img_bottom) < self.img_height
                                and (x - self.img_back) >= 0
                                and (x - self.img_back) < self.img_width
                            ):
                                if self.transparent:
                                    if (
                                        self.img[y - self.img_top][x - self.img_back]
                                        == " "
                                    ):
                                        self.image_buffer.put_char(x, y, None)
                                    else:
                                        self.image_buffer.put_char(
                                            x,
                                            y,
                                            self.img[y - self.img_top][
                                                x - self.img_back
                                            ],
                                        )
                                else:
                                    self.image_buffer.put_char(
                                        x,
                                        y,
                                        self.img[y - self.img_top][x - self.img_back],
                                    )
                        else:
                            self.image_buffer.put_char(x, y, None)
                if self.loop:
                    if self.img_front >= self.width:
                        self.img_front = 0
                    else:
                        self.img_front += self.shift_rate
                    if self.img_back >= self.width:
                        self.img_back = 0
                    else:
                        self.img_back += self.shift_rate
                else:
                    self.img_back += self.shift_rate
                    self.img_front += self.shift_rate
            else:
                self.image_buffer.shift(-self.shift_rate)
        else:
            pass

    def render_vertical_frame(self, frame_number):
        pass
