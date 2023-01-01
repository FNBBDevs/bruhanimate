from bruhanimate.bruhscreen import WinScreen
from bruhanimate.bruhrenderer import *
from bruhanimate import images


def pan_render(screen, img, frames=500, time=0, effect_type="static", background=" ", transparent=False, shift_rate=1, loop=False):

    # CREATE THE RENDERER
    renderer = PanRenderer(screen, frames, time, img, effect_type, background, transparent, "h", shift_rate, loop)
    # renderer = CenterRenderer(screen, frames, time, img, effect_type, background, transparent)

    # CHANGE THE INTENSITY
    if effect_type in ["stars", "noise"]:
        renderer.effect.update_intensity(100)


    # RUN
    renderer.run(end_message=True)


    # [Enter] TO EXIT
    input()


WinScreen.show(pan_render, args=(images.get_image("COMPUTER"), 500, 0.02, "stars", " ", True, 1, False))