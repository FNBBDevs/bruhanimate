from bruhscreen import Screen
from bruhrenderer import *
from images import get_image

import os

os.system(" ")


def holiday(screen):
    try:
        renderer = CenterRenderer(
            screen=screen,
            frames=1000,
            time=0.0,
            img=get_image("COMPUTER"),
            effect_type="snow",
            background=" ",
            transparent=True,
        )

        # renderer.effect.show_info(True)

        # renderer.update_smart_transparent(True)

        renderer.update_collision(True)

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
