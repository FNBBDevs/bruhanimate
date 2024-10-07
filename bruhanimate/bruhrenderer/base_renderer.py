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
from ..bruhutil.bruherrors import InvalidEffectTypeError
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
        self.back_buffer = self.create_buffer()
        self.front_buffer = self.create_buffer()

        self.exit_messages = {
            "msg1": " Frames Are Done ",
            "msg2": "   Press Enter   ",
            "centered": True,
            "wipe": False,
            "x_loc": 0,
            "y_loc": 1,
        }

    def validate_effect_type(self, effect_type: EffectType):
        """Validate the effect type against available effects."""
        if effect_type not in valid_effect_types:
            raise InvalidEffectTypeError(f"'{effect_type}' is not a valid effect. Please choose from {valid_effect_types}")

    def create_effect(self, effect_type: EffectType):
        """Create an effect instance based on the specified type."""
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
            return ChatbotEffect(self.screen, self.create_buffer(), self.create_buffer(), self.background)

    def create_buffer(self) -> Buffer:
        return Buffer(height=self.screen.height, width=self.screen.width)

    def update_collision(self, collision):
        """Update collision for specific effects."""
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
        except Exception:
            self.effect.update_collision(None, None, None, None, collision, None)

    def update_smart_transparent(self, smart_transparent: bool):
        """Enable/Disable the smart transparency effect."""
        self.smart_transparent = smart_transparent
        self.effect.smart_transparent = smart_transparent

    def push_front_to_screen(self):
        """Pushes changes from front_buffer to the screen."""
        for y, x, val in self.front_buffer.get_buffer_changes(self.back_buffer):
            self.screen.print_at(val, x, y, 1)

    def render_exit(self):
        """Renders the exit prompt to the screen."""
        if self.exit_messages['wipe']:
            self.back_buffer.clear_buffer()
        if self.exit_messages['centered']:
            self.back_buffer.put_at_center(self.height // 2 - 1, self.exit_messages['msg1'])
            self.back_buffer.put_at_center(self.height // 2, self.exit_messages['msg2'])
        else:
            self.back_buffer.put_at(self.exit_messages['x_loc'], self.exit_messages['y_loc'] - 1, self.exit_messages['msg1'], transparent=False)
            self.back_buffer.put_at(self.exit_messages['x_loc'], self.exit_messages['y_loc'], self.exit_messages['msg2'], transparent=False)

    def run(self, end_message=True):
        """Main loop for rendering frames."""
        try:
            if self.frames != INF:
                for frame in range(self.frames):
                    if self.screen.has_resized():
                        raise Exception("The screen was resized.")
                    sleep(self.frame_time)
                    self.render_img_frame(frame)
                    self.effect.render_frame(frame)
                    self.back_buffer.sync_with(self.effect.buffer)
                    self.back_buffer.sync_over_top(self.image_buffer)
                    self.push_front_to_screen()
                    self.front_buffer.sync_with(self.back_buffer)
            else:
                frame = 0
                while True:
                    if self.screen.has_resized():
                        raise Exception("The screen was resized.")
                    sleep(self.frame_time)
                    self.render_img_frame(frame)
                    self.effect.render_frame(frame)
                    self.back_buffer.sync_with(self.effect.buffer)
                    self.back_buffer.sync_over_top(self.image_buffer)
                    self.push_front_to_screen()
                    self.front_buffer.sync_with(self.back_buffer)
                    frame += 1

            if end_message:
                self.render_exit()
                self.push_front_to_screen()
                if sys.platform == 'win32':
                    input()
        except KeyboardInterrupt:
            if end_message:
                self.render_exit()
                self.push_front_to_screen()
                if sys.platform == 'win32':
                    input()

    def update_exit_stats(
        self, msg1=None, msg2=None, wipe=None, x_loc=None, y_loc=None, centered=False
    ):
        """Set the exit messages for when the animation finishes."""
        if msg1:
            self.exit_messages['msg1'] = msg1.replace("\n", "")
        if msg2:
            self.exit_messages['msg2'] = msg2.replace("\n", "")
        if wipe is not None:
            self.exit_messages['wipe'] = wipe
        if x_loc is not None and y_loc is not None:
            self.exit_messages['x_loc'], self.exit_messages['y_loc'] = x_loc, y_loc
        self.exit_messages['centered'] = centered

    @abstractmethod
    def render_frame(self):
        """To be defined by each renderer."""
