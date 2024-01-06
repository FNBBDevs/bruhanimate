from bruhanimate.bruhscreen import Screen
from bruhanimate.bruhrenderer import CenterRenderer
import bruhanimate.images as images

import os
import sys

os.system(" ")


def static(screen):
    try:
        renderer = CenterRenderer(
            screen=screen,
            frames=float("inf"),
            img=images.text_to_image("STATIC!"),
            time=0.0,
            effect_type="static",
            background="This is a static background! ",
            transparent=False,
        )

        renderer.run()

        if sys.platform == 'win32':
            input()

    except KeyboardInterrupt:
        renderer.render_exit()
        renderer.push_front_to_screen()
        if sys.platform == 'win32':
            input()


def run():
    Screen.show(static)


if __name__ == "__main__":
    run()