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
if sys.platform == "win32":
    import pyaudio
    import random

    import numpy as np

    from bruhcolor import bruhcolored
    from .base_effect import BaseEffect
    from ..bruhutil import Buffer


    class AudioEffect(BaseEffect):
        """
        A base class for audio effects in a terminal-based visualizer.  
        """
        def __init__(
            self, buffer: Buffer, background: str, num_bands: int = 24, audio_halt: int = 10
        ):
            """
            Initialize the AudioEffect class.

            Args:
                buffer (Buffer): The effect buffer to push updates to.
                background (str): Character or string to use for the background.
                num_bands (int, optional): Number of EQ bands to show. Defaults to 24.
                audio_halt (int, optional): How often we should update the bands, (frame_number % halt == 0 then update). Defaults to 10.
            """
            super(AudioEffect, self).__init__(buffer, background)
            self.FORMAT = pyaudio.paInt16
            self.CHANNELS = 1
            self.RATE = 44100
            self.CHUNK = 1024
            self.BANDS = num_bands + 1
            self.audio_halt = audio_halt
            self.bands = []
            self.p = pyaudio.PyAudio()
            self.upper_band_bound = self.buffer.height()
            self.band_ranges = self.generate_even_ranges(self.BANDS, 0, self.buffer.width())
            self.colors = [random.randint(0, 255) for _ in range(self.BANDS)]
            self.stream = self.p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK,
                stream_callback=self.process_audio,
            )
            self.gradient_mode = "extend"
            self.base_gradient = [
                232,
                233,
                235,
                237,
                239,
                241,
                243,
                245,
                247,
                249,
                251,
                253,
                255,
            ]
            self.gradient = []
            for _ in range(self.BANDS):
                self.gradient += self.base_gradient
            while len(self.gradient) < self.buffer.width():
                self.gradient += self.base_gradient
            self.true_gradient = [self.gradient[idx] for idx in range(self.buffer.width())]
            self.use_gradient = True
            self.non_gradient_color = 27
            self.orientation = "top"
            self.subtract_y = self.buffer.height()

        def set_audio_properties(
            self, num_bands=24, audio_halt=10, use_gradient=True, non_gradient_color=27
        ):
            """
            Set the properties for the AudioEffect class.

            Args:
                num_bands (int, optional): Number of EQ bands to show. Defaults to 24.
                audio_halt (int, optional): How often we should update the bands, (frame_number % halt == 0 then update). Defaults to 10.
                use_gradient (bool, optional): Whether or not to use color gradient. Defaults to True.
                non_gradient_color (int, optional): Color to use if not a gradient. Defaults to 27 (blue).
            """
            self.BANDS = num_bands
            self.audio_halt = audio_halt
            self.band_ranges = self.generate_even_ranges(self.BANDS, 0, self.buffer.width())
            self.colors = [random.randint(0, 255) for _ in range(self.BANDS)]
            self.use_gradient = use_gradient
            self.non_gradient_color = non_gradient_color

        def evenly_distribute_original_values(self, original_list: list[int], desired_width: int):
            """
            Evenly distribute the values in a list to fit within a certain width.

            Args:
                original_list (list[int]): The list of values to distribute.
                desired_width (int): The width to which the values should be distributed.

            Returns:
                list[int]: The evenly distributed list of values.
            """
            repeat_count = desired_width // len(original_list)
            extra_elements = desired_width % len(original_list)
            expanded_list = []
            for value in original_list:
                expanded_list.extend([value] * repeat_count)
                if extra_elements > 0:
                    expanded_list.append(value)
                    extra_elements -= 1
            return expanded_list

        def set_orientation(self, orientation: str):
            """
            Set the orientation of the visualizer.

            Args:
                orientation (str): The orientation to set ("top" or "bottom").
            """
            if orientation in ["top", "bottom"]:
                self.orientation = orientation
                if self.orientation == "bottom":
                    self.subtract_y = self.buffer.height()
                else:
                    self.subtract_y = 0

        def set_audio_gradient(
            self,
            gradient=[232, 233, 235, 237, 239, 241, 243, 245, 247, 249, 251, 253, 255],
            mode="extend",
        ):
            """
            Set the audio gradient for visualizing audio data.

            Args:
                gradient (list, optional): List of colors to use for gradient. Defaults to [232, 233, 235, 237, 239, 241, 243, 245, 247, 249, 251, 253, 255].
                mode (str, optional): Do we want to repeat the gradient or extend the list evenly. Defaults to "extend".
            """
            self.base_gradient = gradient
            self.gradient_mode = mode
            if self.gradient_mode == "repeat":
                self.gradient = []
                for _ in range(self.BANDS):
                    self.gradient += self.base_gradient
                while len(self.gradient) < self.buffer.width():
                    self.gradient += self.base_gradient
                self.true_gradient = [
                    self.gradient[idx] for idx in range(self.buffer.width())
                ]
            else:
                self.gradient = self.evenly_distribute_original_values(
                    gradient, self.buffer.width()
                )
                self.true_gradient = [
                    self.gradient[idx] for idx in range(self.buffer.width())
                ]

        def process_audio(self, data, frame_count, time_info, status):
            """
            Process the audio data and update the visualizer buffer.

            Args:
                data (_type_): Audio data from the stream.
                frame_count (_type_): N/A
                time_info (_type_): N/A
                status (_type_): N/A

            Returns:
                tuple: (data, pyaudio.paContinue)
            """
            audio_array = np.frombuffer(data, dtype=np.int16)
            fft_result = np.fft.rfft(audio_array)
            magnitudes = np.abs(fft_result)
            band_width = len(magnitudes) // self.BANDS
            self.bands = [
                np.mean(magnitudes[i * band_width : (i + 1) * band_width])
                for i in range(self.BANDS)
            ]
            return (data, pyaudio.paContinue)

        def map_bands_to_range(self, N: int):
            """
            Map the bands to a range of values between 0 and N-1.

            Args:
                N (int): The range of values to map the bands to.

            Returns:
                list[int]: The mapped bands.
            """
            min_band = min(self.bands)
            max_band = max(self.bands)
            rand_band = max_band - min_band if max_band != min_band else 1
            normalized_bands = [(band - min_band) / rand_band for band in self.bands]
            scaled_bands = [int(band * N) for band in normalized_bands]
            return scaled_bands

        def generate_even_ranges(self, groups: list[any], start: int, end: int):
            """
            Generate even ranges from a list of groups.

            Args:
                groups (list[any]): The list of groups to generate ranges from.
                start (int): The starting index of the ranges.
                end (int): The ending index of the ranges.

            Returns:
                _type_: _description_
            """
            approximate_group_size = round((end - start) / groups)
            intervals = []
            for i in range(groups):
                group_start = start + i * approximate_group_size
                group_end = group_start + approximate_group_size
                intervals.append((group_start, min(group_end, end)))
            return intervals

        def render_frame(self, frame_number: int):
            """
            Render a single frame of the animation.

            Args:
                frame_number (int): The current frame number of the animation.
            """
            if frame_number == 0:
                self.stream.start_stream()

            if frame_number % self.audio_halt == 0:
                try:
                    self.buffer.clear_buffer()
                    mapped_bands = self.map_bands_to_range(self.upper_band_bound)[1:]
                    for idx, band_group in enumerate(zip(mapped_bands, self.band_ranges)):
                        band, band_range = band_group
                        for y_change in range(band):
                            for x_change in range(*band_range):
                                if self.use_gradient:
                                    self.buffer.put_char(
                                        x_change,
                                        abs(self.subtract_y - y_change),
                                        bruhcolored(
                                            " ", on_color=self.true_gradient[x_change]
                                        ).colored,
                                        False,
                                    )
                                else:
                                    self.buffer.put_char(
                                        x_change,
                                        abs(self.subtract_y - y_change),
                                        bruhcolored(
                                            " ", on_color=self.non_gradient_color
                                        ).colored,
                                        False,
                                    )
                except:
                    pass
