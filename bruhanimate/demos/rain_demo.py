import os
os.system(" ")

from bruhutil import Screen, images
from bruhrenderer import CenterRenderer


def rain(screen):
    renderer = CenterRenderer(
        screen=screen,
        frames=float("inf"),
        img=images.text_to_image("RAIN!"),
        time=0.01,
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


def run():
    Screen.show(rain)


if __name__ == "__main__":
    run()
