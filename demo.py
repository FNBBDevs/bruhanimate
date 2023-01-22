from bruhanimate.bruhrenderer import *
from bruhanimate.bruhscreen import Screen
import bruhanimate.images as images
import sys

def demo(screen, img, frames, time, effect_type, background, transparent):
    
    # CREATE THE RENDERER
    renderer = CenterRenderer(screen, frames, time, img, effect_type, background, transparent)

    # SET EFFECT ATTRIBUTES
    renderer.update_smart_transparent(True)
    renderer.effect.update_color(True)
    renderer.effect.update_intensity(100)

    # RUN THE ANIMATION
    renderer.run()

    # CATCH THE END WITH INPUT() --> for Win-Systems --> Ctl-C for Unix-Systems
    input()


def main():
    Screen.show(demo, args=(images.get_image("TWOPOINT"), 300, 0, "noise", " ", False))



if __name__ == "__main__":
    main()