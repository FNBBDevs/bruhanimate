import sys
from .base_effect import BaseEffect
from .static_effect import StaticEffect
from .star_effect import StarEffect
from .chatbot_effect import ChatbotEffect, GradientNoise, Loading, StringStreamer, Key
from .draw_lines_effect import DrawLinesEffect, Line
from .game_of_life_effect import GameOfLifeEffect
from .matrix_effect import MatrixEffect
from .plasma_effect import PlasmaEffect
from .snow_effect import SnowEffect
from .twinkle_effect import TwinkleEffect, TWINKLE_SPEC
from .offset_effect import OffsetEffect
from .rain_effect  import RainEffect
from .noise_effect import NoiseEffect


__all__ = [
    "BaseEffect",
    "StaticEffect",
    "StarEffect",
    "ChatbotEffect",
    "DrawLinesEffect",
    "GameOfLifeEffect",
    "MatrixEffect",
    "PlasmaEffect",
    "SnowEffect",
    "TwinkleEffect",
    "OffsetEffect",
    "RainEffect",
    "NoiseEffect",
    "GradientNoise",
    "Loading",
    "StringStreamer",
    "Key", 
    "Line",
    "TWINKLE_SPEC"
]

if sys.platform == 'win32':
    from .audio_effect import AudioEffect
    __all__.append("AudioEffect")