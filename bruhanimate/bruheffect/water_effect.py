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

from .base_effect import BaseEffect
from ..bruhutil.bruhffer import Buffer



class WaterEffect(BaseEffect):
    """
    Class for generating a water effect.
    """

    def __init__(self, buffer: Buffer, background: str):
        """
        Initializes the water effect with a buffer and a background string.

        Args:
            buffer (Buffer): Effect buffer to push updates to.
            background (str): character or string to use as the background.
        """
        super(WaterEffect, self).__init__(buffer, background)

    def render_frame(self, frame_number: int):
        """
        Renders the water to the screen.

        Args:
            frame_number (int): The current frame number.
        """
        pass

