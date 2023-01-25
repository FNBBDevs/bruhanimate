from bruhanimate.bruhrenderer import *
from bruhanimate.bruhscreen import Screen
import bruhanimate.images as images

def demo(screen, img, frames, time, effect, background, transparent):
    # CREATE THE RENDERER
    renderer = PanRenderer(screen, frames, time, img, effect, background, transparent, loop=True)
    
    # REGISTER THE LINES - LET'S MAKE A DECENT 3D TRIANGLE
    renderer.effect.add_line((15, 15), (30, 30))
    renderer.effect.add_line((30, 30), (50, 20))
    renderer.effect.add_line((50, 20), (15, 15))

    renderer.effect.add_line((30,30), (32, 22))
    renderer.effect.add_line((32, 22), (15, 15))
    renderer.effect.add_line((32, 22), (50, 20))


    # RUN THE ANIMATION
    renderer.run(end_message=False)

    # CATCH THE END WITH INPUT() ON WINDOWS
    input()

image = images.text_to_image("HELLO WORLD!", padding_top_bottom=1, padding_left_right=3)
Screen.show(demo, args=(image, 500, 0.05, "drawlines", " ", True))