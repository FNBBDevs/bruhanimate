import sys
import time
import random
from ..bruhutil import Buffer, Screen
from ..bruheffect import *
from abc import abstractmethod

_VALID_EFFECTS = ["static", "offset", "noise", "stars", "plasma", "gol", "rain", "matrix", "drawlines", "snow", "twinkle", "audio", "chat"]
HORIZONTAL = "h"
VERTICAL = "v"
INF = float("inf")


def sleep(s):
    sys.stdout.flush()
    time.sleep(s)


class BaseRenderer:
    """
    Defines the base methods, abstract methods, and base attributes
    for the render class, is an Effect Only Renderer
    """

    def __init__(
        self,
        screen: Screen,
        frames: int = 100,
        time: float = 0.1,
        effect_type: str = "static",
        background: str = " ",
        transparent: bool = False,
        collision: bool = False,
    ):
        self.screen = screen
        self.frames = frames
        self.time = time
        self.effect_type = effect_type if effect_type in _VALID_EFFECTS else "static"
        self.transparent = transparent
        self.background = background
        self.height = screen.height
        self.width = screen.width
        self.smart_transparent = False
        self.collision = collision

        # effect
        if self.effect_type == "static":
            self.effect = StaticEffect(Buffer(self.height, self.width), self.background)
        elif self.effect_type == "offset":
            self.effect = OffsetEffect(Buffer(self.height, self.width), self.background)
        elif self.effect_type == "noise":
            self.effect = NoiseEffect(Buffer(self.height, self.width), self.background)
            self.background = self.effect.background
        elif self.effect_type == "stars":
            self.effect = StarEffect(Buffer(self.height, self.width), self.background)
        elif self.effect_type == "plasma":
            self.effect = PlasmaEffect(Buffer(self.height, self.width), self.background)
        elif self.effect_type == "gol":
            self.effect = GameOfLifeEffect(Buffer(self.height, self.width), self.background)
        elif self.effect_type == "rain":
            self.effect = RainEffect(Buffer(self.height, self.width), self.background)
        elif self.effect_type == "matrix":
            self.effect = MatrixEffect(Buffer(self.height, self.width), self.background)
        elif self.effect_type == "drawlines":
            self.effect = DrawLinesEffect(Buffer(self.height, self.width), self.background)
        elif self.effect_type == "snow":
            self.effect = SnowEffect(Buffer(self.height, self.width), self.background)
        elif self.effect_type == "twinkle":
            self.effect = TwinkleEffect(Buffer(self.height, self.width), self.background)
        elif self.effect_type == "audio":
            self.effect = AudioEffect(Buffer(self.height, self.width), self.background)
        elif self.effect_type == "chat":
            self.effect = ChatbotEffect(screen, Buffer(self.height, self.width), Buffer(self.height, self.width), self.background)

        self.effect.smart_transparent = False

        # buffers
        self.image_buffer = Buffer(self.height, self.width).clear_buffer(val=None)
        self.back_buffer = Buffer(self.height, self.width)
        self.front_buffer = Buffer(self.height, self.width)

        # exit message stats
        self.msg1 = " Frames Are Done "
        self.msg2 = "   Press Enter   "
        self.centered = True
        self.wipe = False
        self.x_loc = 0
        self.y_loc = 1

    def update_collision(self, collision):
        """
        Method for updating the collision for the rain effect
        """
        if self.effect_type == "rain":
            try:
                self.collision = collision
                self.effect.update_collision(
                    self.current_img_x,
                    self.current_img_y,
                    self.img_width,
                    self.img_height,
                    collision,
                    self.smart_transparent,
                    self.image_buffer,
                )
            except Exception as e:
                self.effect.update_collision(None, None, None, None, collision, None, None)
        elif self.effect_type == "snow":
            try:
                self.collision = collision
                self.effect.update_collision(
                    self.current_img_x,
                    self.current_img_y,
                    self.img_width,
                    self.img_height,
                    collision,
                    self.image_buffer,
                )
            except Exception as e:
                self.effect.update_collision(None, None, None, None, collision, None)

    def update_smart_transparent(self, smart_transparent):
        """
        Enable / Disable the smart transparency effect
        :param smart_transparent: True / False
        """
        self.smart_transparent = smart_transparent
        self.effect.smart_transparent = smart_transparent

    def push_front_to_screen(self):
        """
        Pushes changes between the back_buffer and front_buffer and applies them to the screen.
        
        :param None: This method does not take any parameters.
        :return None: This method does not return anything.
        """
        for y, x, val in self.front_buffer.get_buffer_changes(self.back_buffer):
            self.screen.print_at(val, x, y, 1)

    def render_exit(self):
        """
        Renders out the exit prompt to the screen.
        """
        if self.wipe:
            self.back_buffer.clear_buffer()
        if self.centered:
            self.back_buffer.put_at_center(self.height // 2 - 1, self.msg1)
            self.back_buffer.put_at_center(self.height // 2, self.msg2)
        else:
            self.back_buffer.put_at(
                self.x_loc, self.y_loc - 1, self.msg1, transparent=False
            )
            self.back_buffer.put_at(
                self.x_loc, self.y_loc, self.msg2, transparent=False
            )

    def run(self, end_message=True):
        """
        Updates the image_buffer and effect_buffer. Then the image_buffer is applied over top the effect_buffer
        and stored into the back_buffer. After the front_buffer is rendered to the screen, the front_buffer is synced
        with the back_buffer. Why? So the effect and image, and there associated calculations can be done independently.
        """

        try:
            if self.frames == INF:
                frame = 0
                while True:
                    if self.screen.has_resized(): raise Exception("An error was encounter. The Screen was resized.")
                    sleep(self.time)
                    self.render_img_frame(frame)
                    self.effect.render_frame(frame)
                    self.back_buffer.sync_with(self.effect.buffer)
                    self.back_buffer.sync_over_top(self.image_buffer)
                    self.push_front_to_screen()
                    self.front_buffer.sync_with(self.back_buffer)
                    frame += 1
            else:
                for frame in range(self.frames):
                    if self.screen.has_resized(): raise Exception("An error was encounter. The Screen was resized.")
                    sleep(self.time)
                    self.render_img_frame(frame)
                    self.effect.render_frame(frame)
                    self.back_buffer.sync_with(self.effect.buffer)
                    self.back_buffer.sync_over_top(self.image_buffer)
                    self.push_front_to_screen()
                    self.front_buffer.sync_with(self.back_buffer)
            
            if end_message:
                self.render_exit()
                self.push_front_to_screen()
            if sys.platform == 'win32': input()
        except KeyboardInterrupt:
            if end_message:
                self.render_exit()
                self.push_front_to_screen()
            if sys.platform == 'win32': input()

    def update_exit_stats(
        self, msg1=None, msg2=None, wipe=None, x_loc=None, y_loc=None, centered=False
    ):
        """
        Set the exit messages for when the animation finishes
        :param msg1: primary message
        :param msg2: secondary message
        :param wipe: whether to clear the buffer
        :param x_loc: where to put the message along the xaxis
        :param y_loc: where to put the message along the yaxis
        :param centered: whether or not the message should be centered
        """
        if msg1:
            self.msg1 = msg1.replace("\n", "")
        if msg2:
            self.msg2 = msg2.replace("\n", "")
        if wipe:
            self.wipe = wipe
        if x_loc and y_loc:
            self.x_loc, self.y_loc = x_loc, y_loc
        self.centered = centered

    @abstractmethod
    def render_frame(self):
        """
        To be defined by each renderer
        """