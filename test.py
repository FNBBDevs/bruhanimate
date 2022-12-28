from bruhscreen import WinScreen
from bruhrenderer import *
from bruhffer import Buffer
import sys
import os
import time
import random

def sleep(s):
    sys.stdout.flush()
    time.sleep(s)

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


def render(screen, frames, time, background, img):
    renderer = CenterRenderer(screen, frames, time, background, img)
    renderer.run()


WinScreen.wrapper(render, args=(20, 0.2, "#", computer,))