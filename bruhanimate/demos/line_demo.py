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

os.system("")

from ..bruhrenderer import PanRenderer
from ..bruhutil import Screen, bruhimage


def demo(screen, img, frames, time, effect, background, transparent):
    # CREATE THE RENDERER
    renderer = PanRenderer(
        screen=screen,
        frames=frames,
        frame_time=time,
        img=img,
        effect_type=effect,
        background=background,
        transparent=transparent,
        loop=True,
    )

    # REGISTER THE LINES - LET'S MAKE A DECENT 3D TRIANGLE
    renderer.effect.add_line((15, 15), (30, 30))
    renderer.effect.add_line((30, 30), (50, 20))
    renderer.effect.add_line((50, 20), (15, 15))

    renderer.effect.add_line((30, 30), (32, 22))
    renderer.effect.add_line((32, 22), (15, 15))
    renderer.effect.add_line((32, 22), (50, 20))

    # RUN THE ANIMATION
    renderer.run(end_message=False)


def run():
    image = bruhimage.text_to_image(
        "HELLO WORLD!", padding_top_bottom=1, padding_left_right=3
    )
    Screen.show(demo, args=(image, 500, 0.05, "drawlines", " ", True))


if __name__ == "__main__":
    run()
