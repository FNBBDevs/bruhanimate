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
import sys
import threading

import numpy as np
from bruhcolor import bruhcolored as bc

from ..bruhutil.bruhffer import Buffer
from .base_effect import BaseEffect
from .settings import AudioSettings

_SAMPLE_RATE = 44100
_CHUNK = 1024
_RAIN_CHARS = "01アウイエオカキクケコサシスセソタチツテト"

# Modes that manage their own buffer state — skip the per-frame clear
_STATEFUL_MODES = {"spectrum", "rain", "waveform"}

# Optional dependency detection
try:
    import sounddevice as _sd
    _HAS_SD = True
except ImportError:
    _HAS_SD = False

if sys.platform == "win32":
    try:
        import pyaudiowpatch as _pa_mod
        _HAS_PAW = True
    except ImportError:
        _HAS_PAW = False
else:
    _HAS_PAW = False


def _find_monitor_device():
    """Return a sounddevice input device index for a PulseAudio/PipeWire monitor, or None."""
    if not _HAS_SD:
        return None
    for i, dev in enumerate(_sd.query_devices()):
        name = dev.get("name", "").lower()
        if "monitor" in name and dev.get("max_input_channels", 0) > 0:
            return i
    return None


class AudioEffect(BaseEffect):
    """
    Visualizes system audio output as terminal animations.

    Modes:

    - ``"bars"``     — vertical EQ bars
    - ``"mirror"``   — EQ bars mirrored from the vertical center outward
    - ``"waveform"`` — oscilloscope: filled columns from center to sample amplitude
    - ``"spectrum"`` — scrolling spectrogram; frequency on Y, time on X
    - ``"radial"``   — circular pulse from center; each ring driven by a frequency band
    - ``"rain"``     — audio-driven falling character rain; frequency energy sets density

    **Windows** requires ``PyAudioWPatch`` for WASAPI loopback::

        pip install bruhanimate[audio]

    **Linux** requires ``sounddevice`` and a PulseAudio/PipeWire monitor source::

        pip install bruhanimate[audio]
    """

    def __init__(self, buffer: Buffer, background: str, settings: AudioSettings = None):
        """
        Initialize the audio effect.

        Args:
            buffer (Buffer): Effect buffer to push updates to.
            background (str): Character or string to use for the background.
            settings (AudioSettings, optional): Configuration for the audio effect.
        """
        super().__init__(buffer, background)
        s = settings or AudioSettings()

        self.mode = s.mode
        self.bar_char = s.bar_char
        self.smoothing = s.smoothing
        self.color = s.color
        self.sensitivity = s.sensitivity

        self._height = buffer.height()
        self._width = buffer.width()
        self._num_bars = s.num_bars if s.num_bars > 0 else max(1, self._width // 2)

        self._bars = np.zeros(self._num_bars)
        self._wave_history = np.zeros(self._width)
        self._lock = threading.Lock()
        self._running = True
        self._audio_chunk = np.zeros(_CHUNK, dtype=np.float32)
        self._error: str = None

        self._thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._thread.start()

    # ------------------------------------------------------------------
    # Runtime setters
    # ------------------------------------------------------------------

    def set_mode(self, mode: str):
        """Switch visualization mode. Clears the buffer when leaving a stateful mode."""
        if self.mode in _STATEFUL_MODES and mode not in _STATEFUL_MODES:
            self.buffer.clear_buffer(val=self.background)
        self.mode = mode

    def set_sensitivity(self, sensitivity: float):
        """Adjust the amplitude sensitivity multiplier."""
        self.sensitivity = sensitivity

    def set_smoothing(self, smoothing: float):
        """Set temporal smoothing (0 = none, close to 1 = very smooth)."""
        self.smoothing = smoothing

    def set_color(self, color: bool):
        """Enable or disable colorized output."""
        self.color = color

    def set_bar_char(self, bar_char: str):
        """Set the character used to draw bars and fills."""
        self.bar_char = bar_char

    # ------------------------------------------------------------------
    # Audio capture
    # ------------------------------------------------------------------

    def _capture_loop(self):
        if sys.platform == "win32":
            self._capture_windows()
        else:
            self._capture_linux()

    def _capture_windows(self):
        if not _HAS_PAW:
            self._error = "PyAudioWPatch not installed. Run: pip install bruhanimate[audio]"
            return
        try:
            pa = _pa_mod.PyAudio()
            wasapi = pa.get_host_api_info_by_type(_pa_mod.paWASAPI)
            speakers = pa.get_device_info_by_index(wasapi["defaultOutputDevice"])

            # Loopback device names are "<name> [Loopback]" — use substring match.
            loopback = None
            if hasattr(pa, "get_loopback_device_info_generator"):
                for dev in pa.get_loopback_device_info_generator():
                    if speakers["name"] in dev["name"]:
                        loopback = dev
                        break

            if loopback is None:
                for i in range(pa.get_device_count()):
                    dev = pa.get_device_info_by_index(i)
                    if dev.get("isLoopbackDevice", False) and speakers["name"] in dev["name"]:
                        loopback = dev
                        break

            if loopback is None:
                self._error = "No WASAPI loopback device found. Is PyAudioWPatch installed?"
                return

            channels = max(1, loopback.get("maxInputChannels", 2))
            rate = int(loopback.get("defaultSampleRate", _SAMPLE_RATE))

            def _cb(in_data, frame_count, time_info, status):
                audio = np.frombuffer(in_data, dtype=np.float32)
                if channels > 1:
                    audio = audio[::channels]
                chunk = np.zeros(_CHUNK, dtype=np.float32)
                n = min(len(audio), _CHUNK)
                chunk[:n] = audio[:n]
                with self._lock:
                    self._audio_chunk = chunk
                return (None, _pa_mod.paContinue)

            stream = pa.open(
                format=_pa_mod.paFloat32,
                channels=channels,
                rate=rate,
                input=True,
                frames_per_buffer=_CHUNK,
                input_device_index=loopback["index"],
                stream_callback=_cb,
            )
            stream.start_stream()
            while self._running:
                threading.Event().wait(0.05)
            stream.stop_stream()
            stream.close()
            pa.terminate()
        except Exception as exc:
            self._error = f"Audio error: {exc}"

    def _capture_linux(self):
        if not _HAS_SD:
            self._error = "sounddevice not installed. Run: pip install bruhanimate[audio]"
            return
        device = _find_monitor_device()

        def _cb(indata, frames, time, status):
            audio = indata[:, 0].copy()
            chunk = np.zeros(_CHUNK, dtype=np.float32)
            n = min(len(audio), _CHUNK)
            chunk[:n] = audio[:n]
            with self._lock:
                self._audio_chunk = chunk

        try:
            kwargs = {"device": device} if device is not None else {}
            with _sd.InputStream(
                samplerate=_SAMPLE_RATE,
                channels=1,
                callback=_cb,
                blocksize=_CHUNK,
                **kwargs,
            ):
                while self._running:
                    _sd.sleep(50)
        except Exception as exc:
            self._error = f"Audio error: {exc}"

    # ------------------------------------------------------------------
    # DSP helpers
    # ------------------------------------------------------------------

    def _fft_bars(self, audio: np.ndarray) -> np.ndarray:
        """Return smoothed, normalised EQ bar heights (0–1)."""
        window = np.hanning(len(audio))
        fft = np.abs(np.fft.rfft(audio * window))
        freqs = np.linspace(0, _SAMPLE_RATE / 2, len(fft))
        edges = np.logspace(np.log10(20), np.log10(20000), self._num_bars + 1)

        raw = np.zeros(self._num_bars)
        for i in range(self._num_bars):
            lo = np.searchsorted(freqs, edges[i])
            hi = max(np.searchsorted(freqs, edges[i + 1]), lo + 1)
            raw[i] = np.mean(fft[lo:hi])

        peak = raw.max() + 1e-8
        raw = np.clip(raw / peak * self.sensitivity, 0.0, 1.0)
        self._bars = self._bars * self.smoothing + raw * (1.0 - self.smoothing)
        return self._bars

    @staticmethod
    def _height_color(ratio: float) -> int:
        """Green → yellow → red based on magnitude (0–1)."""
        if ratio < 0.5:
            return 22 + int(ratio * 2 * 24)  # dark green → bright green
        elif ratio < 0.8:
            return 226  # yellow
        else:
            return 196  # red

    @staticmethod
    def _heat_color(ratio: float) -> int:
        """Blue → cyan → green → yellow → red heat palette (0–1)."""
        if ratio < 0.25:
            return 17 + int(ratio * 4 * 18)   # dark blue → blue
        elif ratio < 0.5:
            return 51 + int((ratio - 0.25) * 4 * 12)  # cyan → green
        elif ratio < 0.75:
            return 82 + int((ratio - 0.5) * 4 * 12)   # green → yellow
        else:
            return 220 + int((ratio - 0.75) * 4 * 3)  # yellow → red

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render_frame(self, frame_number: int):
        # Stateful modes scroll their own buffer; everything else gets cleared.
        if self.mode not in _STATEFUL_MODES:
            self.buffer.clear_buffer(val=self.background)

        with self._lock:
            audio = self._audio_chunk.copy()

        if self._error:
            msg = self._error[:self._width]
            y = self._height // 2
            x = max(0, (self._width - len(msg)) // 2)
            self.buffer.put_at(x, y, msg)
            return

        if self.mode == "mirror":
            self._render_mirror(audio)
        elif self.mode == "waveform":
            self._render_waveform(audio)
        elif self.mode == "spectrum":
            self._render_spectrum(audio)
        elif self.mode == "radial":
            self._render_radial(audio)
        elif self.mode == "rain":
            self._render_rain(audio)
        else:
            self._render_bars(audio)

    def _render_bars(self, audio: np.ndarray):
        bars = self._fft_bars(audio)
        bar_w = max(1, self._width // self._num_bars)

        for i, mag in enumerate(bars):
            bar_h = int(mag * self._height)
            x0 = i * bar_w
            color = self._height_color(mag) if self.color else None
            ch = bc(self.bar_char, color=color) if color is not None else self.bar_char

            for col in range(x0, min(x0 + bar_w - 1, self._width)):
                for pix in range(bar_h):
                    self.buffer.put_char(col, self._height - 1 - pix, ch)

    def _render_mirror(self, audio: np.ndarray):
        bars = self._fft_bars(audio)
        bar_w = max(1, self._width // self._num_bars)
        mid = self._height // 2

        for i, mag in enumerate(bars):
            bar_h = int(mag * mid)
            x0 = i * bar_w
            color = self._height_color(mag) if self.color else None
            ch = bc(self.bar_char, color=color) if color is not None else self.bar_char

            for col in range(x0, min(x0 + bar_w - 1, self._width)):
                for pix in range(bar_h):
                    row_up = mid - 1 - pix
                    row_dn = mid + pix
                    if 0 <= row_up < self._height:
                        self.buffer.put_char(col, row_up, ch)
                    if 0 <= row_dn < self._height:
                        self.buffer.put_char(col, row_dn, ch)

    def _render_waveform(self, audio: np.ndarray):
        """Scrolling RMS amplitude envelope: each column = one frame, scrolls left over time."""
        rms = float(np.sqrt(np.mean(audio ** 2)))
        amp = min(rms * self.sensitivity * 8, 1.0)

        self._wave_history = np.roll(self._wave_history, -1)
        self._wave_history[-1] = amp

        mid = self._height // 2
        bg = self.background
        for x, val in enumerate(self._wave_history):
            peak = int(val * mid)
            color = self._height_color(val) if self.color else None
            ch = bc(self.bar_char, color=color) if color is not None else self.bar_char
            for row in range(self._height):
                offset = abs(row - mid)
                self.buffer.put_char(x, row, ch if offset <= peak else bg)

    def _render_spectrum(self, audio: np.ndarray):
        """Scrolling spectrogram: frequency on Y axis, time scrolls left."""
        bars = self._fft_bars(audio)
        bg = self.background

        # Shift every row 1 column left
        for row in self.buffer.buffer:
            row.pop(0)
            row.append(bg)

        # Draw the current FFT snapshot on the rightmost column
        x = self._width - 1
        n = len(bars)
        for i, mag in enumerate(bars):
            # Low frequencies at bottom, high at top
            y = self._height - 1 - int(i * self._height / n)
            y = max(0, min(self._height - 1, y))
            if mag > 0.02:
                color = self._heat_color(mag) if self.color else None
                ch = bc(self.bar_char, color=color) if color is not None else self.bar_char
                self.buffer.put_char(x, y, ch)

    def _render_radial(self, audio: np.ndarray):
        """Circular pulse: each ring's radius is driven by its frequency band's energy."""
        bars = self._fft_bars(audio)
        cx = self._width // 2
        cy = self._height // 2
        # Terminal chars are ~2x taller than wide, compensate so the shape looks circular
        max_r = min(cx, cy * 2)
        n = len(bars)

        for row in range(self._height):
            for col in range(self._width):
                dx = col - cx
                dy = (row - cy) * 2  # aspect ratio compensation
                r = (dx * dx + dy * dy) ** 0.5
                r_norm = min(r / max_r, 1.0)
                band = int(r_norm * (n - 1))
                mag = bars[band]
                if mag > r_norm:
                    # Color by distance from center (inner = brighter)
                    color = self._height_color(1.0 - r_norm) if self.color else None
                    ch = bc(self.bar_char, color=color) if color is not None else self.bar_char
                    self.buffer.put_char(col, row, ch)

    def _render_rain(self, audio: np.ndarray):
        """Audio-driven rain: frequency energy per band controls drop density."""
        bars = self._fft_bars(audio)
        cols_per_bar = max(1, self._width // len(bars))
        bg = self.background

        # Scroll buffer down by 1 row
        self.buffer.buffer.insert(0, [bg] * self._width)
        self.buffer.buffer.pop()

        # Spawn new drops at the top row based on frequency energy
        top = self.buffer.buffer[0]
        for i, mag in enumerate(bars):
            x0 = i * cols_per_bar
            x1 = min(x0 + cols_per_bar, self._width)
            for col in range(x0, x1):
                if random.random() < mag:
                    color = self._height_color(mag) if self.color else None
                    char = random.choice(_RAIN_CHARS)
                    top[col] = bc(char, color=color) if color is not None else char

    def stop(self):
        """Stop the background audio capture thread."""
        self._running = False
