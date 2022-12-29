from bruhscreen import WinScreen
from bruhrenderer import *
from bruhffer import Buffer

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


def render(screen, frames, time, background, img):

    # Create the renderer
    renderer = CenterRenderer(screen, frames, time, background, img)

    # Edit the exit messages
    renderer.set_exit_stats(msg1="  Animation is Complete  ", msg2="  Press [Enter] to Exit  ", wipe=False)

    # Set the padding on the image
    renderer.set_padding([4, 2])

    # Run the frames
    renderer.run()
    


WinScreen.wrapper(render, args=(10, 0.2, ".-._", computer))

WinScreen.wrapper(render, args=(10, 0.2, ".-._", None))
