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
from bruhanimate.bruheffect import DiffusionSettings

TARGET_FPS = 30
PHASE_FRAMES = 500


def _run(screen):
    screen.clear()

    phases = [
        (
            "Coral pattern  (f=0.0545, k=0.062)",
            DiffusionSettings(f=0.0545, k=0.062, color=True, steps_per_frame=8),
        ),
        (
            "Spot pattern   (f=0.035,  k=0.065)",
            DiffusionSettings(f=0.035, k=0.065, color=True, steps_per_frame=8),
        ),
        (
            "Stripe pattern (f=0.026,  k=0.051)",
            DiffusionSettings(f=0.026, k=0.051, color=True, steps_per_frame=8),
        ),
    ]

    try:
        for label, settings in phases:
            screen.clear()
            renderer = EffectRenderer(
                screen,
                frames=PHASE_FRAMES,
                frame_time=1 / TARGET_FPS,
                effect_type="diffusion",
                background=" ",
                settings=settings,
            )
            for frame in range(PHASE_FRAMES):
                t0 = time.perf_counter()
                renderer.render_to_back_buffer(frame)
                screen.print_at(
                    f"  Diffusion: {label}  (Ctrl+C to skip)".ljust(screen.width),
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


def run():
    Screen.show(_run)


if __name__ == "__main__":
    Screen.show(_run)
