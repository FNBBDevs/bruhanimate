from bruhanimate.bruhscreen import WinScreen
from bruhanimate.bruhrenderer import *
from bruhanimate import images


def center_render(screen, img, frames=500, time=0, effect_type="static", background=" ", transparent=False):

    # CREATE THE RENDERER
    renderer = CenterRenderer(screen, frames, time, img, effect_type, background, transparent)

    # CHANGE THE INTENSITY
    if effect_type in ["stars", "noise"]:
        renderer.effect.update_intensity(10)


    # RUN
    renderer.run(end_message=True)


    # [Enter] TO EXIT
    input()


WinScreen.show(center_render, args=(images.get_image("COMPUTER"), 500, 0.01, "stars", " ", True))
