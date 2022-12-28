from bruhanimate import WinScreen
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

class Buffer:
    def __init__(self, height, width):
        self._height = height
        self._width = width
        line = [u" " for _ in range(self._width)]
        self.buffer = [line[:] for _ in range(self._height)]
    

    def get_buffer_changes(self, in_buf):
        """
        General application is front.get_changes(back)
        """
        res = []
        if  self._height != len(in_buf.buffer) or self._width != len(in_buf.buffer[0]):
            return None
        for y in range(self._height):
            for x in range(self._width):
                if self.buffer[y][x] != in_buf.buffer[y][x]:
                    res.append((x, y, in_buf.buffer[y][x]))
        return res

    def clear_buffer(self, x=0, y=0, w=None, h=None):
        width = w if w else self._width
        height = h if h else self._height
        line = [u" " for _ in range(width)]

        if x == 0 and y == 0 and not w and not y:
            self.buffer = [line[:] for _ in range(height)]
        else:
            for i in range(y, y + height):
                self.buffer[i][x:x + width] = line[:]

    def get_char(self, x, y):
        return self.buffer[y][x]

    def put_char(self, x, y, val):
        if 0 <= y < self._height and 0 <= x < self._width:
            self.buffer[y][x] = val
        else:
            return

    def grab_chunk(self, x, y, width):
        return self.buffer[y][x:x+width]

    def sync_with(self, in_buf):
        self.buffer = [line[:] for line in in_buf.buffer]

    def height(self):
        return self._height

    def width(self):
        return self._width


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
    
    screen.print_center("Frames Are Done - Press Enter", screen.height - 2, len("Frames Are Done - Press Enter"))


WinScreen.wrapper(center_renderer, args=(50, 0.2, "#", computer,))