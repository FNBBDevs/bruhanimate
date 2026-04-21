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

import os
import time

os.system(" ")

from bruhanimate import EffectRenderer, Screen
from bruhanimate.bruheffect import AudioSettings

TARGET_FPS = 30
PHASE_FRAMES = 300


def _run(screen):
    screen.clear()

    phases = [
        ("Bars", AudioSettings(mode="bars", color=True, smoothing=0.5)),
        ("Mirror", AudioSettings(mode="mirror", color=True, smoothing=0.5)),
        ("Waveform", AudioSettings(mode="waveform", color=True, smoothing=0.1)),
        ("Spectrum", AudioSettings(mode="spectrum", color=True, smoothing=0.2)),
        ("Radial", AudioSettings(mode="radial", color=True, smoothing=0.3)),
        ("Rain", AudioSettings(mode="rain", color=True, smoothing=0.2)),
        ("Tunnel", AudioSettings(mode="tunnel", color=True, smoothing=0.2)),
        (
            "Ripple",
            AudioSettings(mode="ripple", color=True, smoothing=0.15, sensitivity=1.5),
        ),
        ("Vortex", AudioSettings(mode="vortex", color=True, smoothing=0.2)),
        ("Wave", AudioSettings(mode="wave", color=True, smoothing=0.25)),
        ("Starfield", AudioSettings(mode="starfield", color=True, smoothing=0.2)),
        (
            "Fireworks",
            AudioSettings(
                mode="fireworks", color=True, smoothing=0.15, sensitivity=2.0
            ),
        ),
        ("Interference", AudioSettings(mode="interference", color=True, smoothing=0.2)),
        ("Bounce", AudioSettings(mode="bounce", color=True, smoothing=0.2)),
        (
            "Lightning",
            AudioSettings(mode="lightning", color=True, smoothing=0.1, sensitivity=1.5),
        ),
        ("Aurora", AudioSettings(mode="aurora", color=True, smoothing=0.3)),
        ("Orbit", AudioSettings(mode="orbit", color=True, smoothing=0.2)),
        (
            "Scope",
            AudioSettings(mode="scope", color=True, smoothing=0.0, sensitivity=3.0),
        ),
        ("Grid", AudioSettings(mode="grid", color=True, smoothing=0.2)),
        ("Helix", AudioSettings(mode="helix", color=True, smoothing=0.25)),
        ("Lissajous", AudioSettings(mode="lissajous", color=True, smoothing=0.2)),
        ("Sunburst", AudioSettings(mode="sunburst", color=True, smoothing=0.2)),
        ("Mandala", AudioSettings(mode="mandala", color=True, smoothing=0.25)),
        (
            "Comet",
            AudioSettings(mode="comet", color=True, smoothing=0.15, sensitivity=1.5),
        ),
        ("Weave", AudioSettings(mode="weave", color=True, smoothing=0.2)),
    ]

    renderer = EffectRenderer(
        screen,
        frames=PHASE_FRAMES,
        frame_time=1 / TARGET_FPS,
        effect_type="audio",
        background=" ",
        settings=phases[0][1],
    )

    try:
        for label, settings in phases:
            screen.clear()
            renderer.effect.set_mode(settings.mode)
            renderer.effect.set_color(settings.color)
            renderer.effect.set_smoothing(settings.smoothing)
            renderer.effect.set_sensitivity(settings.sensitivity)
            for frame in range(PHASE_FRAMES):
                t0 = time.perf_counter()
                renderer.render_to_back_buffer(frame)
                screen.print_at(
                    f"  Audio: {label}  (Ctrl+C to skip)".ljust(screen.width),
                    0,
                    0,
                    screen.width,
                )
                renderer.swap_buffers()
                renderer.present_frame()
                elapsed = time.perf_counter() - t0
                remaining = 1 / TARGET_FPS - elapsed
                if remaining > 0:
                    time.sleep(remaining)
    except KeyboardInterrupt:
        pass
    finally:
        renderer.effect.stop()


def run():
    Screen.show(_run)


if __name__ == "__main__":
    Screen.show(_run)
