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
    Renders a full-screen effect with no image overlay.
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
        super().__init__(
            screen, frames, frame_time, effect_type, background, transparent
        )

    def render_img_frame(self, frame_number: int):
        pass
