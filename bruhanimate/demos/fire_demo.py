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

from bruhanimate.bruhutil import Screen, bruhimage
from bruhanimate.bruhrenderer import CenterRenderer


def show(screen):
    image = bruhimage.text_to_image("FIRE EFFECT!")

    renderer = CenterRenderer(
        screen=screen,
        img=image,
        frames=float("inf"),
        frame_time=0.02,
        effect_type="fire",
        background=" ",
        transparent=False,
    )

    renderer.effect.set_fire_ascii_chars(ascii_chars=" .:#####%@")
    renderer.effect.set_fire_intensity(fire_intensity=0.4)
    # renderer.effect.set_fire_background_color(True)
    renderer.effect.set_fire_use_char_color(use_char_color=True)
    # renderer.effect.set_fire_wind(direction=270, strength=1.0)
    renderer.effect.set_fire_turbulence(turbulence=0.1)
    renderer.effect.set_fire_heat_spot_intensity(1)
    renderer.run()


def run():
    Screen.show(show)


if __name__ == "__main__":
    run()
