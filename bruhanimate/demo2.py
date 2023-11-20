from bruhanimate.bruhscreen import Screen
from bruhanimate.bruhrenderer import *
from bruhanimate.images import text_to_image, get_image

import os
os.system(" ")

def chirstmas(screen):
    try:
        renderer = CenterRenderer(
            screen,
            4000,
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

Screen.show(chirstmas)