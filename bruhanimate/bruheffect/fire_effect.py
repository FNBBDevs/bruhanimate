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

import random
import math
from bruhcolor import bruhcolored as bc
from .base_effect import BaseEffect
from ..bruhutil.bruhffer import Buffer
from typing import List, Dict
import numpy as np


class FireEffect(BaseEffect):
    """
    Class for generating a dynamic fire effect with wind and color variations.
    Optimized for performance using numpy arrays and pre-computed values.
    """

    def __init__(self, buffer: Buffer, background: str):
        """
        Initializes the enhanced fire effect with a buffer and a background string.
        """
        super(FireEffect, self).__init__(buffer, background)
        self.ascii_chars = " .:-=+*#%@"
        self.color_map = [232, 233, 234, 130, 166, 202, 196, 214, 220, 226]

        # Use numpy arrays instead of nested lists for better performance
        self.previous_data = np.zeros(
            (buffer.height(), buffer.width()), dtype=np.float32
        )
        self.current_data = np.zeros_like(self.previous_data)

        # Pre-compute color mappings
        self.char_intensity_map = np.linspace(0, 255, len(self.ascii_chars))
        self.color_intensity_map = np.linspace(0, 255, len(self.color_map))

        # Initialize parameters
        self.fire_intensity = 0.2
        self.swell = False
        self.swell_delta = 0.01
        self.swell_halt = 1
        self.use_char_color = False
        self.background_color = False
        self.wind_direction = 0.0
        self.wind_strength = 0.0
        self.turbulence = 0.0
        self.heat_spots: List[Dict] = []
        self.heat_spot_intensity = 0.1

        # Pre-compute random variations for better performance
        self._random_variations = np.random.uniform(0.8, 1.2, (buffer.width(),))
        self._update_random_variations_counter = 0

    def set_fire_ascii_chars(self, ascii_chars: str):
        """
        Set the ASCII characters used for the fire effect.

        This method allows customization of the ASCII character set used to represent
        different intensity levels of the fire effect, enabling various visual styles.

        Args:
            ascii_chars (str): A string of exactly 10 characters that represent 
                               different intensity levels of the fire effect. 
                               Each character corresponds to increasing intensity 
                               from low to high.

        Returns:
            None: Returns nothing, but updates the ascii_chars attribute if the
                  provided string is valid.
        Note:
            The provided `ascii_chars` string must be exactly 10 characters long.
            If it is not, the method will return without making any changes.
        """
        if len(ascii_chars) != 10:
            return
        self.ascii_chars = ascii_chars

    def set_fire_intensity(self, fire_intensity: float):
        """
        Sets the intensity of the fire effect.
        
        Args:
            fire_intensity (float): A value between 0 and 1 representing the 
                                     intensity of the fire effect. Higher values 
                                     result in a more intense fire.
        
        Returns:
            None: Returns nothing, but updates the fire_intensity attribute if the
                  provided value is valid.
        """
        if 0 <= fire_intensity <= 1:
            self.fire_intensity = fire_intensity

    def set_fire_wind(self, direction: float, strength: float):
        """
        Sets wind parameters for the fire effect.

        Args:
            direction (float): The angle of the wind in degrees (0-360).
            strength (float): The strength of the wind, ranging from 0.0 to 1.0.

        Returns:
            None: Updates the wind_direction and wind_strength attributes.
        """
        self.wind_direction = math.radians(direction)
        self.wind_strength = max(0.0, min(1.0, strength))

    def set_fire_use_char_color(self, use_char_color: bool):
        """
        Enables or disables the use of character color for the fire effect.

        Args:
            use_char_color (bool): A boolean indicating whether to use character color.
        
        Returns:
            None: Updates the use_char_color attribute.
        """
        self.use_char_color = use_char_color

    def set_fire_background_color(self, background_color: bool):
        """
        Enables or disables the background color for the fire effect.

        Args:
            background_color (bool): A boolean indicating whether to show the background color.
        
        Returns:
            None: Updates the background_color attribute.
        """
        self.background_color = background_color

    def set_fire_swell(self, swell: bool, swell_halt: int = 1):
        """
        Controls the swell effect for the fire.

        Args:
            swell (bool): A boolean indicating whether to enable swell.
            swell_halt (int): The number of steps to halt swell before restarting.
        
        Returns:
            None: Updates the swell attribute and sets the initial swell delta.
        """
        self.swell = swell
        self.swell_halt = swell_halt

    def set_fire_turbulence(self, turbulence: float):
        """
        Sets how chaotic the fire behaves.

        Args:
            turbulence (float): A value between 0.0 and 1.0 representing the level of chaos.
        
        Returns:
            None: Updates the turbulence attribute.
        Note:
            Values closer to 0.0 result in less chaotic behavior, while values close to 1.0 result in more chaos.
        """
        self.turbulence = max(0.0, min(1.0, turbulence))

    def set_fire_heat_spot_intensity(self, heat_spot_intensity: float):
        """
        Sets the intensity of heat spots for the fire effect.

        Args:
            heat_spot_intensity (float): A value between 0 and 1 representing the intensity 
                                         of heat spots. Higher values result in more intense heat spots.
        
        Returns:
            None: Updates the heat_spot_intensity attribute if the provided value is valid.
        """
        self.heat_spot_intensity = max(0.0, min(1.0, heat_spot_intensity))

    def get_colored_char(self, intensity: float, max_intensity: float = 255.0) -> str:
        """
        Returns a colored character for the fire effect based on its intensity.

        Args:
            intensity (float): The intensity of the fire at this location.
            max_intensity (float): The maximum possible intensity of the fire effect.

        Returns:
            str: A string representing the colored character to display at this location.
        """
        # Adjust intensity with small random variation
        intensity_variation = intensity * (1 + random.uniform(-0.1, 0.1))
        intensity_variation = max(0, min(intensity_variation, max_intensity))

        # Calculate char index based on intensity
        char_index = int(
            (intensity_variation / max_intensity) * (len(self.ascii_chars) - 1)
        )
        char_index = min(
            char_index, len(self.ascii_chars) - 1
        )  # Ensure we don't exceed array bounds

        if self.ascii_chars[char_index] == " ":
            return " "

        # Calculate color index
        color_index = int(
            (intensity_variation / max_intensity) * (len(self.color_map) - 2)
        )
        color_index = min(
            color_index, len(self.color_map) - 2
        )  # Ensure we don't exceed array bounds

        # Add random sparkles
        if random.random() < 0.01 and intensity > max_intensity * 0.7:
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
        Updates the fire effect data for the current frame.

        Args:
            frame_number (int): The number of the current frame.
        
        Returns:
            None: This method does not return any value.
        """
        # Calculate wind effect
        wind_x = (
            math.cos(self.wind_direction + math.sin(frame_number * 0.05) * 0.2)
            * self.wind_strength
        )
        wind_offset_x = int(wind_x * 2)

        # Use numpy operations for spreading calculations
        height, width = self.buffer.height(), self.buffer.width()

        # Create shifted arrays for spreading
        left = np.roll(self.previous_data, -1, axis=1)
        right = np.roll(self.previous_data, 1, axis=1)
        up = np.roll(self.previous_data, -1, axis=0)
        down = np.roll(self.previous_data, 1, axis=0)

        # Calculate base values
        base_values = (left + right + up + down) / 4.0

        # Apply wind offset
        if wind_offset_x != 0:
            base_values = np.roll(base_values, wind_offset_x, axis=1)

        # Apply turbulence
        if self.turbulence > 0:
            turbulence_factor = np.random.uniform(
                1 - self.turbulence, 1 + self.turbulence, base_values.shape
            )
            base_values *= turbulence_factor

        # Update current data with cooling effect
        self.current_data[:-1, :] = base_values[1:, :] * 0.95

        # Add random intensity boosts (reduced frequency)
        if frame_number % 5 == 0:
            boost_mask = np.random.random(self.current_data.shape) < 0.001
            self.current_data[boost_mask] *= np.random.uniform(1.2, 1.5)

        # Update heat spots
        if random.random() < self.heat_spot_intensity:
            self.heat_spots.append(
                {
                    "x": random.randint(0, self.buffer.width() - 1),
                    "y": random.randint(
                        self.buffer.height() - 3, self.buffer.height() - 1
                    ),
                    "intensity": random.uniform(0.5, 1.0),
                    "lifetime": random.randint(5, 15),
                    "y_offset": 0.0,
                }
            )

        new_heat_spots = []
        for spot in self.heat_spots:
            if spot["lifetime"] > 0:
                x, y = spot["x"], int(spot["y"])
                if 0 <= x < self.buffer.width() and 0 <= y < self.buffer.height():
                    self.current_data[y, x] = max(
                        self.current_data[y, x], 255 * spot["intensity"]
                    )
                spot["lifetime"] -= 1
                spot["y_offset"] += random.uniform(0, 0.5)
                spot["y"] = max(0, spot["y"] - int(spot["y_offset"]))
                new_heat_spots.append(spot)
        self.heat_spots = new_heat_spots

        # Swap buffers
        self.previous_data, self.current_data = (
            self.current_data.copy(),
            self.previous_data,
        )

    def add_new_fire_row(self, frame_number: int):
        """
        Adds a new row to the fire effect.

        Args:
            frame_number (int): The number of the current frame.
        
        Returns:
            None: This method does not return any value.
        """
        # Update random variations periodically
        if self._update_random_variations_counter % 10 == 0:
            self._random_variations = np.random.uniform(
                0.8, 1.2, (self.buffer.width(),)
            )
        self._update_random_variations_counter += 1

        # Calculate base intensities
        x_values = np.arange(self.buffer.width())
        base_intensities = self.fire_intensity * (
            1 + 0.3 * np.sin(x_values / 5 + frame_number * 0.1)
        )
        base_intensities *= self._random_variations

        # Set new fire row
        random_values = np.random.random(self.buffer.width())
        self.current_data[-1, :] = np.where(random_values < base_intensities, 255, 0)

    def render_frame(self, frame_number: int):
        """
        Renders the current frame of the fire effect.

        Args:
            frame_number (int): The number of the current frame.
        
        Returns:
            None: This method does not return any value.
        """
        self.update_data(frame_number)

        # Ensure intensities are properly clipped
        intensities = np.clip(self.current_data, 0, 255)

        # Update buffer
        for y in range(self.buffer.height()):
            for x in range(self.buffer.width()):
                colored_char = self.get_colored_char(intensities[y, x])
                self.buffer.put_char(x, y, colored_char)

        self.add_new_fire_row(frame_number)

        if self.swell and frame_number % self.swell_halt == 0:
            if self.fire_intensity >= 1.0:
                self.swell_delta = -0.01
            elif self.fire_intensity <= 0.1:
                self.swell_delta = 0.01
            self.fire_intensity += self.swell_delta
