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
from .base_renderer import BaseRenderer
from ..bruhutil import Screen, INF, sleep
from ..bruhutil.bruherrors import ScreenResizedError
from ..bruhutil.bruhtypes import EffectType


class EffectRenderer(BaseRenderer):
    """
    Class for rendering the Effect and only the Effect
    """

    def __init__(

        self,
        screen: Screen,
        frames: int = 100,
        frame_time: float = 0.1,
        effect_type: EffectType = "static",
        background: str = " ",
        transparent: bool = False,
    ):
        super(EffectRenderer, self).__init__(
            screen, frames, frame_time, effect_type, background, transparent
        )

        self.background = self.effect.background

    def render_effect_frame(self, frame_number: int):
        """
        Renders a single frame of the effect.

        Args:
            frame_number (int): The current frame number.

        Returns:
            None
        """
        self.effect.render_frame(frame_number)

    def run(self, end_message: bool = True):
        """
        Runs the effect renderer.

        Args:
            end_message (bool): Whether to render an exit message at the end. Defaults to True.

        Returns:
            None

        Raises:
            ScreenResizedError: If the screen is resized during rendering.
        """
        try:
            if self.frames == INF:
                frame = 0
                while True:
                    if self.screen.has_resized(): raise ScreenResizedError("An error was encounter. The Screen was resized.")
                    sleep(self.frame_time)
                    self.render_effect_frame(frame)
                    self.back_buffer.sync_with(self.effect.buffer)
                    self.push_front_to_screen()
                    self.front_buffer.sync_with(self.back_buffer)
                    frame += 1
            else:
                for frame in range(self.frames):
                    if self.screen.has_resized(): raise ScreenResizedError("An error was encounter. The Screen was resized.")
                    sleep(self.frame_time)
                    self.render_effect_frame(frame)
                    self.back_buffer.sync_with(self.effect.buffer)
                    self.push_front_to_screen()
                    self.front_buffer.sync_with(self.back_buffer)
            if end_message:
                self.render_exit()
                self.push_front_to_screen()
            if sys.platform == 'win32': input()
        except KeyboardInterrupt:
            if end_message:
                self.render_exit()
                self.push_front_to_screen()
            if sys.platform == 'win32': input()

        if end_message:
            self.render_exit()
            self.push_front_to_screen()
