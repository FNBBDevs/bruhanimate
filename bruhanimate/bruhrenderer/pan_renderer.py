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

from typing import List, Tuple

from ..bruhutil import Screen
from ..bruhutil.bruherrors import InvalidPanRendererDirectionError
from ..bruhutil.bruhtypes import (
    EffectType,
    PanRendererDirection,
    valid_pan_renderer_directions,
)
from .base_renderer import BaseRenderer


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
        super().__init__(
            screen, frames, frame_time, effect_type, background, transparent, collision
        )
        self.direction = self.validate_direction(direction)
        self.img = img
        self.shift_rate = max(1, int(shift_rate))
        self.loop = loop
        if self.img:
            self._set_img_attributes()

    def validate_direction(
        self, direction: PanRendererDirection
    ) -> PanRendererDirection:
        """
        Validates the given direction to ensure it is one of the valid pan renderer directions.

        Args:
            direction (PanRendererDirection): The direction to be validated.

        Returns:
            PanRendererDirection: The validated direction.

        Raises:
            InvalidPanRendererDirectionError: If the given direction is not a valid pan renderer direction.
        """
        if direction not in valid_pan_renderer_directions:
            raise InvalidPanRendererDirectionError(
                f"Invalid direction for PanRenderer. Please choose from {valid_pan_renderer_directions}"
            )
        return direction

    def _set_img_attributes(self) -> None:
        """
        Sets attributes related to the image, including whether to render it, its height and width,
        and its initial position on the screen.
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

    @property
    def img_size(self) -> Tuple[int, int]:
        """
        Gets the size of the image.

        Returns:
            A tuple containing the height and width of the image. If the image is None or empty,
            returns (0, 0).
        """
        return len(self.img), len(self.img[0]) if self.img else (0, 0)

    def render_img_frame(self, frame_number: int) -> None:
        """
        Renders a single frame of the image.

        Args:
            frame_number: The current frame number.
        """
        if not self.loop and self.img_back > self.width + 1:
            return

        if self.direction == "horizontal":
            self.render_horizontal_frame(frame_number=frame_number)
        elif self.direction == "vertical":
            self.render_vertical_frame(frame_number=frame_number)

    def _set_padding(self, padding_vals: Tuple[int, int]) -> None:
        """
        Sets the image's padding based on the provided values.

        Args:
            padding_vals (Tuple[int, int]): A tuple containing two integers representing the left/right and top/bottom padding.

        Returns:
            None

        Raises:
            ValueError: If the provided padding value is invalid or if no image has been set.
        """
        if not self.img or len(padding_vals) != 2:
            return
        left_right, top_bottom = padding_vals
        self.padding = (left_right, top_bottom)

        # Create a new image with the desired padding
        self.img = [" " * self.img_width for _ in range(top_bottom)]
        +[(" " * left_right) + line + (" " * left_right) for line in self.img]
        +[" " * self.img_width for _ in range(top_bottom)]

        # Update the image attributes to reflect the new padding
        self._set_img_attributes()

    def render_horizontal_frame(self, frame_number):
        """
        Renders a horizontal frame of the image.

        Args:
            frame_number: The current frame number.
        """
        if self.shift_rate > 0:
            # Calculate the number of frames to render
            num_frames = (self.img_width // self.shift_rate) + 1

            # Check if we're in loop mode or have reached the end of the image
            if not self.loop or frame_number >= num_frames:
                return

            # Update the image position based on the shift rate and current frame number
            new_img_back = -self.img_width - (frame_number * self.shift_rate)
            new_img_front = frame_number * self.shift_rate

            # Render each row of the image at its new position
            for y in range(self.height):
                for x in range(self.width):
                    if (
                        x >= new_img_back
                        and x < new_img_front
                        and y >= self.img_top
                        and y < self.img_bottom
                    ):
                        # Check if we're within the bounds of the image
                        if self.img_height > 0 and self.img_width > 0:
                            img_row = self.img[y - self.img_top]

                            # Check if each pixel in the row is within the bounds of the image
                            for j, pixel in enumerate(img_row):
                                if x - new_img_back >= j:
                                    # Put the pixel into the screen buffer at its new position
                                    if self.transparent:
                                        if (
                                            y == self.img_top + (self.img_height // 2)
                                            and x - new_img_back == 0
                                        ) or self.img[y - self.img_top][j] != " ":
                                            self.image_buffer.put_char(x, y, pixel)
                                    else:
                                        self.image_buffer.put_char(x, y, pixel)

            # Update the image buffer to reflect the updated position of the image
            self.image_buffer.shift(self.shift_rate)

        return

    def render_vertical_frame(self, frame_number):
        """
        Renders a vertical frame of the image.

        Args:
            frame_number: The current frame number.
        """
        if self.shift_rate > 0:
            # Calculate the number of frames to render
            num_frames = (self.img_height // self.shift_rate) + 1

            # Check if we're in loop mode or have reached the end of the image
            if not self.loop and frame_number >= num_frames:
                return

            # Update the image position based on the shift rate and current frame number
            new_img_top = -self.img_height - (frame_number * self.shift_rate)
            new_img_bottom = frame_number * self.shift_rate

            # Render each column of the image at its new position
            for x in range(self.width):
                for y in range(self.height):
                    if (
                        y >= new_img_top
                        and y < new_img_bottom
                        and x >= self.img_back
                        and x < self.img_front
                    ):
                        # Check if we're within the bounds of the image
                        if self.img_height > 0 and self.img_width > 0:
                            column_index = x - self.img_back

                            # Check if each pixel in the column is within the bounds of the image
                            img_column = [
                                self.img[j][column_index]
                                for j in range(self.img_height)
                            ]
                            for i, pixel in enumerate(img_column):
                                if y - new_img_top >= i:
                                    # Put the pixel into the screen buffer at its new position
                                    if self.transparent:
                                        if self.img[i][column_index] != " ":
                                            self.image_buffer.put_char(x, y, pixel)
                                    else:
                                        self.image_buffer.put_char(x, y, pixel)

            # Update the image buffer to reflect the updated position of the image
            self.image_buffer.shift_vertical(self.shift_rate)

        return
