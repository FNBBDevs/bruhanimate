from bruhanimate.bruhscreen import WinScreen
from bruhanimate.bruhrenderer import *


def gol_render(screen, frames, time, effect, background, transparent):
    """
    Testing just an effect
    """
    # SETUP
    renderer = EffectRenderer(screen, frames, time, effect, background, transparent)

    # RUN
    renderer.run(end_message=True)

    # [Enter] TO MOVE ON
    input()


def plasma_render(screen, frames, time, effect, background, transparent):
    """
    Testing just an effect
    """
    # SETUP
    renderer = EffectRenderer(screen, frames, time, effect, background, transparent)

    # RUN
    renderer.run(end_message=False)


def noise_render(screen, frames, time, effect, background, transparent):
    """
    Testing just rendering an effect
    """
    # SETUP
    renderer = EffectRenderer(screen, frames, time, effect, background, transparent)

    # REDUCE INTENSITY FOR FASTER RENDER
    renderer.effect.update_intensity(1)

    # RUN
    renderer.run(end_message=False)


def stars_render(screen, frames, time, effect, background, transparent):
    """
    Testing just rendering an effect
    """
    # SETUP
    renderer = EffectRenderer(screen, frames, time, effect, background, transparent)

    # REDUCE INTENSITY FOR FASTER RENDER
    renderer.effect.update_intensity(1)

    # RUN
    renderer.run(end_message=False)


def static_render(screen, frames, time, effect, background, transparent):
    """
    Testing just rendering an effect
    """
    # SETUP
    renderer = EffectRenderer(screen, frames, time, effect, background, transparent)

    # RUN
    renderer.run(end_message=False)


def offset_render(screen, frames, time, effect, background, transparent):
    """
    Testing just rendering an effect
    """
    # SETUP
    renderer = EffectRenderer(screen, frames, time, effect, background, transparent)

    # RUN
    renderer.run(end_message=False)

    # CHANGE THE DIRECTION
    renderer.effect.update_direction("left")

    # CHANGE THE END MESSAGES
    renderer.set_exit_stats("  Animation Frames Completed  ", "    Press [Enter] to leave    ", wipe=False)

    # RUN
    renderer.run()

    # [Enter] TO MOVE ON
    input()


def main():

    FRAMES = 500

    # TESTING GOL
    WinScreen.show(gol_render, args=(FRAMES, 0, "gol", " ", None))

    # TESTING NOISE
    WinScreen.show(noise_render, args=(FRAMES, 0, "noise", " ", None))

    # TESTING STARS
    WinScreen.show(stars_render, args=(FRAMES, 0, "stars", " ", None))

    # TESTING PLASMA
    WinScreen.show(plasma_render, args=(100, 0, 'plasma', " ", None))

    # TESTING STATIC
    WinScreen.show(static_render, args=(FRAMES, 0, "static", ".-._", None))

    # TESTING OFFSET
    WinScreen.show(offset_render, args=(FRAMES, 0, "offset", "..--..__", None))


if __name__ == "__main__":
    main()