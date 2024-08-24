from abc import abstractmethod


class BaseEffect:
    """
    Class for keeping track of an effect, and updataing it's buffer
    """

    def __init__(self, buffer, background):
        self.buffer = buffer
        self.background = background
        self.background_length = len(background)

    @abstractmethod
    def render_frame(self, frame_number):
        """
        To be defined by each effect
        """