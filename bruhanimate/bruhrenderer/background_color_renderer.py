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

from typing import Any

from bruhcolor import bruhcolored

from ..bruhutil.bruhtypes import EffectType
from .base_renderer import BaseRenderer


class BackgroundColorRenderer(BaseRenderer):
    """
    Renders ASCII art centered on screen with a solid ANSI background color.

    Args:
        screen: The screen object to render to.
        img (list[str]): ASCII art as a list of strings.
        frames (int): Number of frames to render. Defaults to 100.
        frame_time (float): Seconds between frames. Defaults to 0.1.
        effect_type (EffectType): Background effect. Defaults to "static".
        background (str): Background fill character. Defaults to " ".
        transparent (bool): Whether to apply transparency. Defaults to False.
        collision (bool): Whether to enable collision detection. Defaults to False.
        on_color_code (int): ANSI 256-color code (0–255) for the background. Defaults to 27.
        settings: Optional settings dataclass to configure the effect.
        preset: Optional named preset registered for the effect.
    """

    def __init__(
        self,
        screen,
        img: list[str],
        frames: int = 100,
        frame_time: float = 0.1,
        effect_type: EffectType = "static",
        background: str = " ",
        transparent: bool = False,
        collision: bool = False,
        on_color_code: int = 27,
        settings: Any = None,
        preset: str | None = None,
    ):
        super().__init__(
            screen,
            frames,
            frame_time,
            effect_type,
            background,
            transparent,
            collision,
            settings=settings,
            preset=preset,
        )

        if not on_color_code:
            raise ValueError("a color code must be provided to BackgroundColorRenderer")
        if (
            not isinstance(on_color_code, int)
            or on_color_code < 0
            or on_color_code > 255
        ):
            raise ValueError("the color code must be an int value 0-255")

        self.img = img
        self.img_height = len(self.img)
        self.img_width = len(self.img[0])
        self.img_y_start = (self.height - self.img_height) // 2
        self.img_x_start = (self.width - self.img_width) // 2
        self.current_img_x = self.img_x_start
        self.current_img_y = self.img_y_start
        self.on_color_code = on_color_code

    def render_img_frame(self, frame_number: int):
        """
        Applies the background color to each image character on frame 0 only.
        Subsequent frames reuse the already-colored image buffer unchanged.
        """
        if frame_number != 0:
            return

        for y in range(self.img_y_start, self.img_y_start + self.img_height):
            for x in range(self.img_x_start, self.img_x_start + self.img_width):
                self.image_buffer.put_char(
                    x,
                    y,
                    bruhcolored(
                        self.img[y - self.img_y_start][x - self.img_x_start],
                        on_color=self.on_color_code,
                    ).colored,
                )
