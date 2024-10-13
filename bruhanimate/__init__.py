import sys


if sys.platform == "win32":
    from .bruheffect import AudioEffect
    from .demos import audio_demo


from .bruheffect import (
    BaseEffect,
    StaticEffect,
    OffsetEffect,
    NoiseEffect,
    StarEffect,
    PlasmaEffect,
    GameOfLifeEffect,
    RainEffect,
    MatrixEffect,
    ChatbotEffect,
    GradientNoise,
    Loading,
    StringStreamer,
    Key,
    Line,
    DrawLinesEffect,
    SnowEffect,
    TwinkleEffect,
    TWINKLE_SPEC,
)


from .bruhutil import (
    Screen,
    Buffer,
    bruhimage,
    get_image,
    text_to_image,
    LIFE_COLORS,
    LIFE_SCALES,
    PLASMA_COLORS,
    PLASMA_VALUES,
    GRADIENTS,
    VALID_DIRECTIONS,
    OLD_GREY_SCALES,
    GREY_SCALES,
    WIND_DIRECTIONS,
    NOISE,
    SNOWFLAKE_COLORS,
    FLAKE_WEIGHT_CHARS,
    TWINKLE_COLORS,
    VALID_INTERFACES,
    SNOWFLAKE_TYPES
)

from .bruhrenderer import (
    BaseRenderer,
    EffectRenderer,
    CenterRenderer,
    PanRenderer,
    FocusRenderer,
    BackgroundColorRenderer,
)

from .demos import (
    line_demo,
    plasma_demo,
    snow_demo,
    holiday,
    stars_demo,
    twinkle_demo,
    noise_demo,
    matrix_demo,
    gol_demo,
    rain_demo,
    offset_demo,
    static_demo,
    chatbot_demo,
)


__version__ = "0.2.66"
__valid_demos__ = [
    "static_demo",
    "offset_demo",
    "matrix_demo",
    "gol_demo",
    "rain_demo",
    "chatbot_demo" "line_demo",
    "plasma_demo",
    "snow_demo",
    "stars_demo",
    "twinkle_demo",
    "noise_demo" "holiday",
]

if sys.platform == "win32":
    __valid_demos__.append("audio_demo")


if sys.platform == "win32":
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
        "audio_demo",
        "chatbot_demo",
        "AudioEffect",
        "BaseEffect",
        "StaticEffect",
        "OffsetEffect",
        "NoiseEffect",
        "StarEffect",
        "PlasmaEffect",
        "GameOfLifeEffect",
        "RainEffect",
        "MatrixEffect",
        "ChatbotEffect",
        "StringStreamer",
        "GradientNoise",
        "Loading",
        "Key",
        "DrawLinesEffect",
        "Line",
        "FLAKE",
        "SnowEffect",
        "Buffer",
        "BaseRenderer",
        "EffectRenderer",
        "CenterRenderer",
        "PanRenderer",
        "FocusRenderer",
        "BackgroundColorRenderer",
        "bruhimage",
        "__version__",
        "__valid_demos__",
        "LIFE_COLORS",
        "LIFE_SCALES",
        "PLASMA_COLORS",
        "PLASMA_VALUES",
        "GRADIENTS",
        "VALID_DIRECTIONS",
        "OLD_GREY_SCALES",
        "GREY_SCALES",
        "WIND_DIRECTIONS",
        "NOISE",
        "SNOWFLAKE_COLORS",
        "SNOWFLAKE_TYPES",
        "FLAKE_WEIGHT_CHARS",
        "TWINKLE_COLORS",
        "VALID_INTERFACES",
        "get_image",
        "text_to_image",
        "TwinkleEffect",
        "TWINKLE_SPEC",
    ]
else:
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
        "chatbot_demo",
        "BaseEffect",
        "StaticEffect",
        "OffsetEffect",
        "NoiseEffect",
        "StarEffect",
        "PlasmaEffect",
        "GameOfLifeEffect",
        "RainEffect",
        "MatrixEffect",
        "ChatbotEffect",
        "StringStreamer",
        "GradientNoise",
        "Loading",
        "Key",
        "DrawLinesEffect",
        "Line",
        "FLAKE",
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
        "__valid_demos__",
        "LIFE_COLORS",
        "LIFE_SCALES",
        "PLASMA_COLORS",
        "PLASMA_VALUES",
        "GRADIENTS",
        "VALID_DIRECTIONS",
        "OLD_GREY_SCALES",
        "GREY_SCALES",
        "WIND_DIRECTIONS",
        "NOISE",
        "FLAKES",
        "FLAKE_COLORS",
        "FLAKE_JUMPS",
        "NEXT_FLAKE_MOVE",
        "FLAKE_WEIGHT_CHARS",
        "FLAKE_FLIPS",
        "TWINKLE_COLORS",
        "VALID_INTERFACES",
        "get_image",
        "text_to_image",
        "TwinkleEffect",
        "TWINKLE_SPEC",
    ]

