import os
os.system(" ")

from bruhanimate import Screen, get_image
from bruhanimate import CenterRenderer


def holiday(screen):
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


def run():
    Screen.show(holiday)


if __name__ == "__main__":
    run()
