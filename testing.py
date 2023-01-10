from bruhanimate.bruhscreen import *
from bruhanimate.bruhrenderer import *
from bruhanimate import images
import sys


def test(screen, frames, time, effect, background, transparent):

    print(f"\nSCREEN INFORMATION --> WIDTH: {screen.width}\tHEIGHT: {screen.height}")

    renderer = EffectRenderer(screen, frames, time, effect, background, transparent)

    l = 19
    o = l//2
    if l % 2 == 0:
        l += 1

    sx = ((screen.width-1) // 2) - (l // 2)
    sy = (screen.height // 2) - (l // 2)

    print(sx, sy)

    
    renderer.effect.add_line((sx, sy), (sx+l-1, sy))
    renderer.effect.add_line((sx, sy), (sx, sy+l-1))
    renderer.effect.add_line((sx+l-1, sy), (sx+l-1, sy+l-1))
    renderer.effect.add_line((sx, sy+l-1), (sx+l-1, sy+l-1))

    renderer.effect.add_line((sx+o, sy+o), (sx+l+o-1, sy+o))
    renderer.effect.add_line((sx+o, sy+o), (sx+o, sy+l+o-1))
    renderer.effect.add_line((sx+l+o-1, sy+o), (sx+l+o-1, sy+l+o-1))
    renderer.effect.add_line((sx+o, sy+l+o-1), (sx+l+o-1, sy+l+o-1))

    renderer.effect.add_line((sx, sy), (sx+o, sy+o))
    renderer.effect.add_line((sx, sy+l), (sx+o, sy+l+o-1))
    renderer.effect.add_line((sx+l, sy), (sx+l+o-1, sy+o))
    renderer.effect.add_line((sx+l, sy+l), (sx+l+o-1, sy+l+o-1))

    renderer.run()

    input()

WinScreen.show(test, args=(20, 0.05, "drawlines", " ", True))