import sys
import time


def sleep(s):
    sys.stdout.flush()
    time.sleep(s)


VALID_EFFECTS = ["static", "offset", "noise", "stars", "plasma", "gol", "rain", "matrix", "drawlines", "snow", "twinkle", "audio", "chat"]

HORIZONTAL = "h"

VERTICAL = "v"

INF = float("inf")

LIFE_COLORS = {
    "GREYSCALE": [232, 235, 239, 241, 244, 247, 248, 250, 254, 231],
    "GREYSCALE_r": [232, 235, 239, 241, 244, 247, 248, 250, 254, 231][::-1],
    "GREYSCALE_MUTED": [232, 235, 235, 239, 239, 241, 241, 244, 244, 231],
    "RAINBOW": [232, 202, 208, 190, 112, 27, 105, 129, 161, 231],
    "RAINBOW_r": [231, 196, 208, 190, 112, 27, 105, 129, 161, 201][::-1],
}

LIFE_SCALES = {
    "default": " .:-=+*%#@",
    ".": " .........",
    "o": " ooooooooo",
    "0": " 000000000",
}

PLASMA_COLORS = {
    2: [[232, 231]],
    8: [[150, 93, 11, 38, 181, 250, 143, 12], [142, 167, 216, 161, 59, 228, 148, 219]],
    10: [[232, 16, 53, 55, 89, 91, 126, 163, 197, 196][::-1]],
    16: [[232,16,53,55,56,89,90,91,125,126,163,199,198,197,196,39,81,231,][::-1],[195, 106, 89, 176, 162, 180, 201, 233, 124, 252, 104, 181, 2, 182, 4, 170],],
}

PLASMA_VALUES = [[43, 15, 8, 24], [15, 42, 47, 23], [35, 29, 31, 27], [10, 26, 19, 41]]

GRADIENTS = [
    [21, 57, 93, 129, 165, 201, 165, 129, 93, 57],
]

VALID_DIRECTIONS = ["right", "left"]

OLD_GREY_SCALES = [" .:;rsA23hHG#9&@"]

GREY_SCALES = [" .,:ilwW", " .,:ilwW%@", " .:;rsA23hHG#9&@"]

WIND_DIRECTIONS = ["east", "west", "none"]

NOISE = "!@#$%^&*()_+1234567890-=~`qazwsxedcrfvtgbyhnujmik,ol.p;/[']\QAZXSWEDCVFRTGBNHYUJM<KIOL>?:P{\"}|"

FLAKES = {1: "*", 3: "+", 7: "."}

FLAKE_COLORS = {1: 253, 3: 69, 7: 31}

FLAKE_JUMPS = {
    1: [1, 2, 3],
    3: [1, 2, 3],
    7: [1, 2],
}

NEXT_FLAKE_MOVE = {
    ("center", "right"): 1,
    ("center", "left"): -1,
    ("left", "center"): 1,
    ("right", "center"): -1,
    ("right", "left"): None,  # not valid
    ("left", "right"): None,  # not valid
}

FLAKE_WEIGHT_CHARS = {1: ",", 4: ";", 7: "*", 12: "@", 18: "#"}

FLAKE_FLIPS = {
    1: ["*", "1"],
    3: ["+", "3"],
    7: [".", "7"],
}

TWINKLE_COLORS = {idx: val for idx, val in enumerate(range(232, 256))}

VALID_INTERFACES = ["ollama", "openai"]