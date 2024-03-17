import os

here = os.path.abspath(os.path.dirname(__file__))

from bruhanimate.bruhscreen import Screen
from bruhanimate.bruheffects import (
    BaseEffect,
    StaticEffect,
    OffsetEffect,
    NoiseEffect,
    StarEffect,
    PlasmaEffect,
    GameOfLifeEffect,
    RainEffect,
    MatrixEffect,
    Line,
    DrawLines,
    _FLAKE,
    SnowEffect,
)
from bruhanimate.bruhffer import Buffer
from bruhanimate.bruhrenderer import (
    BaseRenderer,
    EffectRenderer,
    CenterRenderer,
    PanRenderer,
    FocusRenderer,
    BackgroundColorRenderer,
)
from bruhanimate import images
from bruhanimate.demos import line_demo, plasma_demo, snow_demo, holiday, stars_demo, twinkle_demo, noise_demo, matrix_demo, gol_demo, rain_demo, offset_demo, static_demo

__version__ = "0.2.31"
__valid_demos__ = [demo.split(".")[0] for demo in os.listdir(os.path.join(here, "demos")) if "init" not in demo and "pycache" not in demo]

__all__ = [
    "Screen",
    "plasma_demo",
    "line_demo",
    "holiday",
    "snow_demo",
    "stars_demo",
    "twinkle_demo",
    "noise_demo",
    "matrix_demo",
    "gol_demo",
    "rain_demo",
    "offset_demo",
    "static_demo",
    "BaseEffect",
    "StaticEffect",
    "OffsetEffect",
    "NoiseEffect",
    "StarEffect",
    "PlasmaEffect",
    "GameOfLifeEffect",
    "RainEffect",
    "MatrixEffect",
    "DrawLines",
    "Line",
    "_FLAKE",
    "SnowEffect",
    "Buffer",
    "BaseRenderer",
    "EffectRenderer",
    "CenterRenderer",
    "PanRenderer",
    "FocusRenderer",
    "BackgroundColorRenderer",
    "images",
    "__version__",
    "__valid_demos__"
]
