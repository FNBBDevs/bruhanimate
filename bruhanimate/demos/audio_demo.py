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
os.system(" ")

from ..bruhutil import Screen, bruhimage, GRADIENTS
from ..bruhrenderer import CenterRenderer

def audio(screen):
    renderer = CenterRenderer(
        screen=screen,
        frames=float("inf"),
        img=bruhimage.text_to_image("AUDIO!"),
        time=0.01,
        effect_type="audio",
        background=" ",
        transparent=False,
    )
    renderer.effect.set_audio_properties(num_bands=screen.width, audio_halt=15, use_gradient=True)
    renderer.effect.set_audio_gradient(GRADIENTS[0], mode="repeat")
    renderer.effect.set_orientation("top")
    renderer.run()


def run():
    Screen.show(audio)


if __name__ == "__main__":
    run()
