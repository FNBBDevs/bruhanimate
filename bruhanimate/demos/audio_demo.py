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

from bruhanimate.bruheffect import AudioEffect, AudioSettings
from bruhanimate.bruhrenderer import EffectRenderer
from bruhanimate.bruhutil import Screen


def show(screen):
    screen.clear()

    phases = [
        ("EQ Bars  |  color",    AudioSettings(mode="bars",     color=True,  smoothing=0.75)),
        ("EQ Bars  |  mirror",   AudioSettings(mode="mirror",   color=True,  smoothing=0.75)),
        ("Waveform |  color",    AudioSettings(mode="waveform", color=True,  smoothing=0.5)),
        ("EQ Bars  |  no color", AudioSettings(mode="bars",     color=False, smoothing=0.75)),
    ]

    for label, settings in phases:
        renderer = EffectRenderer(
            screen=screen,
            frames=float("inf"),
            frame_time=1 / 30,
            effect_type="audio",
            background=" ",
            transparent=False,
        )
        renderer.effect = AudioEffect(
            renderer.effect.buffer,
            " ",
            settings=settings,
        )
        try:
            renderer.run(end_message=False)
        except KeyboardInterrupt:
            renderer.effect.stop()
            return
        renderer.effect.stop()


def run():
    Screen.show(show)


if __name__ == "__main__":
    run()
