import os
os.system(" ")

from bruhanimate import Screen, images
from bruhanimate import CenterRenderer


def static(screen):
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


def run():
    Screen.show(static)


if __name__ == "__main__":
    run()
