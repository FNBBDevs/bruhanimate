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

from bruhcolor import bruhcolored
from .base_renderer import BaseRenderer

class BackgroundColorRenderer(BaseRenderer):
    def __init__(
        self,
        screen,
        frames,
        time,
        img,
        on_color_code,
        effect_type="static",
        background=" ",
        transparent=False,
    ):
        super(BackgroundColorRenderer, self).__init__(
            screen, frames, time, effect_type, background, transparent
        )

        self.img = img
        self.img_height = len(self.img)
        self.img_width = len(self.img[0])
        self.img_y_start = (self.height - len(self.img)) // 2
        self.img_x_start = (self.width - len(self.img[0])) // 2
        self.current_img_x = self.img_x_start
        self.current_img_y = self.img_y_start

        if not on_color_code:
            raise Exception("a color code must be provided to BackgroundColorRenderer")
        if (
            not isinstance(on_color_code, int)
            or on_color_code < 0
            or on_color_code > 255
        ):
            raise Exception("the color code must be an int value 0-255")
        self.on_color_code = on_color_code

    def render_img_frame(self, frame_number):
        for y in range(self.height):
            for x in range(self.width):
                if (
                    (y >= self.img_y_start)
                    and (y < (self.img_y_start + self.img_height))
                    and (x >= self.img_x_start)
                    and (x < (self.img_x_start + self.img_width))
                ):
                    self.image_buffer.put_char(
                        x,
                        y,
                        bruhcolored(
                            self.img[y - self.img_y_start][x - self.img_x_start],
                            on_color=self.on_color_code,
                        ).colored,
                    )
