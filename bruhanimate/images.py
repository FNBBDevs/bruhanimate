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

BRUH       = [r"loading BRUH SHELL 2.0 loading BRUH SHELL 2.0 loading BRUH ",r"loading BRUH SHELL 2.0 loading BRUH SHELL 2.0 loading BRUH ",r"loading BRUH SHELL 2.0 loading BRUH SHELL 2.0 loading BRUH ",r"loading BRUH         _             _           oading BRUH ",r"loading BRUH       /\ \          / /\          oading BRUH ",r"loading BRUH      /  \ \        / /  \         oading BRUH ",r"loading BRUH     / /\ \ \      / / /\ \        oading BRUH ",r"loading BRUH     \/_/\ \ \    / / /\ \ \       oading BRUH ",r"loading BRUH         / / /   /_/ /  \ \ \      oading BRUH ",r"loading BRUH        / / /    \ \ \   \ \ \     oading BRUH ",r"loading BRUH       / / /  _   \ \ \   \ \ \    oading BRUH ",r"loading BRUH      / / /_/\_\ _ \ \ \___\ \ \   oading BRUH ",r"loading BRUH     / /_____/ //\_\\ \/____\ \ \  oading BRUH ",r"loading BRUH     \________/ \/_/ \_________\/  oading BRUH ",r"loading BRUH                                   oading BRUH ",r"loading BRUH SHELL 2.0 loading BRUH SHELL 2.0 loading BRUH ",r"loading BRUH SHELL 2.0 loading BRUH SHELL 2.0 loading BRUH ",r"loading BRUH SHELL 2.0 loading BRUH SHELL 2.0 loading BRUH ",]
BRUH_EMPTY = [r"    _             _          ",r"  /\ \          / /\         ",r" /  \ \        / /  \        ",r"/ /\ \ \      / / /\ \       ",r"\/_/\ \ \    / / /\ \ \      ",r"    / / /   /_/ /  \ \ \     ",r"   / / /    \ \ \   \ \ \    ",r"  / / /  _   \ \ \   \ \ \   ",r" / / /_/\_\ _ \ \ \___\ \ \  ",r"/ /_____/ //\_\\ \/____\ \ \ ",r"\________/ \/_/ \_________\/ ",]
COMPUTER   = [f"                       .,,uod8B8bou,,.                             ",    f"              ..,uod8BBBBBBBBBBBBBBBBRPFT?l!i:.                    ",    f"         ,=m8BBBBBBBBBBBBBBBRPFT?!||||||||||||||                   ",    f"         !...:!TVBBBRPFT||||||||||!!^^\"\"'    |||                   ",f"         !.......:!?|||||!!^^\"\"'             |||                   ",f"         !.........|||   ___ ___ _   _ _  _  |||                   ", f"         !.........|||  | _ ) _ \ | | | || | |||                   ",f"         !.........|||  | _ \   / |_| | __ | |||                   ",f"         !.........|||  |___/_|_\\\___/|_||_| |||                   ",f"         !.........|||   ---   --            |||                   ",f"         !.........|||  |_  ) /  \           |||                   ",f"         `.........|||   / / | () |        , |||                   ",f"          .;.......|||  /___(_)__/     _.-!!||||                   ",f"   .,uodWBBBBb.....|||        _.-!!|||||||||!:'                    ",f"!YBBBBBBBBBBBBBBb..!|||:..-!!|||||||!iof68BBBBBb....               ",f"!..YBBBBBBBBBBBBBBb!!||||||||!iof68BBBBBBRPFT?!::   `.             ",f"!....YBBBBBBBBBBBBBBbaaitf68BBBBBBRPFT?!:::::::::     `.           ",f"!......YBBBBBBBBBBBBBBBBBBBRPFT?!::::::;:!^\"`;:::       `.         ",f"!........YBBBBBBBBBBRPFT?!::::::::::^''...::::::;         iBBbo.   ",f"`..........YBRPFT?!::::::::::::::::::::::::;iof68bo.      WBBBBbo. ",f"  `..........:::::::::::::::::::::::;iof688888888888b.     `YBBBP^'",f"    `........::::::::::::::::;iof688888888888888888888b.     `     ",f"      `......:::::::::;iof688888888888888888888888888888b.         ", f"        `....:::;iof688888888888888888888888888888888899fT!        ",f"          `..::!8888888888888888888888888888888899fT|!^\"'          ",f"            `' !!988888888888888888888888899fT|!^\"'                ",f"                `!!8888888888888888899fT|!^\"'                      ",f"                  `!988888888899fT|!^\"'                            ",f"                    `!9899fT|!^\"'                                  ",f"                      `!^\"'                                        "]
HEY        = [f"    __  __          ",f"   / / / /__  __  __",f"  / /_/ / _ \/ / / /",f" / __  /  __/ /_/ / ",f"/_/ /_/\___/\__, /  ",f"           /____/   "]

_REGISTERED_IMAGES = {
    "BRUH": BRUH, 
    "BRUH_EMPTY": BRUH_EMPTY, 
    "COMPUTER": COMPUTER, 
    "HEY": HEY,
}


def get_image(name):
    if name in _REGISTERED_IMAGES:
        return _REGISTERED_IMAGES[name]
    else:
        return _REGISTERED_IMAGES["HEY"]
