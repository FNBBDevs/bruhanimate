from bruheffect import BaseEffect


class StaticEffect(BaseEffect):
    """
    Class for generating a static background.
    """

    def __init__(self, buffer, background):
        super(StaticEffect, self).__init__(buffer, background)

    def render_frame(self, frame_number):
        """
        Renders the background to the screen
        """
        for y in range(self.buffer.height()):
            self.buffer.put_at(
                0,
                y,
                self.background
                * (
                    self.buffer.width() // self.background_length
                    + self.background_length
                ),
            )

