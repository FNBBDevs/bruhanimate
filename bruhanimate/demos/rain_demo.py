from bruhanimate.bruhscreen import Screen
from bruhanimate.bruhrenderer import CenterRenderer
import bruhanimate.images as images

import os

os.system(" ")


def rain(screen):
    try:
        renderer = CenterRenderer(
            screen=screen,
            frames=float("inf"),
            img=images.text_to_image("RAIN!"),
            time=0.05,
            effect_type="rain",
            background=" ",
            transparent=False,
        )

        renderer.update_collision(True)
        renderer.update_smart_transparent(True)
        
        renderer.effect.update_intensity(0)
        renderer.effect.update_swells(True)
        renderer.effect.update_wind_direction("east")

        renderer.run()

        input()

    except KeyboardInterrupt:
        renderer.render_exit()
        renderer.push_front_to_screen()
        input()


def run():
    Screen.show(rain)


if __name__ == "__main__":
    run()