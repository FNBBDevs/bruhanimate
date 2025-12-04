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


def matrix(screen):
    renderer = CenterRenderer(
        screen=screen,
        img=bruhimage.text_to_image("MATRIX!"),
        frames=float("inf"),
        frame_time=0,
        effect_type="matrix",
        background=" ",
        transparent=False,
    )

    renderer.effect.set_matrix_properties((1, 25), (1, 10), 0.5, 0.5, 0.5, 10)

    renderer.run()


def run():
    Screen.show(matrix)


if __name__ == "__main__":
    run()
