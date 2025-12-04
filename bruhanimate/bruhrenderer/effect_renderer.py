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

from ..bruhutil import Screen
from ..bruhutil.bruhtypes import EffectType
from .base_renderer import BaseRenderer


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

    def render_img_frame(self, frame_number: int):
        """
        No-op implementation since EffectRenderer doesn't render images.

        Args:
            frame_number (int): The current frame number.

        Returns:
            None
        """
        pass  # EffectRenderer doesn't need to render images

    def render_effect_frame(self, frame_number: int):
        """
        Renders a single frame of the effect.
        This method is kept for backwards compatibility but isn't needed
        since the base renderer handles effect rendering automatically.

        Args:
            frame_number (int): The current frame number.

        Returns:
            None
        """
        self.effect.render_frame(frame_number)
