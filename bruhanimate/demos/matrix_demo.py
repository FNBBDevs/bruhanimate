from bruhanimate.bruhscreen import Screen
from bruhanimate.bruhrenderer import CenterRenderer
import bruhanimate.images as images

import os
import sys

os.system(" ")


def matrix(screen):
    renderer = CenterRenderer(
        screen=screen,
        img=images.text_to_image("MATRIX!"),
        frames=float("inf"),
        time=0,
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
