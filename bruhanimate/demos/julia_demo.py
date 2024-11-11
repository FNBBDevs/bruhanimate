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
    image = bruhimage.text_to_image("JULIA FRACTALS!")

    renderer = CenterRenderer(
        screen=screen,
        img=image,
        frames=float("inf"),
        frame_time=0.01,
        effect_type="julia",
        background=" ",
        transparent=True,
    )

    renderer.run()


def run():
    Screen.show(show)


if __name__ == "__main__":
    run()
