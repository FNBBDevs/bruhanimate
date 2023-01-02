from bruhanimate.bruhscreen import WinScreen
from bruhanimate.bruhrenderer import *
from bruhanimate import images


def effect(screen, frames=500, time=0, background=" ", transparent=False):

    # CREATE THE RENDERERS AND RENDERER ATTRIBUTES
    static_renderer = EffectRenderer(screen, frames, time, "static", background, transparent)

    offset_renderer = EffectRenderer(screen, frames, time, "offset", background, transparent)

    stars_renderer = EffectRenderer(screen, frames, time, "stars", " ", transparent)

    noise_renderer = EffectRenderer(screen, frames, time, "noise", " ", transparent)
    noise_renderer.effect.update_intensity(10)

    plasma_renderer = EffectRenderer(screen, frames, time, "plasma", " ", transparent)

    gol_renderer = EffectRenderer(screen, frames, time, "gol", " ", transparent)
    gol_renderer.effect.set_decay(True)

    # RUN
    static_renderer.run(end_message=False)
    screen.clear()

    offset_renderer.effect.update_direction("left")
    offset_renderer.run(end_message=False)
    offset_renderer.effect.update_direction("right")
    offset_renderer.run(end_message=False)
    screen.clear()

    stars_renderer.run(end_message=False)
    screen.clear()

    noise_renderer.run(end_message=False)
    screen.clear()

    plasma_renderer.run(end_message=False)
    screen.clear()

    gol_renderer.run(end_message=True)


    # [Enter] TO EXIT
    input()
    print(f"PLASMA VALS: {plasma_renderer.effect.vals}")

def center(screen, img, frames=500, time=0, effect_type="static", background=" ", transparent=False):
    pass

def pan(screen, img, frames=500, time=0, effect_type="static", background=" ", transparent=False, direction="h", shift=1, loop=False):
    pass

WinScreen.show(effect, args=(250, 0, "hello world, what is up?", None))