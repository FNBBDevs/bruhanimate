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

from bruhanimate.bruheffect import AudioSettings
from bruhanimate.bruhrenderer import EffectRenderer
from bruhanimate.bruhutil import Screen

TARGET_FPS = 30
PHASE_FRAMES = 400


def run_phase(screen, renderer, label):
    for frame in range(PHASE_FRAMES):
        t0 = time.perf_counter()
        renderer.render_to_back_buffer(frame)
        screen.print_at(f"  {label}".ljust(screen.width), 0, 0, screen.width)
        renderer.swap_buffers()
        renderer.present_frame()
        elapsed = time.perf_counter() - t0
        remaining = (1 / TARGET_FPS) - elapsed
        if remaining > 0:
            time.sleep(remaining)


def show(screen):
    phases = [
        ("EQ Bars  |  color",    AudioSettings(mode="bars",     color=True,  smoothing=0.75)),
        ("EQ Bars  |  mirror",   AudioSettings(mode="mirror",   color=True,  smoothing=0.75)),
        ("Waveform |  color",    AudioSettings(mode="waveform", color=True,  smoothing=0.5)),
        ("EQ Bars  |  no color", AudioSettings(mode="bars",     color=False, smoothing=0.75)),
    ]

    r = EffectRenderer(screen, PHASE_FRAMES, 1 / TARGET_FPS, "audio", " ", False)

    try:
        for label, settings in phases:
            screen.clear()
            r.effect.set_mode(settings.mode)
            r.effect.set_color(settings.color)
            r.effect.set_smoothing(settings.smoothing)
            run_phase(screen, r, label)
    except KeyboardInterrupt:
        pass
    finally:
        r.effect.stop()


def run():
    Screen.show(show)


if __name__ == "__main__":
    run()
