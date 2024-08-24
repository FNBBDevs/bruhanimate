from bruhutil import VALID_DIRECTIONS
from bruheffect import BaseEffect


class OffsetEffect(BaseEffect):
    """
    Class for generating an offset-static backgorund.
    :new-param direction: which way the offset should go.
    """

    def __init__(self, buffer, background, direction="right"):
        super(OffsetEffect, self).__init__(buffer, background)
        self.direction = direction if direction in VALID_DIRECTIONS else "right"

    def update_direction(self, direction):
        """
        Function to update the direction of the offset
        :param direction: East / West
        """
        self.direction = direction if direction in VALID_DIRECTIONS else "right"
        self.buffer.clear_buffer()

    def render_frame(self, frame_number):
        """
        Function to render the next frame of the Offset effect
        """
        for y in range(self.buffer.height()):
            row = (
                self.background[y % self.background_length :]
                + self.background[: y % self.background_length]
            ) * (self.buffer.width() // self.background_length + self.background_length)
            if self.direction == "right":
                self.buffer.put_at(0, y, row[::-1])
            else:
                self.buffer.put_at(0, y, row)

