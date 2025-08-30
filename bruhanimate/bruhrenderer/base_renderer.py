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

import sys
from typing import Literal, TypeVar, Dict, Generic
from abc import abstractmethod
from ..bruheffect import *
from ..bruhutil.utils import sleep
from ..bruhutil.bruhffer import Buffer
from ..bruhutil.bruhscreen import Screen
from ..bruhutil.bruherrors import InvalidEffectTypeError, ScreenResizedError
from ..bruhutil.bruhtypes import EffectType, valid_effect_types


HORIZONTAL = "h"
VERTICAL = "v"
INF = float("inf")


class BaseRenderer:
    """
    Base class for rendering effects on the screen.
    """

    def __init__(
        self,
        screen: Screen,
        frames: int = 100,
        frame_time: float = 0.1,
        effect_type: EffectType = "static",
        background: str = " ",
        transparent: bool = False,
        collision: bool = False,
    ):
        self.validate_effect_type(effect_type)

        self.screen = screen
        self.frames = frames
        self.frame_time = frame_time
        self.effect_type = effect_type
        self.transparent = transparent
        self.background = background
        self.height = screen.height
        self.width = screen.width
        self.smart_transparent = False
        self.collision = collision

        self.effect = self.create_effect(effect_type)
        self.image_buffer = self.create_buffer().clear_buffer(val=None)

        self.buffer_a = self.create_buffer()
        self.buffer_b = self.create_buffer()
        self.current_buffer = self.buffer_a
        self.display_buffer = self.buffer_b

        self.last_displayed = self.create_buffer()

        self.exit_messages = {
            "msg1": " Frames Are Done ",
            "msg2": "   Press Enter   ",
            "centered": True,
            "wipe": False,
            "x_loc": 0,
            "y_loc": 1,
        }

    def swap_buffers(self):
        """
        Swaps the front and back buffers - the core of double buffering.
        This makes the completed back buffer visible and gives us a new back buffer to draw to.

        Returns:
            None
        """
        # Atomic buffer swap
        self.current_buffer, self.display_buffer = (
            self.display_buffer,
            self.current_buffer,
        )

    def present_frame(self):
        """
        Presents the current display buffer to the screen.
        Only updates screen positions that have actually changed for efficiency.

        Returns:
            None
        """
        # Only update screen positions where the display buffer differs from what was last shown
        for y, x, val in self.last_displayed.get_buffer_changes(self.display_buffer):
            self.screen.print_at(val, x, y, 1)

        # Track what we just displayed
        self.last_displayed.sync_with(self.display_buffer)

    def clear_back_buffer(self):
        """
        Clears the back buffer (current drawing buffer) for the next frame.

        Returns:
            None
        """
        self.current_buffer.clear_buffer(val=self.background)

    def render_to_back_buffer(self, frame: int):
        """
        Renders the current frame to the back buffer.
        This is where all drawing operations happen before presentation.

        Args:
            frame (int): The current frame number.

        Returns:
            None
        """
        # Clear the back buffer
        self.clear_back_buffer()

        # Render the effect to its own buffer
        self.effect.render_frame(frame)

        # Composite the effect buffer onto the back buffer
        self.current_buffer.sync_with(self.effect.buffer)

        # Render the image frame if needed
        self.render_img_frame(frame)

        # Overlay the image buffer on top (respecting transparency)
        self.current_buffer.sync_over_top(self.image_buffer)

    def validate_effect_type(self, effect_type: EffectType) -> None:
        """
        Validates the provided effect type against a list of valid effect types.

        Args:
            effect_type (EffectType): The effect type to be validated.

        Raises:
            InvalidEffectTypeError: If the provided effect type is not valid.
        """
        if effect_type not in valid_effect_types:
            raise InvalidEffectTypeError(
                f"'{effect_type}' is not a valid effect. Please choose from {valid_effect_types}"
            )

    def create_effect(self, effect_type: EffectType) -> object:
        """
        Creates an instance of the specified effect type.

        Args:
            effect_type (EffectType): The type of effect to be created.

        Returns:
            An instance of the specified effect type.

        Raises:
            ValueError: If the provided effect type is not recognized.
        """
        if effect_type == "static":
            return StaticEffect(self.create_buffer(), self.background)
        elif effect_type == "offset":
            return OffsetEffect(self.create_buffer(), self.background)
        elif effect_type == "noise":
            return NoiseEffect(self.create_buffer(), self.background)
        elif effect_type == "stars":
            return StarEffect(self.create_buffer(), self.background)
        elif effect_type == "plasma":
            return PlasmaEffect(self.create_buffer(), self.background)
        elif effect_type == "gol":
            return GameOfLifeEffect(self.create_buffer(), self.background)
        elif effect_type == "rain":
            return RainEffect(self.create_buffer(), self.background)
        elif effect_type == "matrix":
            return MatrixEffect(self.create_buffer(), self.background)
        elif effect_type == "drawlines":
            return DrawLinesEffect(self.create_buffer(), self.background)
        elif effect_type == "snow":
            return SnowEffect(self.create_buffer(), self.background)
        elif effect_type == "twinkle":
            return TwinkleEffect(self.create_buffer(), self.background)
        elif effect_type == "audio":
            return AudioEffect(self.create_buffer(), self.background)
        elif effect_type == "chat":
            return ChatbotEffect(
                self.screen, self.create_buffer(), self.create_buffer(), self.background
            )
        elif effect_type == "firework":
            return FireworkEffect(self.create_buffer(), self.background)
        elif effect_type == "fire":
            return FireEffect(self.create_buffer(), self.background)
        elif effect_type == "julia":
            return JuliaEffect(self.create_buffer(), self.background)

    def create_buffer(self) -> Buffer:
        """
        Creates a new buffer with the specified height and width.

        Args:

        Returns:
            A newly created buffer object.
        """
        return Buffer(height=self.screen.height, width=self.screen.width)

    def update_collision(self, collision: bool):
        """
        Updates the effect's collision state.

        Args:
            collision (bool): The new collision state.

        Returns:
            None
        """
        try:
            self.collision = collision
            self.effect.update_collision(
                self.current_img_x,
                self.current_img_y,
                self.img_width,
                self.img_height,
                collision,
                self.smart_transparent,
                self.image_buffer,
            )
        except Exception as e:
            print(f"base_renderer: update_collision: warning: {e}")
            self.effect.update_collision(None, None, None, None, collision, None)

    def update_smart_transparent(self, smart_transparent: bool):
        """
        Updates the effect's smart transparent state.

        Args:
            smart_transparent (bool): The new smart transparent state.

        Returns:
            None
        """
        self.smart_transparent = smart_transparent
        self.effect.smart_transparent = smart_transparent

    def render_exit_to_back_buffer(self):
        """
        Renders the exit message to the back buffer following double buffering principles.

        Returns:
            None
        """
        if self.exit_messages["wipe"]:
            self.current_buffer.clear_buffer()
        else:
            self.current_buffer.sync_with(self.display_buffer)

        if self.exit_messages["centered"]:
            center_y1 = self.height // 2 - 1
            center_y2 = self.height // 2

            self.current_buffer.put_at_center(center_y1, self.exit_messages["msg1"])
            self.current_buffer.put_at_center(center_y2, self.exit_messages["msg2"])
        else:
            self.current_buffer.put_at(
                self.exit_messages["x_loc"],
                self.exit_messages["y_loc"] - 1,
                self.exit_messages["msg1"],
                transparent=False,
            )
            self.current_buffer.put_at(
                self.exit_messages["x_loc"],
                self.exit_messages["y_loc"],
                self.exit_messages["msg2"],
                transparent=False,
            )

    def update_exit_stats(
        self, msg1=None, msg2=None, wipe=None, x_loc=None, y_loc=None, centered=False
    ):
        """
        Updates the exit message statistics.
        Args:
            msg1 (str): The first line of the exit message. Defaults to None.
            msg2 (str): The second line of the exit message. Defaults to None.
            wipe (bool): Whether to clear the screen before rendering the exit message. Defaults to False.
            x_loc (int): The x-coordinate of the exit message. Defaults to 0.
            y_loc (int): The y-coordinate of the exit message. Defaults to 1.
            centered (bool): Whether to center the exit message horizontally. Defaults to True.

        Returns:
            None
        """
        if msg1:
            self.exit_messages["msg1"] = msg1.replace("\n", "")
        if msg2:
            self.exit_messages["msg2"] = msg2.replace("\n", "")
        if wipe is not None:
            self.exit_messages["wipe"] = wipe
        if x_loc is not None and y_loc is not None:
            self.exit_messages["x_loc"], self.exit_messages["y_loc"] = x_loc, y_loc
        self.exit_messages["centered"] = centered

    def run(self, end_message=True):
        """
        Runs the renderer using proper double buffering.

        Args:
            end_message (bool): Whether to render an exit message after finishing. Defaults to True.

        Returns:
            None
        """
        try:
            # Initialize both buffers
            self.clear_back_buffer()
            self.display_buffer.clear_buffer(val=self.background)

            if self.frames != INF:
                for frame in range(self.frames):
                    if self.screen.has_resized():
                        raise ScreenResizedError("The screen was resized.")

                    # Render complete frame to back buffer
                    self.render_to_back_buffer(frame)

                    # Swap buffers (atomic operation)
                    self.swap_buffers()

                    # Present the now-front buffer to screen
                    self.present_frame()

                    # Wait for next frame
                    sleep(self.frame_time)
            else:
                frame = 0
                while True:
                    if self.screen.has_resized():
                        raise ScreenResizedError("The screen was resized.")

                    # Render complete frame to back buffer
                    self.render_to_back_buffer(frame)

                    # Swap buffers (atomic operation)
                    self.swap_buffers()

                    # Present the now-front buffer to screen
                    self.present_frame()

                    # Wait for next frame
                    sleep(self.frame_time)
                    frame += 1
        except KeyboardInterrupt:
            pass

        if end_message:
            self.render_exit_to_back_buffer()
            self.swap_buffers()
            self.present_frame()
            if sys.platform == "win32":
                input()

    @abstractmethod
    def render_frame(self):
        """
        Renders a single frame of the effect.

        Returns:
            None
        """
        # To be defined by each renderer
        pass
