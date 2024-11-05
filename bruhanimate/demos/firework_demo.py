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

from bruhanimate.bruhutil import Screen, bruhimage, Buffer
from bruhanimate.bruhrenderer import CenterRenderer
from bruhanimate.bruheffect import TwinkleEffect


def show(screen):
    image = bruhimage.text_to_image("HAPPY NEW YEAR!", font="js_cursive")

    renderer = CenterRenderer(
        screen=screen,
        img=image,
        frames=float("inf"),
        frame_time=0.05,
        effect_type="firework",
        background=" ",
        transparent=True
    )

    second_effect = TwinkleEffect(buffer=Buffer(screen.height, screen.width), background=" ")
    second_effect.set_density(0.01)

    renderer.effect.set_second_effect(second_effect)
    renderer.effect.set_firework_rate(0.05)
    renderer.effect.set_firework_type("random")
    renderer.effect.set_firework_color_enabled(True)
    renderer.effect.set_firework_color_type("twotone")
    renderer.run(end_message=True)


def run():
    Screen.show(show)


if __name__ == "__main__":
    run()