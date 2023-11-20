"""
Copyright 2023 Ethan Christensen

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import re
import random
import pyfiglet
import bruhcolor

BRUH = [r"loading BRUH SHELL 2.0 loading BRUH SHELL 2.0 loading BRUH ", r"loading BRUH SHELL 2.0 loading BRUH SHELL 2.0 loading BRUH ", r"loading BRUH SHELL 2.0 loading BRUH SHELL 2.0 loading BRUH ", r"loading BRUH         _             _           oading BRUH ", r"loading BRUH       /\ \          / /\          oading BRUH ", r"loading BRUH      /  \ \        / /  \         oading BRUH ", r"loading BRUH     / /\ \ \      / / /\ \        oading BRUH ", r"loading BRUH     \/_/\ \ \    / / /\ \ \       oading BRUH ", r"loading BRUH         / / /   /_/ /  \ \ \      oading BRUH ",
        r"loading BRUH        / / /    \ \ \   \ \ \     oading BRUH ", r"loading BRUH       / / /  _   \ \ \   \ \ \    oading BRUH ", r"loading BRUH      / / /_/\_\ _ \ \ \___\ \ \   oading BRUH ", r"loading BRUH     / /_____/ //\_\\ \/____\ \ \  oading BRUH ", r"loading BRUH     \________/ \/_/ \_________\/  oading BRUH ", r"loading BRUH                                   oading BRUH ", r"loading BRUH SHELL 2.0 loading BRUH SHELL 2.0 loading BRUH ", r"loading BRUH SHELL 2.0 loading BRUH SHELL 2.0 loading BRUH ", r"loading BRUH SHELL 2.0 loading BRUH SHELL 2.0 loading BRUH ",]
BRUH_EMPTY = [r"    _             _          ", r"  /\ \          / /\         ", r" /  \ \        / /  \        ", r"/ /\ \ \      / / /\ \       ", r"\/_/\ \ \    / / /\ \ \      ",
              r"    / / /   /_/ /  \ \ \     ", r"   / / /    \ \ \   \ \ \    ", r"  / / /  _   \ \ \   \ \ \   ", r" / / /_/\_\ _ \ \ \___\ \ \  ", r"/ /_____/ //\_\\ \/____\ \ \ ", r"\________/ \/_/ \_________\/ ",]
COMPUTER = [f"                       .,,uod8B8bou,,.                             ",    f"              ..,uod8BBBBBBBBBBBBBBBBRPFT?l!i:.                    ",    f"         ,=m8BBBBBBBBBBBBBBBRPFT?!||||||||||||||                   ",    f"         !...:!TVBBBRPFT||||||||||!!^^\"\"'    |||                   ", f"         !.......:!?|||||!!^^\"\"'             |||                   ", f"         !.........|||   ___ ___ _   _ _  _  |||                   ", f"         !.........|||  | _ ) _ \ | | | || | |||                   ", f"         !.........|||  | _ \   / |_| | __ | |||                   ", f"         !.........|||  |___/_|_\\\___/|_||_| |||                   ", f"         !.........|||   ---   --            |||                   ", f"         !.........|||  |_  ) /  \           |||                   ",
            f"         `.........|||   / / | () |        , |||                   ", f"          .;.......|||  /___(_)__/     _.-!!||||                   ", f"   .,uodWBBBBb.....|||        _.-!!|||||||||!:'                    ", f"!YBBBBBBBBBBBBBBb..!|||:..-!!|||||||!iof68BBBBBb....               ", f"!..YBBBBBBBBBBBBBBb!!||||||||!iof68BBBBBBRPFT?!::   `.             ", f"!....YBBBBBBBBBBBBBBbaaitf68BBBBBBRPFT?!:::::::::     `.           ", f"!......YBBBBBBBBBBBBBBBBBBBRPFT?!::::::;:!^\"`;:::       `.         ", f"!........YBBBBBBBBBBRPFT?!::::::::::^''...::::::;         iBBbo.   ", f"`..........YBRPFT?!::::::::::::::::::::::::;iof68bo.      WBBBBbo. ", f"  `..........:::::::::::::::::::::::;iof688888888888b.     `YBBBP^'", f"    `........::::::::::::::::;iof688888888888888888888b.     `     ", f"      `......:::::::::;iof688888888888888888888888888888b.         ", f"        `....:::;iof688888888888888888888888888888888899fT!        ", f"          `..::!8888888888888888888888888888888899fT|!^\"'          ", f"            `' !!988888888888888888888888899fT|!^\"'                ", f"                `!!8888888888888888899fT|!^\"'                      ", f"                  `!988888888899fT|!^\"'                            ", f"                    `!9899fT|!^\"'                                  ", f"                      `!^\"'                                        "]
HEY = [f"    __  __          ", f"   / / / /__  __  __", f"  / /_/ / _ \/ / / /",
       f" / __  /  __/ /_/ / ", f"/_/ /_/\___/\__, /  ", f"           /____/   "]
TWOPOINT = [r"                                                                               ",      r"   ____________ _   _ _   _  _____ _   _  _____ _      _       _____  _____    ", r"   | ___ \ ___ \ | | | | | |/  ___| | | ||  ___| |    | |     / __  \|  _  |   ", r"   | |_/ / |_/ / | | | |_| |\ `--.| |_| || |__ | |    | |     `' / /'| |/' |   ",
            r"   | ___ \    /| | | |  _  | `--. \  _  ||  __|| |    | |       / /  |  /| |   ", r"   | |_/ / |\ \| |_| | | | |/\__/ / | | || |___| |____| |____ ./ /___\ |_/ /   ", r"   \____/\_| \_|\___/\_| |_/\____/\_| |_/\____/\_____/\_____/ \_____(_)___/    ", r"                                                                               "]

CHRISTMAS_1 = [
    "               ",
    "     _\/_      ",
    "      /\       ",
    "      /\\       ",
    "     /  \\      ",
    "     /~~\\ o    ",
    "    / o  \\     ",
    "   /~~*~~~\\    ",
    " o /    o \\    ",
    "  /~~~~~~~~\\~` ",
    " /__*_______\\  ",
    "      ||       ",
    "    \\====/     ",
    "     \\__/      ",
    "               "]


_REGISTERED_IMAGES = {
    "BRUH": BRUH,
    "BRUH_EMPTY": BRUH_EMPTY,
    "COMPUTER": COMPUTER,
    "HEY": HEY,
    "TWOPOINT": TWOPOINT,
    "CHRISTMAS_1": CHRISTMAS_1
}

def get_image(name):
    if name in _REGISTERED_IMAGES:
        return _REGISTERED_IMAGES[name]
    else:
        return _REGISTERED_IMAGES["HEY"]


def text_to_image(text, font=pyfiglet.DEFAULT_FONT, padding_top_bottom=0, padding_left_right=0):
    img_flat = None
    try:
        img_flat = pyfiglet.Figlet(font).renderText(text)
    except:
        img_flat = pyfiglet.Figlet().renderText("Invalid Font")
    img = []
    row = ""
    for val in img_flat:
        if val == "\n":
            img.append(row)
            row = ""
        else:
            row+=val
    
    if padding_top_bottom > 0:
        img = [" "*len(img[0])for __ in range(padding_top_bottom)] + img + [" "*len(img[0])for __ in range(padding_top_bottom)]
    if padding_left_right > 0:
        for i in range(len(img)):
            img[i] = (" "*padding_left_right) + img[i] + (" "*padding_left_right)
    return img
