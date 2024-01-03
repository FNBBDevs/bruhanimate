from bruhanimate.bruhscreen import Screen
from bruhanimate.bruhrenderer import CenterRenderer
import bruhanimate.images as images

import os
os.system(" ")

def snow(screen):
    try:
        renderer = CenterRenderer(
            screen=screen,
            img=images.text_to_image("SNOW!"),
            frames=float("inf"),
            time=0.075,
            effect_type="snow",
            background=" ",
            transparent=True
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
    Screen.show(snow)


if __name__ == "__main__":
    run()
