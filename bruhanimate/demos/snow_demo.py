from bruhanimate.bruhscreen import Screen
from bruhanimate.bruhrenderer import EffectRenderer

import os
os.system(" ")

def snow(screen):
    try:
        renderer = EffectRenderer(
            screen,
            float("inf"),
            0.075,
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
    Screen.show(snow)


if __name__ == "__main__":
    run()
