import os
os.system(" ")

from bruhutil import Screen, images
from bruhrenderer import CenterRenderer


def gol(screen):
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


def run():
    Screen.show(gol)


if __name__ == "__main__":
    run()
