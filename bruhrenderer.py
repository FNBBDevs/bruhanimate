from abc import ABC, abstractmethod
from bruhffer import Buffer
import sys
import os
import time
import random

def sleep(s):
    sys.stdout.flush()
    time.sleep(s)


class BaseRenderer:
    def __init__(self, screen, frames, time):
        self.screen = screen
        self.frames = frames
        self.time = time
        self.height = screen.height
        self.width  = screen.width

        # BUFFERS
        self.back = Buffer(self.height, self.width)
        self.front = Buffer(self.height, self.width)

        # EXIT STATS
        self.msg1 = " Frames Are Done "
        self.msg2 = "   Press Enter   "
        self.wipe = False

    def push_front_to_screen(self):
        """
        Pushes changes between the back and front buffer and applies them
        to the screen
        """
        updates = self.front.get_buffer_changes(self.back)
        if updates:
            for update in updates:
                self.screen.print_at(update[2], update[0], update[1], len(update[2]))
    
    def render_exit(self):
        """
        Renders out the exit prompt to the screen.
        :param wipe: To clear the final frame on the front buffer / screen.
        """
        if self.wipe:
            self.back.clear_buffer()
        self.back.put_at_center(self.height - 3, self.msg1)    
        self.back.put_at_center(self.height - 2, self.msg2)

    def run(self):
        """
        Renders a new frame to the back buffer, then syncs it with the front buffer.
        Then the front buffer is pushed to the screen.
        """
        for _ in range(self.frames):
            sleep(self.time)
            self.render_frame()
            self.push_front_to_screen()
            self.front.sync_with(self.back)
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
            self.msg1 = msg1
        if msg2:
            self.msg2 = msg2
        if wipe:
            self.wipe = wipe

    
    @abstractmethod
    def render_frame(self):
        """
        To be defined by specific renderer classes
        """

class CenterRenderer(BaseRenderer):
    def __init__(self, screen, frames, time, background, img):
        super(CenterRenderer, self).__init__(screen, frames, time)
        self.background = background if background else " "
        self.img = img
        self.orig_img = img
        self.padding = [0, 0]

        if img:
            self.img_height = len(img)
            self.img_width  = len(img[0])
            self.img_y_start = (self.height - len(img)) // 2
            self.img_x_start = (self.width - len(img[0])) // 2

    def set_padding(self, padding_vals):
        """
        Set the padding for the image
        :param padding_vals: vals for padding [left-right, top-bottom]
        """
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
        self.img_height = len(self.img)
        self.img_width = len(self.img[0])
        self.img_y_start = (self.height - len(self.img)) // 2
        self.img_x_start = (self.width - len(self.img[0])) // 2


                
    def render_frame(self):
        """
        Renders out the img to the center of the screen in the back buffer.
        """
        if self.img:
            for y in range(len(self.back.buffer)):
                if y >= self.img_y_start and y < self.img_y_start + self.img_height:
                    self.back.put_at(0, y, self.background*(self.img_x_start))
                    self.back.put_at(self.img_x_start, y, self.img[y-self.img_y_start])
                    self.back.put_at(self.img_x_start + self.img_width, y, self.background*(self.img_x_start))
                else:
                    self.back.put_at(0, y, self.background*self.width)
        else:
            """
            Simply render the specified background.
            """
            for _ in range(self.height):
                self.back.put_at(0, _, self.background*self.width)


