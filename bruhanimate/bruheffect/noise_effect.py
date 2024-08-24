import random

from bruhcolor import bruhcolored
from bruheffect import BaseEffect

class NoiseEffect(BaseEffect):
    """
    Class for generating noise.
    :param intensity: randomness for the noise, higher the value the slower the effect (due to computation).
                      Will be a value 1 - 999
    :param color: whether or not ro color the noise
    """

    def __init__(self, buffer, background, intensity=200, color=False):
        super(NoiseEffect, self).__init__(buffer, background)

        self.intensity = (
            intensity / 1000 if intensity and 1 <= intensity <= 999 else 200 / 1000
        )

        self.noise = " !@#$%^&*()_+1234567890-=~`qazwsxedcrfvtgbyhnujmik,ol.p;/[']\QAZXSWEDCVFRTGBNHYUJM<KIOL>?:P{\"}|"
        self.noise_length = len(self.noise)
        self.color = color

    def update_intensity(self, intensity):
        """
        Function to update the intensity of the effect
        :param intensity: new intensity
        """
        self.intensity = (
            intensity / 1000 if intensity and 1 <= intensity <= 999 else 200 / 1000
        )

    def update_color(self, color, characters):
        """
        Function to enable / disable color for the effect
        :param color: True / False
        :param character: True / False to make characters visable
        """
        self.color = color
        self.characters = characters

    def render_frame(self, frame_number):
        """
        Function to render the next frame of the Noise effect
        """
        if self.color:
            for y in range(self.buffer.height()):
                for x in range(self.buffer.width()):
                    if random.random() < self.intensity:
                        if self.characters:
                            self.buffer.put_char(
                                x,
                                y,
                                bruhcolored(
                                    self.noise[
                                        random.randint(0, self.noise_length - 1)
                                    ],
                                    on_color=random.randint(0, 255),
                                ).colored,
                            )
                        else:
                            self.buffer.put_char(
                                x,
                                y,
                                bruhcolored(
                                    " ", on_color=random.randint(0, 255)
                                ).colored,
                            )
        else:
            for y in range(self.buffer.height()):
                for x in range(self.buffer.width()):
                    if random.random() < self.intensity:
                        self.buffer.put_char(
                            x, y, self.noise[random.randint(0, self.noise_length - 1)]
                        )