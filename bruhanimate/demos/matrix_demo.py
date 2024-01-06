from bruhanimate.bruhscreen import Screen
from bruhanimate.bruhrenderer import EffectRenderer

import os
import sys

os.system(" ")


def matrix(screen):
    try:
        renderer = EffectRenderer(
            screen=screen,
            frames=float("inf"),
            time=0.05,
            effect_type="matrix",
            background=" ",
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
    Screen.show(matrix)


if __name__ == "__main__":
    run()