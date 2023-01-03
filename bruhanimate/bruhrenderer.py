import sys
import time
import random
from bruhanimate.bruhffer import Buffer
from bruhanimate.bruheffects import *
from abc import abstractmethod
_VALID_EFFECTS = ["static", "offset", "noise", "stars", "plasma", "gol", "rain"]
HORIZONTAL = "h"
VERTICAL   = "v"

def sleep(s):
    sys.stdout.flush()
    time.sleep(s)


class BaseRenderer:
    """
    Defines the base methods, abstract methods, and base attributes
    for the render class, is an Effect Only Renderer
    """
    def __init__(self, screen, frames, time, effect_type="static", background=" ", transparent=False, collision=False):

        # NECESSAARY INFO
        self.screen            = screen
        self.frames            = frames if frames else 100
        self.time              = time   if time >= 0 else 0.1
        self.effect_type       = effect_type if effect_type in _VALID_EFFECTS else "static"
        self.transparent       = transparent
        self.background        = background
        self.height            = screen.height
        self.width             = screen.width
        self.smart_transparent = False
        self.collision         = collision
        
        # EFFECT
        effect_buffer = Buffer(self.height, self.width)
        if self.effect_type == "static":
            self.effect = StaticEffect(effect_buffer, self.background)
        elif self.effect_type == "offset":
            self.effect = OffsetEffect(effect_buffer, self.background)
        elif self.effect_type == "noise":
            self.effect = NoiseEffect(effect_buffer, self.background)
            self.background = self.effect.background
        elif self.effect_type == "stars":
            self.effect = StarEffect(effect_buffer, self.background)
        elif self.effect_type == "plasma":
            self.effect = PlasmaEffect(effect_buffer, self.background)
        elif self.effect_type == "gol":
            self.effect = GameOfLifeEffect(effect_buffer, self.background)
        elif self.effect_type == "rain":
            self.effect = RainEffect(effect_buffer, self.background)
        
        # BUFFERS
        self.image_buffer  = Buffer(self.height, self.width)
        self.back_buffer   = Buffer(self.height, self.width)
        self.front_buffer  = Buffer(self.height, self.width)

        # EXIT STATS
        self.msg1 = " Frames Are Done "
        self.msg2 = "   Press Enter   "
        self.wipe = False
    
    def update_collision(self, collision):
        if self.effect_type == "rain":
            try:
                self.collision = collision
                self.effect.update_collision(self.current_img_x, self.current_img_y, self.img_width, self.img_height, collision, self.smart_transparent, self.image_buffer)
            except Exception as e:
                self.effect.update_collision(None, None, None, None, collision, None, None)
        
    def update_smart_transparent(self, smart_transparent):
        self.smart_transparent = smart_transparent

    def push_front_to_screen(self):
        """
        Pushes changes between the back_buffer and front_buffer and applies them
        to the screen
        """
        for y, x, val in self.front_buffer.get_buffer_changes(self.back_buffer):
            self.screen.print_at(val, x, y, 1)
    
    def render_exit(self):
        """
        Renders out the exit prompt to the screen.
        """
        if self.wipe:
            self.back_buffer.clear_buffer()
        self.back_buffer.put_at_center(self.height // 2 - 1, self.msg1)    
        self.back_buffer.put_at_center(self.height // 2, self.msg2)

    def run(self, end_message=True):
        """
        Updates the image_buffer and effect_buffer. Then the image_buffer is applied over top the effect_buffer
        and stored into the back_buffer. After the front_buffer is rendered to the screen, the front_buffer is synced
        with the back_buffer. Why? So the effect and image, and there associated calculations can be done independently.
        """
        for _ in range(self.frames):
            sleep(self.time)
            self.render_img_frame(_)
            self.effect.render_frame(_)
            self.back_buffer.sync_with(self.effect.buffer)
            self.back_buffer.sync_over_top_img(self.image_buffer)
            self.push_front_to_screen()
            self.front_buffer.sync_with(self.back_buffer)
        
        if end_message:
            self.render_exit()
            self.push_front_to_screen()

    def set_exit_stats(self, msg1=None, msg2=None, wipe=None):
        """
        Set the exit messages for when the animation finishes
        :param msg1: primary message
        :param msg2: secondary message
        :param wipe: whether to clear the buffer
        """
        if msg1:
            self.msg1 = msg1.replace("\n", "")
        if msg2:
            self.msg2 = msg2.replace("\n", "")
        if wipe:
            self.wipe = wipe

    def set_effect(self):
        effect_type = self.effect_type
        effect_buffer = Buffer(self.height, self.width)
        
        if effect_type == "static":
            pass
        elif effect_type == "offset":
            pass
        elif effect_type == "noise":
            pass
        elif effect_type == "start":
            pass

    @abstractmethod
    def render_frame(self):
        """
        To be defined by each renderer
        """


class EffectRenderer(BaseRenderer):
    """
    Class for rendering the Effect and only the Effect
    """
    def __init__(self, screen, frames, time, effect_type="static", background=" ", transparent=False):
        super(EffectRenderer, self).__init__(screen, frames, time, effect_type, background, transparent)
        self.background = self.effect.background
    
    def render_effect_frame(self, frame_number):
        self.effect.render_frame(frame_number)
    
    def run(self, end_message=True):
        start = time.time()
        second = 1
        for _ in range(self.frames):
            self.render_effect_frame(_)
            self.back_buffer.sync_with(self.effect.buffer)
            self.push_front_to_screen()
            self.front_buffer.sync_with(self.back_buffer)
            sleep(self.time)
            if time.time() - start >= 0.5:
                second += 1
                start = time.time()
        if end_message:
            self.render_exit()
            self.push_front_to_screen()


class CenterRenderer(BaseRenderer):
    """
    A renderer to load an image in the center of the screen.
    Updates the image_buffer only
    """
    def __init__(self, screen, frames, time, img, effect_type="static", background=" ", transparent=False):
        super(CenterRenderer, self).__init__(screen, frames, time, effect_type, background, transparent)
        self.background        = background if background else " "
        self.transparent       = transparent if transparent else False

        # IMAGE
        self.img             = img
        self.img_height      = len(self.img)
        self.img_width       = len(self.img[0])
        self.img_y_start     = (self.height - len(self.img)) // 2
        self.img_x_start     = (self.width - len(self.img[0])) // 2
        self.current_img_x   = self.img_x_start
        self.current_img_y   = self.img_y_start


    def render_img_frame(self, frame_number):
        """
        Renders out the image to the center of the screen,
        if there is no image passed into the renderer then
        the background is rendered on it's own
        """
        if frame_number == 0:
            if self.smart_transparent:
                # Place the image in it's entirerty
                for y in range(self.height):
                    for x in range(self.width):
                        if y >= self.img_y_start and y < self.img_y_start + self.img_height and x >= self.img_x_start and x < self.img_x_start + self.img_width:
                            self.image_buffer.put_char(x, y, self.img[y-self.img_y_start][x-self.img_x_start])
                # Now process spaces from left-to-right till a non-space character is hit. 
                # Then do the same right-to-left. Place these spaces with None
                for y in range(self.height):
                    if y >= self.img_y_start and y < self.img_y_start + self.img_height:
                        for x in range(self.width):
                            if x >= self.img_x_start and x < self.img_x_start + self.img_width:
                                if self.image_buffer.get_char(x, y) != " ":
                                    break
                                else:
                                    self.image_buffer.put_char(x, y, None)
                            else:
                                self.image_buffer.put_char(x, y, None)
                        for x in range(self.width - 1, -1, -1):
                            if x >= self.img_x_start and x < self.img_x_start + self.img_width:
                                if self.image_buffer.get_char(x, y) != " ":
                                    break
                                else:
                                    self.image_buffer.put_char(x, y, None)
                            else:
                                self.image_buffer.put_char(x, y, None)
                    else:
                        for x in range(self.width):
                            self.image_buffer.put_char(x, y, None)
            else:
                for y in range(self.height):
                    for x in range(self.width):
                        if y >= self.img_y_start and y < self.img_y_start + self.img_height and x >= self.img_x_start and x < self.img_x_start + self.img_width:
                            if self.transparent:
                                if self.img[y-self.img_y_start][x-self.img_x_start] == " ":
                                    self.image_buffer.put_char(x, y, None)
                                else:
                                    self.image_buffer.put_char(x, y, self.img[y-self.img_y_start][x-self.img_x_start])
                            else:
                                self.image_buffer.put_char(x, y, self.img[y-self.img_y_start][x-self.img_x_start])
                        else:
                            self.image_buffer.put_char(x, y, None)


class PanRenderer(BaseRenderer):
    """
    A renderer to pan an image across the screen.
    Update the image_buffer only.
    """
    def __init__(self, screen, frames, time, img, effect_type="static", background=" ", transparent=False, direction="h", shift_rate=1, loop=False):
        super().__init__(screen, frames, time, effect_type, background, transparent)
        self.direction = direction if direction and direction in ["h", "v"] else "h"
        self.img = img
        self.shift_rate = shift_rate
        self.loop = loop
        self._set_img_attributes()
    
    def _set_img_attributes(self):
        self.render_image = True
        self.img_height = len(self.img)
        self.img_width  = len(self.img[0])
        self.img_back   = -self.img_width-1
        self.img_front  = -1
        self.img_top    = (self.height - self.img_height) // 2
        self.img_bottom = ((self.height - self.img_height) // 2) + self.img_height
        self.current_img_x = self.img_back
        self.current_img_y = self.img_top

    def _set_padding(self, padding_vals):
        """
        Set the padding for the image
        :param padding_vals: vals for padding [left-right, top-bottom]
        """

        if not self.img:
            return

        if len(padding_vals) == 2:
            self.padding = padding_vals
        
        left_right = self.padding[0]
        top_bottom = self.padding[1]
        if left_right > 0 or top_bottom > 0:
            tmp = []
            for _ in range(top_bottom):
                tmp.append(" "*self.img_width)
            for line in self.img:
                tmp.append(line)
            for _ in range(top_bottom):
                tmp.append(" "*self.img_width)

            for i in range(len(tmp)):
                tmp[i] = (" "*left_right) + tmp[i] + (" "*left_right)
            
            self.img = [line for line in tmp]
            self._set_img_attributes()

    def render_img_frame(self, frame_number):
        """
        Renders out the next frame of the pan animation,
        if there is no image passed into the renderer then
        the background is rendered on it's own
        """
        if not self.loop:
            if self.img_back > self.width + 1:
                return
        if self.direction == HORIZONTAL:
            self.render_horizontal_frame(frame_number)
        elif self.direction == VERTICAL:
            self.render_veritcal_frame()

    def render_horizontal_frame(self, frame_number):

        if (0 <= frame_number <= self.img_width) or not self.loop:
            for y in range(self.height):
                for x in range(self.width):
                    if x >= self.img_back and x < self.img_front and y >= self.img_top and y < self.img_bottom:
                        if (y-self.img_top) >= 0 and (y-self.img_bottom) < self.img_height and (x-self.img_back) >= 0 and (x-self.img_back) < self.img_width:
                            if self.transparent:
                                if self.img[y-self.img_top][x-self.img_back]== " ":
                                    self.image_buffer.put_char(x, y, None)
                                else:
                                    self.image_buffer.put_char(x, y, self.img[y-self.img_top][x-self.img_back])
                            else:
                                self.image_buffer.put_char(x, y, self.img[y-self.img_top][x-self.img_back])
                    else:
                        self.image_buffer.put_char(x, y, None)
            if self.loop:
                if self.img_front >= self.width:
                    self.img_front = 0
                else:
                    self.img_front += self.shift_rate
                if self.img_back >= self.width:
                    self.img_back = 0
                else:
                    self.img_back += self.shift_rate
            else:
                self.img_back += self.shift_rate
                self.img_front += self.shift_rate
        else:
            for y in range(self.height):
                self.image_buffer.buffer[y] = self.image_buffer.buffer[y][-self.shift_rate:] + self.image_buffer.buffer[y][:-self.shift_rate]