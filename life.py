from bruhanimate.bruhrenderer import EffectRenderer
from bruhanimate.bruhscreen import WinScreen 

def life(screen, frames, time, effect, background, transparent):    
    gol_renderer = EffectRenderer(screen, frames, time, "gol", " ", transparent)
    gol_renderer.effect.set_decay(True, "RAINBOW_r")
    gol_renderer.run()
    input()

WinScreen.show(life, args=(400, 0, None, " ", False))