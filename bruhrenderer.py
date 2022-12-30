import sys
import os
import time
import random
from bruhffer import Buffer
from bruheffects import *
from abc import ABC, abstractmethod
from threading import Timer
_VALID_EFFECTS = ["static", "offset", "noise", "stars"]

def sleep(s):
    sys.stdout.flush()
    time.sleep(s)


class BaseRenderer:
    """
    Defines the base methods, abstract methods, and base attributes
    for the render class, is an Effect Only Renderer
    """
    def __init__(self, screen, frames, time, effect_type="static", background=" ", transparent=False):

        # NECESSAARY INFO
        self.screen      = screen
        self.frames      = frames if frames else 100
        self.time        = time   if time >= 0 else 0.1
        self.effect_type = effect_type if effect_type in _VALID_EFFECTS else "static"
        self.transparent = transparent
        self.background  = background
        self.height      = screen.height
        self.width       = screen.width
        
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
        
        # BUFFERS
        self.image_buffer  = Buffer(self.height, self.width)
        self.back_buffer   = Buffer(self.height, self.width)
        self.front_buffer  = Buffer(self.height, self.width)

        # EXIT STATS
        self.msg1 = " Frames Are Done "
        self.msg2 = "   Press Enter   "
        self.wipe = False

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
        self.back_buffer.put_at_center(self.height - 3, self.msg1)    
        self.back_buffer.put_at_center(self.height - 2, self.msg2)

    def run(self):
        """
        Updates the image_buffer and effect_buffer. Then the image_buffer is applied over top the effect_buffer
        and stored into the back_buffer. After the front_buffer is rendered to the screen, the front_buffer is synced
        with the back_buffer. Why? So the effect and image, and there associated calculations can be done independently.
        """
        for _ in range(self.frames):
            sleep(self.time)
            self.render_img_frame(_)
            self.render_effect_frame(_)
            self.push_front_to_screen()
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
    
    def run(self):
        start = time.time()
        second = 1
        for _ in range(self.frames):
            self.render_effect_frame(_)
            self.back_buffer.sync_with(self.effect.buffer)
            self.push_front_to_screen()
            self.front_buffer.sync_with(self.back_buffer)
            sleep(self.time)
            if time.time() - start >= 1:
                print(f"{second} SECOND ELAPSED AT FRAME: {_}")
                second += 1
                start = time.time()
        self.render_exit()
        self.push_front_to_screen()


class CenterRenderer(BaseRenderer):
    """
    A renderer to load an image in the center of the screen.
    Updates the image_buffer only
    """
    def __init__(self, screen, frames, time, img, effect_type="static", background=" ", transparent=False):
        super(CenterRenderer, self).__init__(screen, frames, time, effect_type, background, transparent)
        self.background = background if background else " "
        self.img = None
        self.transparent = transparent if transparent else False
        self.orig_img = img
        self.padding = [0, 0]

        if img:
            self.img = img
            self._set_img_attributes()

    def set_padding(self, padding_vals):
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
    
    def _set_img_attributes(self):
        """
        Updates attributes that relate to the image given an image exists
        """
        if self.img:
            self.img_height = len(self.img)
            self.img_width = len(self.img[0])
            self.img_y_start = (self.height - len(self.img)) // 2
            self.img_x_start = (self.width - len(self.img[0])) // 2
 
    def render_img_frame(self, frame_number):
        """
        Renders out the image to the center of the screen,
        if there is no image passed into the renderer then
        the background is rendered on it's own
        """
        if self.img:
            for y in range(self.back.height()):
                self.back.put_at(0, y, ''.join([self.background[random.randint(0, len(self.background) - 1)] if random.random() < 0.1 else self.back.get_char(_, y) for _ in range(self.back.width())]))
                """if self.offset:
                    self.back.put_at(0, y, (self.background[y%len(self.background):] + self.background[:y%len(self.background)])*self.width)
                else:
                    self.back.put_at(0, y, self.background*self.width, self.transparent)"""
                if y >= self.img_y_start and y < self.img_y_start + self.img_height:
                    self.back.put_at(self.img_x_start, y, self.img[y-self.img_y_start], self.transparent)
        else:
            for y in range(self.height):
                if self.offset:
                    self.back.put_at(0, y, (self.background[y%len(self.background):] + self.background[:y%len(self.background)])*self.width)
                else:
                    self.back.put_at(0, y, self.background*self.width)


class PanRenderer(BaseRenderer):
    """
    A renderer to pan an image across the screen.
    Update the image_buffer only.
    """
    def __init__(self, screen, frames, time, img, effect_type="static", background=" ", transparent=False, direction="h", shift_rate=1):
        super().__init__(screen, frames, time, effect_type, background, transparent)
        self.direction = direction if direction and direction in ["h", "v"] else "h"
        self.img = None
        self.current_x = 0
        self.current_y = 0
        self.shift_rate = shift_rate

        if img:
            self.img = img
            self.frames = (self.screen.width + len(self.img[0])) // self.shift_rate + self.shift_rate
            self._set_img_attributes()
    
    def _set_img_attributes(self):
        if self.img:
            self.current_x = 0 if self.direction == "v" else -len(self.img[0])
            self.current_y = 0 if self.direction == "h" else -len(self.img)
            self.img_height = len(self.img)
            self.img_width = len(self.img[0])
            self.img_y_start = (self.height - len(self.img)) // 2
            self.img_x_start = (self.width - len(self.img[0])) // 2

    def set_padding(self, padding_vals):
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
        if self.img:
            if self.direction == "h":
                # Align center vertically

                for y in range(self.height):
                    if self.offset:
                        self.back.put_at(0, y, (self.background[y%len(self.background):] + self.background[:y%len(self.background)])*self.width)
                    else:
                        self.back.put_at(0, y, self.background*self.width, self.transparent)
                    if y >= self.img_y_start and y < self.img_y_start + len(self.img):
                        self.back.put_at(self.current_x, y, self.img[y-self.img_y_start], self.transparent)
                self.current_x += self.shift_rate
        else:
            for y in range(self.height):
                if self.offset:
                    self.back.put_at(0, y, (self.background[y%len(self.background):] + self.background[:y%len(self.background)])*self.width)
                else:
                    self.back.put_at(0, y, self.background*self.width)

