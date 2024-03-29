from bruhanimate.bruhscreen import Screen
from bruhanimate.bruhrenderer import CenterRenderer
import bruhanimate.images as images

import os
import sys

os.system(" ")


def twinkle(screen):
    renderer = CenterRenderer(
        screen=screen,
        img=images.text_to_image("TWINKLE!"),
        frames=float("inf"),
        time=0.05,
        effect_type="twinkle",
        background=" ",
        transparent=False,
    )

    renderer.run()


def run():
    Screen.show(twinkle)


if __name__ == "__main__":
    run()
