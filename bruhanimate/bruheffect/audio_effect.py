import pyaudio
import random

import numpy as np

from bruhcolor import bruhcolored
from .base_effect import BaseEffect


class AudioEffect(BaseEffect):
    def __init__(
        self, buffer, background: str, num_bands: int = 24, audio_halt: int = 10
    ):
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
        self.BANDS = num_bands
        self.audio_halt = audio_halt
        self.band_ranges = self.generate_even_ranges(self.BANDS, 0, self.buffer.width())
        self.colors = [random.randint(0, 255) for _ in range(self.BANDS)]
        self.use_gradient = use_gradient
        self.non_gradient_color = non_gradient_color

    def evenly_distribute_original_values(self, original_list, desired_width):
        repeat_count = desired_width // len(original_list)
        extra_elements = desired_width % len(original_list)
        expanded_list = []
        for value in original_list:
            expanded_list.extend([value] * repeat_count)
            if extra_elements > 0:
                expanded_list.append(value)
                extra_elements -= 1
        return expanded_list

    def set_orientation(self, orientation):
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
        audio_array = np.frombuffer(data, dtype=np.int16)
        fft_result = np.fft.rfft(audio_array)
        magnitudes = np.abs(fft_result)
        band_width = len(magnitudes) // self.BANDS
        self.bands = [
            np.mean(magnitudes[i * band_width : (i + 1) * band_width])
            for i in range(self.BANDS)
        ]
        return (data, pyaudio.paContinue)

    def map_bands_to_range(self, N):
        min_band = min(self.bands)
        max_band = max(self.bands)
        rand_band = max_band - min_band if max_band != min_band else 1
        normalized_bands = [(band - min_band) / rand_band for band in self.bands]
        scaled_bands = [int(band * N) for band in normalized_bands]
        return scaled_bands

    def generate_even_ranges(self, groups, start, end):
        approximate_group_size = round((end - start) / groups)
        intervals = []
        for i in range(groups):
            group_start = start + i * approximate_group_size
            group_end = group_start + approximate_group_size
            intervals.append((group_start, min(group_end, end)))
        return intervals

    def render_frame(self, frame_number):
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
