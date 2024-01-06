from bruhanimate.bruhscreen import Screen
from bruhanimate.bruhrenderer import CenterRenderer
import bruhanimate.images as images

import os
import sys

os.system(" ")


def gol(screen):
    try:
        renderer = CenterRenderer(
            screen=screen,
            frames=float("inf"),
            img=images.text_to_image("GOL!"),
            time=0.0,
            effect_type="gol",
            background=" ",
            transparent=False,
        )

        renderer.effect.update_decay(True, "RAINBOW", "default")

        renderer.run()

        if sys.platform == 'win32':
            input()

    except KeyboardInterrupt:
        renderer.render_exit()
        renderer.push_front_to_screen()
        if sys.platform == 'win32':
            input()


def run():
    Screen.show(gol)


if __name__ == "__main__":
    run()