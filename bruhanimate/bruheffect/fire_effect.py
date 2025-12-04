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

import math
import random
from typing import Dict, List

import numpy as np
from bruhcolor import bruhcolored as bc

from ..bruhutil.bruhffer import Buffer
from .base_effect import BaseEffect


class FireEffect(BaseEffect):
    """
    Class for generating a dynamic, improved fire effect with taller, rounder,
    and more visible flames using fuller ASCII characters.
    """

    def __init__(self, buffer: Buffer, background: str):
        """
        Initializes the enhanced fire effect with a buffer and a background string.
        """
        super(FireEffect, self).__init__(buffer, background)
        self.ascii_chars = " ░▒▓██████"
        self.color_map = [232, 160, 196, 202, 208, 214, 220, 226, 231, 15]

        self.previous_data = np.zeros(
            (buffer.height(), buffer.width()), dtype=np.float32
        )
        self.current_data = np.zeros_like(self.previous_data)

        # Values are closer to 1.0, so heat is retained longer as it rises.
        self.height_cooling_map = np.linspace(0.98, 0.92, buffer.height())[
            :, np.newaxis
        ]

        self.fire_intensity = 0.2
        self.swell = False
        self.swell_delta = 0.02
        self.swell_halt = 1
        self.use_char_color = False
        self.background_color = False
        self.wind_direction = 0.0
        self.wind_strength = 0.0
        self.turbulence = 0.0
        self.heat_spots: List[Dict] = []
        self.heat_spot_intensity = 0.1

        self._random_variations = np.random.uniform(0.8, 1.2, (buffer.width(),))
        self._update_random_variations_counter = 0

    def set_fire_ascii_chars(self, ascii_chars: str):
        """
        Set the ASCII characters used for the fire effect.
        """
        if len(ascii_chars) != 10:
            return
        self.ascii_chars = ascii_chars

    def set_fire_intensity(self, fire_intensity: float):
        """
        Sets the intensity of the fire effect.
        """
        if 0 <= fire_intensity <= 1:
            self.fire_intensity = fire_intensity

    def set_fire_wind(self, direction: float, strength: float):
        """
        Sets wind parameters for the fire effect.
        """
        self.wind_direction = math.radians(direction)
        self.wind_strength = max(0.0, min(1.0, strength))

    def set_fire_use_char_color(self, use_char_color: bool):
        """
        Enables or disables the use of character color for the fire effect.
        """
        self.use_char_color = use_char_color

    def set_fire_background_color(self, background_color: bool):
        """
        Enables or disables the background color for the fire effect.
        """
        self.background_color = background_color

    def set_fire_swell(self, swell: bool, swell_halt: int = 1):
        """
        Controls the swell effect for the fire.
        """
        self.swell = swell
        self.swell_halt = swell_halt

    def set_fire_turbulence(self, turbulence: float):
        """
        Sets how chaotic the fire behaves.
        """
        self.turbulence = max(0.0, min(1.0, turbulence))

    def set_fire_heat_spot_intensity(self, heat_spot_intensity: float):
        """
        Sets the intensity of heat spots for the fire effect.
        """
        self.heat_spot_intensity = max(0.0, min(1.0, heat_spot_intensity))

    def get_colored_char(self, intensity: float, max_intensity: float = 255.0) -> str:
        """
        Returns a colored character for the fire effect based on its intensity.
        """
        intensity_variation = intensity * (1 + random.uniform(-0.1, 0.1))
        intensity_variation = max(0, min(intensity_variation, max_intensity))

        char_index = int(
            (intensity_variation / max_intensity) * (len(self.ascii_chars) - 1)
        )
        char_index = min(char_index, len(self.ascii_chars) - 1)

        if intensity_variation < 1:
            return " "

        if self.ascii_chars[char_index] == " ":
            return " "

        color_index = int(
            (intensity_variation / max_intensity) * (len(self.color_map) - 2)
        )
        color_index = min(color_index, len(self.color_map) - 2)

        if random.random() < 0.04 and intensity > max_intensity * 0.9:
            color_index = len(self.color_map) - 1

        if self.background_color:
            return bc(text=" ", on_color=self.color_map[color_index]).colored
        elif self.use_char_color:
            return bc(
                text=self.ascii_chars[char_index], color=self.color_map[color_index]
            ).colored
        return self.ascii_chars[char_index]

    def update_data(self, frame_number: int):
        """
        Updates the fire effect data with logic for taller and rounder flames.
        """
        wind_x = (
            math.cos(self.wind_direction + math.sin(frame_number * 0.05) * 0.2)
            * self.wind_strength
        )
        wind_offset_x = int(wind_x * 2)

        _height, _width = self.buffer.height(), self.buffer.width()

        left = np.roll(self.previous_data, -1, axis=1)
        right = np.roll(self.previous_data, 1, axis=1)
        up = np.roll(self.previous_data, -1, axis=0)

        # The left and right weights are now higher, making the fire spread outwards more.
        # The divisor is the sum of the new weights (1.8 + 1.2 + 1.2 = 4.2)
        base_values = (up * 1.8 + left * 1.2 + right * 1.2) / 4.2

        if wind_offset_x != 0:
            base_values = np.roll(base_values, wind_offset_x, axis=1)

        if self.turbulence > 0:
            turbulence_factor = np.random.uniform(
                1 - self.turbulence, 1 + self.turbulence, base_values.shape
            )
            base_values *= turbulence_factor

        self.current_data[:-1, :] = base_values[1:, :] * self.height_cooling_map[:-1, :]

        if random.random() < self.heat_spot_intensity:
            self.heat_spots.append(
                {
                    "x": random.randint(0, self.buffer.width() - 1),
                    "y": random.randint(
                        self.buffer.height() - 3, self.buffer.height() - 1
                    ),
                    "intensity": random.uniform(0.5, 1.0),
                    "lifetime": random.randint(10, 20),
                    "y_offset": 0.0,
                    "x_offset": 0.0,
                }
            )

        new_heat_spots = []
        for spot in self.heat_spots:
            if spot["lifetime"] > 0:
                spot["y_offset"] += random.uniform(0, 0.5)
                spot["y"] = max(0, spot["y"] - int(spot["y_offset"]))
                spot["x_offset"] += random.uniform(-0.3, 0.3)
                spot["x"] += spot["x_offset"]

                x, y = int(spot["x"]), int(spot["y"])

                if 0 <= x < self.buffer.width() and 0 <= y < self.buffer.height():
                    self.current_data[y, x] = max(
                        self.current_data[y, x], 255 * spot["intensity"]
                    )

                spot["lifetime"] -= 1
                if spot["y"] > 0:
                    new_heat_spots.append(spot)
        self.heat_spots = new_heat_spots

        self.previous_data, self.current_data = (
            self.current_data.copy(),
            self.previous_data,
        )

    def add_new_fire_row(self, frame_number: int):
        """
        Adds a new row to the fire effect.
        """
        if self._update_random_variations_counter % 10 == 0:
            self._random_variations = np.random.uniform(
                0.8, 1.2, (self.buffer.width(),)
            )
        self._update_random_variations_counter += 1

        x_values = np.arange(self.buffer.width())
        base_intensities = self.fire_intensity * (
            1 + 0.3 * np.sin(x_values / 5 + frame_number * 0.1)
        )
        base_intensities *= self._random_variations

        random_values = np.random.random(self.buffer.width())
        self.current_data[-1, :] = np.where(random_values < base_intensities, 255, 0)

    def render_frame(self, frame_number: int):
        """
        Renders the current frame of the fire effect.
        """
        self.update_data(frame_number)

        intensities = np.clip(self.current_data, 0, 255)

        for y in range(self.buffer.height()):
            for x in range(self.buffer.width()):
                colored_char = self.get_colored_char(intensities[y, x])
                self.buffer.put_char(x, y, colored_char)

        self.add_new_fire_row(frame_number)

        if self.swell and frame_number % self.swell_halt == 0:
            if self.fire_intensity >= 1.0:
                self.swell_delta = -0.02  # Adjusted to match the new delta
            elif self.fire_intensity <= 0.1:
                self.swell_delta = 0.02  # Adjusted to match the new delta
            self.fire_intensity += self.swell_delta
