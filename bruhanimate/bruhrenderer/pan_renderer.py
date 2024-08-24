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

from ..bruhutil import Screen, VERTICAL, HORIZONTAL
from .base_renderer import BaseRenderer

class PanRenderer(BaseRenderer):
    """
    A renderer to pan an image across the screen.
    Update the image_buffer only.
    """

    def __init__(
        self,
        screen: Screen,
        img: list[str],
        frames: int,
        time: float,
        effect_type: str = "static",
        background: str = " ",
        transparent: bool = False,
        direction: str = "h",
        shift_rate: int = 1,
        loop: bool = False,
    ):
        super(PanRenderer, self).__init__(
            screen, frames, time, effect_type, background, transparent
        )

        self.direction = direction if direction and direction in ["h", "v"] else "h"
        self.img = img
        self.shift_rate = int(shift_rate)
        self.loop = loop
        if self.img:
            self._set_img_attributes()

    def _set_img_attributes(self):
        """
        Sets the attributes for the image given it exists
        """
        self.render_image = True
        self.img_height = len(self.img)
        self.img_width = len(self.img[0])
        self.img_back = -self.img_width - 1
        self.img_front = -1
        self.img_top = (self.height - self.img_height) // 2
        self.img_bottom = ((self.height - self.img_height) // 2) + self.img_height
        self.current_img_x = self.img_back
        self.current_img_y = self.img_top

    def _set_padding(self, padding_vals):
        """
        Set the padding for the image [DEPRECATED FOR NOW]
        :param padding_vals: vals for padding [left-right, top-bottom]
        """
        if not self.img:
            return

        if len(padding_vals) == 2:
            self.padding = padding_vals

        left_right = self.padding[0]
        top_bottom = self.padding[1]
        if left_right > 0 or top_bottom > 0:
            tmp = []
            for _ in range(top_bottom):
                tmp.append(" " * self.img_width)
            for line in self.img:
                tmp.append(line)
            for _ in range(top_bottom):
                tmp.append(" " * self.img_width)

            for i in range(len(tmp)):
                tmp[i] = (" " * left_right) + tmp[i] + (" " * left_right)

            self.img = [line for line in tmp]
            self._set_img_attributes()

    def render_img_frame(self, frame_number):
        """
        Renders out the next frame of the pan animation,
        if there is no image passed into the renderer then
        the background is rendered on it's own
        """
        if not self.loop:
            if self.img_back > self.width + 1:
                return
        if self.direction == HORIZONTAL:
            self.render_horizontal_frame(frame_number)
        elif self.direction == VERTICAL:
            self.render_veritcal_frame()

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

