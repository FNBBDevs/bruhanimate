import os
os.system(" ")

from bruhutil import Screen, images
from bruhrenderer import CenterRenderer


def snow(screen):
    renderer = CenterRenderer(
        screen=screen,
        img=images.text_to_image("SNOW!"),
        frames=float("inf"),
        time=0.075,
        effect_type="snow",
        background=" ",
        transparent=True,
    )

    renderer.update_collision(True)

    renderer.update_smart_transparent(True)

    renderer.run()


def run():
    Screen.show(snow)


if __name__ == "__main__":
    run()
