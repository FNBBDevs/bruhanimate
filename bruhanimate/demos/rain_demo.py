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

from ..bruhrenderer import CenterRenderer
from ..bruhutil import Screen, bruhimage


def rain(screen):
    renderer = CenterRenderer(
        screen=screen,
        frames=float("inf"),
        img=bruhimage.text_to_image("RAIN!"),
        frame_time=0.01,
        effect_type="rain",
        background=" ",
        transparent=False,
    )

    renderer.update_collision(True)
    renderer.update_smart_transparent(True)

    renderer.effect.update_intensity(0)
    renderer.effect.update_swells(True)
    renderer.effect.update_wind_direction("east")

    renderer.run()


def run():
    Screen.show(rain)


if __name__ == "__main__":
    run()
