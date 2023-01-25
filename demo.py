from bruhanimate.bruhrenderer import *
from bruhanimate.bruhscreen import Screen
import bruhanimate.images as images
import sys
import pyfiglet

def demo(screen, img, frames, time, effect_type, background, transparent):
    
    # CREATE THE RENDERER
    renderer = CenterRenderer(screen, frames, time, img, effect_type, background, transparent)

    # SET EFFECT ATTRIBUTES
    renderer.effect.update_color(color=True, characters=True)
    renderer.update_smart_transparent(True)

    # RUN THE ANIMATION
    renderer.run(end_message=False)

    # CATCH THE END WITH INPUT() --> for Win-Systems --> Ctl-C for Unix-Systems
    print(screen.width, screen.height)
    input()


def main():
    image = images.get_image("BRUH")
    Screen.show(demo, args=(image, 300, 0, "plasma", " ", False))



if __name__ == "__main__":
    main()