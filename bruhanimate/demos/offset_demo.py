from bruhanimate.bruhscreen import Screen
from bruhanimate.bruhrenderer import CenterRenderer
import bruhanimate.images as images

import os
import sys

os.system(" ")


def offset(screen):
    renderer = CenterRenderer(
        screen=screen,
        frames=float("inf"),
        img=images.text_to_image("OFFSET!"),
        time=0.0,
        effect_type="offset",
        background="!!@@##$$%%^^&&**(())__++",
        transparent=False,
    )

    renderer.run()


def run():
    Screen.show(offset)


if __name__ == "__main__":
    run()
