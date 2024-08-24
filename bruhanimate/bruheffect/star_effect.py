import random

from bruhcolor import bruhcolored
from ..bruhutil import LIFE_COLORS
from .noise_effect import NoiseEffect

class StarEffect(NoiseEffect):
    """
    Class for rendering out a blinking star effect. This is just a Noise effect with a predefined intensity.
    Ideally the background would be ' ' for the best effect, but the choice is yours.
    """

    def __init__(self, buffer, background, color_type="GREYSCALE"):
        super(StarEffect, self).__init__(buffer, background)

        self.stars = f"{background*(100 // self.background_length)}.*+"
        self.stars_length = len(self.stars)
        self.color_type = color_type

    def update_color_type(self, color_type):
        """
        Function to update the color of the stars
        :param color_type: color map
        """
        self.color_type = color_type

    def update_background(self, background):
        """
        Function to update the background of the efffect
        :param background: the new background
        """
        self.background = background
        self.background_length = len(background)
        self.stars = f"{background*(100 // self.background_length)}.*+"
        self.stars_length = len(self.stars)

    def render_frame(self, frame_number):
        """
        Function to update the next frame of the Stars effect
        """
        for y in range(self.buffer.height()):
            for x in range(self.buffer.width()):
                if random.random() < self.intensity:
                    self.buffer.put_char(
                        x,
                        y,
                        bruhcolored(
                            self.stars[random.randint(0, self.stars_length - 1)],
                            color=LIFE_COLORS[self.color_type][
                                random.randint(
                                    0, len(LIFE_COLORS[self.color_type]) - 1
                                )
                            ],
                        ).colored,
                    )
