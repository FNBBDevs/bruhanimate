from bruhanimate import WinScreen
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

def center_renderer(screen, frames, time, background, img):
    width, height = screen.width, screen.height
    img_width, img_height = len(img[0]), len(img)

    back = Buffer(height, width)
    front = Buffer(height, width)

    for _ in range(frames):
        sleep(time)
        back.put_char(_, _, " ")
        back.put_char(_ + 1, _ + 1, "#")
        updates = front.get_buffer_changes(back)
        if not updates:
            continue
        else:
            for update in updates:
                screen.print_at(update[2], update[0], update[1], 1)
            front.sync_with(back)
    front.clear_buffer()
    
    screen.print_center("Frames Are Done - Press Enter", screen.height - 2, len("Frames Are Done - Press Enter"))


WinScreen.wrapper(center_renderer, args=(20, 0.2, "#", computer,))