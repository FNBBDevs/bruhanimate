from bruhanimate.bruhscreen import WinScreen
from bruhanimate.bruhrenderer import *
from bruhanimate import images


def effects(screen, frames=500, time=0, background=" ", transparent=False):

    # CREATE THE RENDERERS AND RENDERER ATTRIBUTES

    static_renderer = EffectRenderer(screen, frames, time, "static", background, transparent)

    offset_renderer = EffectRenderer(screen, frames, time, "offset", background, transparent)

    stars_renderer = EffectRenderer(screen, frames, time, "stars", " ", transparent)

    noise_renderer = EffectRenderer(screen, frames, time, "noise", " ", transparent)
    noise_renderer.effect.update_intensity(10)

    plasma_renderer = EffectRenderer(screen, frames, time, "plasma", " ", transparent)
    plasma_renderer.effect.update_plasma_values(15, 26, 19, 41)

    rain_renderer = EffectRenderer(screen, frames, 0.03, "rain", " ", transparent)
    rain_renderer.update_smart_transparent(True)
    rain_renderer.update_collision(True)
    print(rain_renderer.effect.collision)
    rain_renderer.effect.update_intensity(900)

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

    rain_renderer.run()
    screen.clear()

    gol_renderer.run(end_message=True)

    # [Enter] TO EXIT
    input()


def center(screen, img, frames=500, time=0, effect_type="static", background=" ", transparent=False):

    # SETUP
    renderer = CenterRenderer(screen, frames, time, img, effect_type, background, transparent)
    renderer.effect.set_decay(True)

    if effect_type == "plasma":
        renderer.effect.update_plasma_values(10, 26, 19, 41)
    if effect_type == "gol":
        renderer.update_smart_transparent(True)

    # RUN
    renderer.run(end_message=True)

    # [Enter] TO MOVE ON
    input()


def pan(screen, img, frames=500, time=0, effect_type="static", background=" ", transparent=False, direction="h", shift=1, loop=False):

    # SETUP
    renderer = PanRenderer(screen, frames, time, img, effect_type, background, transparent, direction, shift, loop)

    # ATTRIBUTES
    renderer.update_smart_transparent(True)

    # RUN
    renderer.run(end_message=True)

    # [Enter] TO MOVE ON
    input()


WinScreen.show(effects, args=(250, 0, "| .:-=+*%#@#%*+=-:.  ", None))

WinScreen.show(center, args=(images.get_image("COMPUTER"), 200, 0, "gol", " ", True))

WinScreen.show(pan, args=(images.get_image("COMPUTER"), 200, 0.005, "stars", " ", True, "h", 1, True))
