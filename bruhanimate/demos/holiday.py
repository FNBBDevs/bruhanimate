from bruhanimate.bruhscreen import Screen
from bruhanimate.bruhrenderer import *
from bruhanimate.images import get_image

import os

os.system(" ")


def holiday(screen):
    try:
        renderer = CenterRenderer(
            screen=screen,
            frames=2000,
            time=0.075,
            img=get_image("CHRISTMAS_1"),
            effect_type="snow",
            background=" ",
            transparent=True,
        )

        renderer.update_collision(True)

        renderer.update_smart_transparent(True)

        renderer.run()

        input()

    except KeyboardInterrupt:
        renderer.render_exit()
        renderer.push_front_to_screen()
        input()


def run():
    Screen.show(holiday)


if __name__ == "__main__":
    run()
