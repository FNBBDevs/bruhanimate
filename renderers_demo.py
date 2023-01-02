from bruhanimate.bruhscreen import WinScreen
from bruhanimate.bruhrenderer import *
from bruhanimate import images


def gol_render(screen, img, frames=500, time=0, effect_type="static", background=" ", transparent=False):

    # CREATE THE RENDERER
    renderer = CenterRenderer(screen, frames, time, img, effect_type, background, transparent)
    
    # ENABLE DECCAY
    # renderer.effect.set_decay(True)

    # RUN
    renderer.run(end_message=True)


    # [Enter] TO EXIT
    input()


WinScreen.show(gol_render, args=(images.get_image("COMPUTER"), 500, 0, "gol", " ", True))