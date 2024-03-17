from bruhanimate.bruhscreen import Screen
from bruhanimate.bruhrenderer import EffectRenderer

import os
import sys

os.system(" ")


def stars(screen):
    renderer = EffectRenderer(
        screen=screen,
        frames=float("inf"),
        time=0.05,
        effect_type="stars",
        background=" ",
        transparent=False,
    )

    renderer.effect.update_color_type("GREYSCALE")

    renderer.run()


def run():
    Screen.show(stars)


if __name__ == "__main__":
    run()
