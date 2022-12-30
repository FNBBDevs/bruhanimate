from bruhscreen import WinScreen
from bruhrenderer import *

bruh2_0 = [
    r"loading BRUH SHELL 2.0 loading BRUH SHELL 2.0 loading BRUH ",
    r"loading BRUH SHELL 2.0 loading BRUH SHELL 2.0 loading BRUH ",
    r"loading BRUH SHELL 2.0 loading BRUH SHELL 2.0 loading BRUH ",
    r"loading BRUH         _             _           oading BRUH ",
    r"loading BRUH       /\ \          / /\          oading BRUH ",
    r"loading BRUH      /  \ \        / /  \         oading BRUH ",
    r"loading BRUH     / /\ \ \      / / /\ \        oading BRUH ",
    r"loading BRUH     \/_/\ \ \    / / /\ \ \       oading BRUH ",
    r"loading BRUH         / / /   /_/ /  \ \ \      oading BRUH ",
    r"loading BRUH        / / /    \ \ \   \ \ \     oading BRUH ",
    r"loading BRUH       / / /  _   \ \ \   \ \ \    oading BRUH ",
    r"loading BRUH      / / /_/\_\ _ \ \ \___\ \ \   oading BRUH ",
    r"loading BRUH     / /_____/ //\_\\ \/____\ \ \  oading BRUH ",
    r"loading BRUH     \________/ \/_/ \_________\/  oading BRUH ",
    r"loading BRUH                                   oading BRUH ",
    r"loading BRUH SHELL 2.0 loading BRUH SHELL 2.0 loading BRUH ",
    r"loading BRUH SHELL 2.0 loading BRUH SHELL 2.0 loading BRUH ",
    r"loading BRUH SHELL 2.0 loading BRUH SHELL 2.0 loading BRUH ",
]
bruh2_0_2 = [
    r"    _             _          ",
    r"  /\ \          / /\         ",
    r" /  \ \        / /  \        ",
    r"/ /\ \ \      / / /\ \       ",
    r"\/_/\ \ \    / / /\ \ \      ",
    r"    / / /   /_/ /  \ \ \     ",
    r"   / / /    \ \ \   \ \ \    ",
    r"  / / /  _   \ \ \   \ \ \   ",
    r" / / /_/\_\ _ \ \ \___\ \ \  ",
    r"/ /_____/ //\_\\ \/____\ \ \ ",
    r"\________/ \/_/ \_________\/ ",
]
computer = [
    f"                       .,,uod8B8bou,,.                             ",
    f"              ..,uod8BBBBBBBBBBBBBBBBRPFT?l!i:.                    ",
    f"         ,=m8BBBBBBBBBBBBBBBRPFT?!||||||||||||||                   ",
    f"         !...:!TVBBBRPFT||||||||||!!^^\"\"'    |||                   ",
    f"         !.......:!?|||||!!^^\"\"'             |||                   ",
    f"         !.........|||   ___ ___ _   _ _  _  |||                   ",
    f"         !.........|||  | _ ) _ \ | | | || | |||                   ",
    f"         !.........|||  | _ \   / |_| | __ | |||                   ",
    f"         !.........|||  |___/_|_\\\___/|_||_| |||                   ",
    f"         !.........|||   ---   --            |||                   ",
    f"         !.........|||  |_  ) /  \           |||                   ",
    f"         `.........|||   / / | () |        , |||                   ",
    f"          .;.......|||  /___(_)__/     _.-!!||||                   ",
    f"   .,uodWBBBBb.....|||        _.-!!|||||||||!:'                    ",
    f"!YBBBBBBBBBBBBBBb..!|||:..-!!|||||||!iof68BBBBBb....               ",
    f"!..YBBBBBBBBBBBBBBb!!||||||||!iof68BBBBBBRPFT?!::   `.             ",
    f"!....YBBBBBBBBBBBBBBbaaitf68BBBBBBRPFT?!:::::::::     `.           ",
    f"!......YBBBBBBBBBBBBBBBBBBBRPFT?!::::::;:!^\"`;:::       `.         ",
    f"!........YBBBBBBBBBBRPFT?!::::::::::^''...::::::;         iBBbo.   ",
    f"`..........YBRPFT?!::::::::::::::::::::::::;iof68bo.      WBBBBbo. ",
    f"  `..........:::::::::::::::::::::::;iof688888888888b.     `YBBBP^'",
    f"    `........::::::::::::::::;iof688888888888888888888b.     `     ",
    f"      `......:::::::::;iof688888888888888888888888888888b.         ",
    f"        `....:::;iof688888888888888888888888888888888899fT!        ",
    f"          `..::!8888888888888888888888888888888899fT|!^\"'          ",
    f"            `' !!988888888888888888888888899fT|!^\"'                ",
    f"                `!!8888888888888888899fT|!^\"'                      ",
    f"                  `!988888888899fT|!^\"'                            ",
    f"                    `!9899fT|!^\"'                                  ",
    f"                      `!^\"'                                        "
]
hey = [
  f"    __  __          ",
  f"   / / / /__  __  __",
  f"  / /_/ / _ \/ / / /",
  f" / __  /  __/ /_/ / ",
  f"/_/ /_/\___/\__, /  ",
  f"           /____/   "
]


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
    renderer.set_exit_stats("  Animation Frames Completed  ", "    Press [Enter] to leave    ", wipe=True)

    # RUN
    renderer.run()

    # [Enter] TO MOVE ON
    input()




if __name__ == "__main__":
    FRAMES = 1000

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