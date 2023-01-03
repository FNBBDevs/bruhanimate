import sys
if sys.platform == 'win32':
    from bruhanimate.bruhscreen import WinScreen
else:
    from bruhanimate.bruhscreen import UnixScreen
from bruhanimate.bruheffects    import BaseEffect, StaticEffect, OffsetEffect, NoiseEffect, StarEffect, PlasmaEffect, GameOfLifeEffect, RainEffect
from bruhanimate.bruhffer       import Buffer
from bruhanimate.bruhrenderer   import BaseRenderer, EffectRenderer, CenterRenderer, PanRenderer
from bruhanimate import images

__all__ = [ 
    "BaseEffect",
    "StaticEffect",
    "OffsetEffect", 
    "NoiseEffect", 
    "StarEffect",
    "PlasmaEffect",
    "GameOfLifeEffect",
    "RainEffect",
    "Buffer",
    "BaseRenderer",
    "EffectRenderer",
    "CenterRenderer",
    "PanRenderer",
    "images"
]

if sys.platform == "win32":
    __all__.append("WinScreen")
else:
    __all__.append("UnixScreen")