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
        self.back = Buffer(self.height, self.width)
        self.front = Buffer(self.height, self.width)

    def push_front_to_screen(self):
        """
        Pushes changes between the back and front buffer and applies them
        to the screen
        """
        updates = self.front.get_buffer_changes(self.back)
        if updates:
            for update in updates:
                self.screen.print_at(update[2], update[0], update[1], len(update[2]))
    
    def render_exit(self, wipe=True):
        """
        Renders out the exit prompt to the screen.
        :param wipe: To clear the final frame on the front buffer / screen.
        """
        pass
    
    def run(self):
        """
        Renders a new frame to the back buffer, then syncs it with the front buffer.
        Then the front buffer is pushed to the screen.
        """
        for _ in range(self.frames):
            self.render_frame()
            self.push_front_to_screen()
            self.front.sync_with(self.back)
        self.render_exit()
        self.push_front_to_screen()
    
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

        if img:
            self.img_height = len(img)
            self.img_width  = len(img[0])
            self.img_y_start = (self.height - len(img)) // 2
            self.img_x_start = (self.width - len(img[0])) // 2
                
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


