import os
os.system(" ")

from bruhutil import Screen, images
from bruhrenderer import CenterRenderer


def noise(screen):
    renderer = CenterRenderer(
        screen=screen,
        frames=float("inf"),
        img=images.text_to_image("NOISE!"),
        time=0.0,
        effect_type="noise",
        background=" ",
        transparent=False,
    )

    renderer.effect.update_color(True, False)

    renderer.run()


def run():
    Screen.show(noise)


if __name__ == "__main__":
    run()
