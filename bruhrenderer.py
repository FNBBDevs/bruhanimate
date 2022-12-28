from bruhanimate import WinScreen
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




class CenterRenderer(BaseRenderer):
    def __init__(self, screen, frames, time, background, img):
        super(CenterRenderer, self).__init__(screen, frames, time)
        self.background = background
        self.img = img

        if img:
            self.img_height = len(img)
            self.img_width  = len(img[0])
            
    def run(self):
        for _ in self.frames:
            self.render_frame()
            self.push_front_to_screen()
        self.render_exit()
        self.push_front_to_screen()
    
    def push_front_to_screen(self):
        """
        Pushes changes between the back and front buffer and applies them
        to the screen
        """
        pass

    def render_frame(self):
        """
        Renders out the img to the center of the screen in the back buffer.
        """
        pass

    def render_exit(self, wipe=True):
        """
        Renders out the exit prompt to the screen.
        :param wipe: To clear the final frame on the front buffer / screen.
        """
        pass