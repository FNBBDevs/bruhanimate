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

from ..bruhutil import Screen, bruhimage
from ..bruhrenderer import CenterRenderer


def static(screen):
    renderer = CenterRenderer(
        screen=screen,
        frames=float("inf"),
        img=bruhimage.text_to_image("STATIC!"),
        frame_time=1.0,
        effect_type="static",
        background="This is a static background! ",
        transparent=False,
    )

    renderer.run()


def run():
    Screen.show(static)


if __name__ == "__main__":
    run()
