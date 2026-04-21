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
from bruhanimate.bruheffect import AutomatonSettings

TARGET_FPS = 30
PHASE_FRAMES = 200


def run(screen):
    screen.clear()

    phases = [
        ("Rule 30   — chaotic", 30),
        ("Rule 90   — Sierpinski triangle", 90),
        ("Rule 110  — Turing-complete", 110),
        ("Rule 184  — traffic flow", 184),
    ]

    renderer = EffectRenderer(
        screen,
        frames=PHASE_FRAMES,
        frame_time=1 / TARGET_FPS,
        effect_type="automaton",
        background=" ",
        settings=AutomatonSettings(color=True, rule=phases[0][1]),
    )

    try:
        for label, rule in phases:
            screen.clear()
            renderer.effect.set_rule(rule)
            for frame in range(PHASE_FRAMES):
                t0 = time.perf_counter()
                renderer.render_to_back_buffer(frame)
                screen.print_at(
                    f"  Automaton: {label}  (Ctrl+C to skip)".ljust(screen.width),
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


if __name__ == "__main__":
    Screen.show(run)
