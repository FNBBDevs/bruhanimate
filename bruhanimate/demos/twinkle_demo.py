from bruhanimate.bruhscreen import Screen
from bruhanimate.bruhrenderer import CenterRenderer
import bruhanimate.images as images

import os

os.system(" ")


def twinkle(screen):
    try:
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

        input()

    except KeyboardInterrupt:
        renderer.render_exit()
        renderer.push_front_to_screen()
        input()


def run():
    Screen.show(twinkle)


if __name__ == "__main__":
    run()