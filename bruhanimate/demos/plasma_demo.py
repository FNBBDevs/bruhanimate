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

from ..bruhutil import Screen, images
from ..bruhrenderer import FocusRenderer


def show(screen):
    image = images.text_to_image("PLASMA!", padding_top_bottom=1, padding_left_right=3)

    # Create the renderer
    renderer = FocusRenderer(
        screen=screen,
        frames=500,
        time=0,
        img=image,
        effect_type="plasma",
        background=" ",
        transparent=False,
        start_frame=110,
        reverse=True,
        start_reverse=300,
    )

    # Set the attributes
    renderer.effect.update_color_properties(
        color=True, characters=True, random_color=True
    )

    renderer.effect.update_grey_scale_size(10)

    renderer.effect.update_plasma_values(10, 26, 19, 41)

    renderer.effect.update_info_visibility(True)

    renderer.run(end_message=True)


def run():
    Screen.show(show)


if __name__ == "__main__":
    run()
