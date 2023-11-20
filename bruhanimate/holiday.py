from bruhanimate.bruhscreen import Screen
from bruhanimate.bruhrenderer import *
from bruhanimate.images import get_image

import os
os.system(" ")

def holiday(screen):
    try:
        renderer = CenterRenderer(
            screen,
            2000,
            0.075,
            get_image("CHRISTMAS_1"),
            effect_type="snow",
            background=" ",
            transparent=True
        )
        
        renderer.update_collision(True)

        renderer.update_smart_transparent(True)

        renderer.run()

        input()

    except KeyboardInterrupt:
        pass


def run():
    Screen.show(holiday)


if __name__ == "__main__":
    run()
