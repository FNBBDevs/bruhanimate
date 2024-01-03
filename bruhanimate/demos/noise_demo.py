from bruhanimate.bruhscreen import Screen
from bruhanimate.bruhrenderer import CenterRenderer
import bruhanimate.images as images

import os

os.system(" ")


def noise(screen):
    try:
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

        input()

    except KeyboardInterrupt:
        renderer.render_exit()
        renderer.push_front_to_screen()
        input()


def run():
    Screen.show(noise)


if __name__ == "__main__":
    run()