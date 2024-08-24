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

from abc import abstractmethod


class BaseEffect:
    """
    Class for keeping track of an effect, and updataing it's buffer
    """

    def __init__(self, buffer, background):
        self.buffer = buffer
        self.background = background
        self.background_length = len(background)

    @abstractmethod
    def render_frame(self, frame_number):
        """
        To be defined by each effect
        """