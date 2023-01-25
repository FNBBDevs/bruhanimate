from bruhanimate.bruhrenderer import *
from bruhanimate.bruhscreen import Screen
import bruhanimate.images as images
import sys
import pyfiglet

def show(screen):
    image = images.text_to_image("Welcome!", padding_top_bottom=1, padding_left_right=3)
    
    # CREATE THE RENDERER
    renderer = FocusRenderer(screen, 200, 0, image, "plasma", " ", transparent=False, start_frame=50)
    renderer2 = CenterRenderer(screen, 100, 0.01, images.get_image("COMPUTER"), "stars", background=" ", transparent=False)

    # SET EFFECT ATTRIBUTES
    renderer.effect.update_color_properties(color=True, characters=True, random_color=False)
    renderer.effect.update_grey_scale_size(10)
    renderer.effect.update_plasma_values(10, 26, 19, 41)

    renderer2.effect.update_color_type("RAINBOW")
    renderer2.effect.update_intensity(30)
    renderer2.update_smart_transparent(True)

    # RUN THE ANIMATION
    renderer.run(end_message=True)

    # CATCH THE END WITH INPUT() --> for Win-Systems --> Ctl-C for Unix-Systems
    input()

    screen.clear()
    renderer2.run()
    input()


def run():
    Screen.show(show)


if __name__ == "__main__":
    run()