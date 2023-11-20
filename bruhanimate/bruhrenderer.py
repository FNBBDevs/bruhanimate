"""
Copyright 2023 Ethan Christensen

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import sys
import time
import random
from bruhanimate.bruhffer import Buffer
from bruhanimate.bruheffects import *
from bruhcolor import bruhcolored
from abc import abstractmethod

_VALID_EFFECTS = [
    "static",
    "offset",
    "noise",
    "stars",
    "plasma",
    "gol",
    "rain",
    "matrix",
    "drawlines",
    "snow",
]
HORIZONTAL = "h"
VERTICAL = "v"


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
        screen,
        frames,
        time,
        effect_type="static",
        background=" ",
        transparent=False,
        collision=False,
    ):
        # NECESSAARY INFO
        self.screen = screen
        self.frames = frames if frames else 100
        self.time = time if time >= 0 else 0.1
        self.effect_type = effect_type if effect_type in _VALID_EFFECTS else "static"
        self.transparent = transparent
        self.background = background
        self.height = screen.height
        self.width = screen.width
        self.smart_transparent = False
        self.collision = collision

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
        elif self.effect_type == "matrix":
            self.effect = MatrixEffect(effect_buffer, self.background)
        elif self.effect_type == "drawlines":
            self.effect = DrawLines(effect_buffer, self.background)
        elif self.effect_type == "snow":
            self.effect = SnowEffect(effect_buffer, self.background)

        # BUFFERS
        self.image_buffer = Buffer(self.height, self.width)
        self.image_buffer.clear_buffer(val=None)
        self.back_buffer = Buffer(self.height, self.width)
        self.front_buffer = Buffer(self.height, self.width)

        # EXIT STATS
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
                self.effect.update_collision(
                    None, None, None, None, collision, None, None
                )
        elif self.effect_type == "snow":
            try:
                self.collision = collision
                self.effect.update_collision(
                    self.current_img_x,
                    self.current_img_y,
                    self.img_width,
                    self.img_height,
                    collision,
                    self.image_buffer
                )
            except Exception as e:
                self.effect.update_collision(
                    None, None, None, None, collision, None
                )

    def update_smart_transparent(self, smart_transparent):
        """
        Enable / Disable the smart transparency effect
        :param smart_transparent: True / False
        """
        self.smart_transparent = smart_transparent

    def update_points(self, p1, p2):
        """
        Given two points, update start and end points for this line
        :param p1: start point (x, y)
        :param p2: end   point (x, y)
        """
        self.effect.line.uppdate_points(p1, p2)

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
        for _ in range(self.frames):
            sleep(self.time)
            self.render_img_frame(_)  # img buf
            self.effect.render_frame(_)  # effect buf
            self.back_buffer.sync_with(self.effect.buffer)
            self.back_buffer.sync_over_top_img(self.image_buffer)
            self.push_front_to_screen()
            self.front_buffer.sync_with(self.back_buffer)

        if end_message:
            self.render_exit()
            self.push_front_to_screen()

    def update_exit_stats(
        self, msg1=None, msg2=None, wipe=None, x_loc=0, y_loc=1, centered=False
    ):
        """
        Set the exit messages for when the animation finishes
        :param msg1: primary message
        :param msg2: secondary message
        :param wipe: whether to clear the buffer
        :param x_loc: where to put the message along the xaxis
        :param y_loc: where to put the message along the yaxis
        """
        if msg1:
            self.msg1 = msg1.replace("\n", "")
        if msg2:
            self.msg2 = msg2.replace("\n", "")
        if wipe:
            self.wipe = wipe
        self.x_loc, self.y_loc = x_loc, y_loc
        self.centered = centered

    @abstractmethod
    def render_frame(self):
        """
        To be defined by each renderer
        """


class EffectRenderer(BaseRenderer):
    """
    Class for rendering the Effect and only the Effect
    """

    def __init__(
        self,
        screen,
        frames,
        time,
        effect_type="static",
        background=" ",
        transparent=False,
    ):
        super(EffectRenderer, self).__init__(
            screen, frames, time, effect_type, background, transparent
        )
        self.background = self.effect.background

    def render_effect_frame(self, frame_number):
        """
        We only need to render the effect, so we just call the effects render
        frame method to update the effect buffer
        """
        self.effect.render_frame(frame_number)

    def run(self, end_message=True):
        """
        Generate the next effect frame and sync it with the back / front buffer
        """
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

    def __init__(
        self,
        screen,
        frames,
        time,
        img,
        effect_type="static",
        background=" ",
        transparent=False,
    ):
        super(CenterRenderer, self).__init__(
            screen, frames, time, effect_type, background, transparent
        )
        self.background = background if background else " "
        self.transparent = transparent if transparent else False

        # IMAGE
        self.img = img
        self.img_height = len(self.img)
        self.img_width = len(self.img[0])
        self.img_y_start = (self.height - len(self.img)) // 2
        self.img_x_start = (self.width - len(self.img[0])) // 2
        self.current_img_x = self.img_x_start
        self.current_img_y = self.img_y_start

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
                        if (
                            y >= self.img_y_start
                            and y < self.img_y_start + self.img_height
                            and x >= self.img_x_start
                            and x < self.img_x_start + self.img_width
                        ):
                            self.image_buffer.put_char(
                                x,
                                y,
                                self.img[y - self.img_y_start][x - self.img_x_start],
                            )
                # Now process spaces from left-to-right till a non-space character is hit.
                # Then do the same right-to-left. Place these spaces with None
                for y in range(self.height):
                    if y >= self.img_y_start and y < self.img_y_start + self.img_height:
                        for x in range(self.width):
                            if (
                                x >= self.img_x_start
                                and x < self.img_x_start + self.img_width
                            ):
                                if self.image_buffer.get_char(x, y) != " ":
                                    break
                                else:
                                    self.image_buffer.put_char(x, y, None)
                            else:
                                self.image_buffer.put_char(x, y, None)
                        for x in range(self.width - 1, -1, -1):
                            if (
                                x >= self.img_x_start
                                and x < self.img_x_start + self.img_width
                            ):
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
                    if y >= self.img_y_start and y < self.img_y_start + self.img_height:
                        self.image_buffer.put_at_center(
                            y, self.img[y - self.img_y_start],
                            transparent=self.transparent
                        )


class PanRenderer(BaseRenderer):
    """
    A renderer to pan an image across the screen.
    Update the image_buffer only.
    """

    def __init__(
        self,
        screen,
        frames,
        time,
        img,
        effect_type="static",
        background=" ",
        transparent=False,
        direction="h",
        shift_rate=1,
        loop=False,
    ):
        super(PanRenderer, self).__init__(
            screen, frames, time, effect_type, background, transparent
        )
        self.direction = direction if direction and direction in ["h", "v"] else "h"
        self.img = img
        self.shift_rate = int(shift_rate)
        self.loop = loop
        if self.img:
            self._set_img_attributes()

    def _set_img_attributes(self):
        """
        Sets the attributes for the image given it exists
        """
        self.render_image = True
        self.img_height = len(self.img)
        self.img_width = len(self.img[0])
        self.img_back = -self.img_width - 1
        self.img_front = -1
        self.img_top = (self.height - self.img_height) // 2
        self.img_bottom = ((self.height - self.img_height) // 2) + self.img_height
        self.current_img_x = self.img_back
        self.current_img_y = self.img_top

    def _set_padding(self, padding_vals):
        """
        Set the padding for the image [DEPRECATED FOR NOW]
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
                tmp.append(" " * self.img_width)
            for line in self.img:
                tmp.append(line)
            for _ in range(top_bottom):
                tmp.append(" " * self.img_width)

            for i in range(len(tmp)):
                tmp[i] = (" " * left_right) + tmp[i] + (" " * left_right)

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
        """
        Renders the next image frame for a horizontal pan
        """
        if self.shift_rate > 0:
            if (
                0 <= frame_number <= self.img_width // self.shift_rate + 1
            ) or not self.loop:
                for y in range(self.height):
                    for x in range(self.width):
                        if (
                            x >= self.img_back
                            and x < self.img_front
                            and y >= self.img_top
                            and y < self.img_bottom
                        ):
                            if (
                                (y - self.img_top) >= 0
                                and (y - self.img_bottom) < self.img_height
                                and (x - self.img_back) >= 0
                                and (x - self.img_back) < self.img_width
                            ):
                                if self.transparent:
                                    if (
                                        self.img[y - self.img_top][x - self.img_back]
                                        == " "
                                    ):
                                        self.image_buffer.put_char(x, y, None)
                                    else:
                                        self.image_buffer.put_char(
                                            x,
                                            y,
                                            self.img[y - self.img_top][
                                                x - self.img_back
                                            ],
                                        )
                                else:
                                    self.image_buffer.put_char(
                                        x,
                                        y,
                                        self.img[y - self.img_top][x - self.img_back],
                                    )
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
                self.image_buffer.shift(-self.shift_rate)
        else:
            pass


class FocusRenderer(BaseRenderer):
    """
    A Renderer that takes an image and randomly spreads the characters around the screen.
    The characters are then pulled to the middle of the screen
    """

    def __init__(
        self,
        screen,
        frames,
        time,
        img,
        effect_type="static",
        background=" ",
        transparent=False,
        start_frame=0,
        reverse=False,
        start_reverse=None,
    ):
        super(FocusRenderer, self).__init__(
            screen, frames, time, effect_type, background, transparent
        )
        self.background = background if background else " "
        self.transparent = transparent if transparent else False
        self.img = img
        self.start_frame = start_frame
        self.reverse = reverse
        self.start_reverse = start_reverse

        if start_reverse < self.start_frame:
            raise Exception(
                f"the frame to start the reverse can not be less than the start frame\n\tstart_frame: {self.start_frame}, start_reverse: {self.start_reverse}"
            )

        if self.reverse and self.start_reverse == None:
            raise Exception(
                "if reverse is enabled, and start_reverse frame must be provided"
            )

        if self.img:
            self._set_img_attributes()

    def _set_img_attributes(self):
        """
        Set the attributes of the img
        """
        self.img_height = len(self.img)
        self.img_width = len(self.img[0])
        self.img_y_start = (self.height - len(self.img)) // 2
        self.img_x_start = (self.width - len(self.img[0])) // 2
        self.current_img_x = self.img_x_start
        self.current_img_y = self.img_y_start
        self.start_board = [
            [
                [
                    random.randint(0, self.width - 1),
                    random.randint(0, self.height - 1),
                    self.img[y][x],
                    (x, y),
                ]
                for x in range(self.img_width)
            ]
            for y in range(self.img_height)
        ]
        self.current_board = [
            [
                [
                    self.start_board[y][x][0],
                    self.start_board[y][x][1],
                    self.img[y][x],
                    (x, y),
                ]
                for x in range(self.img_width)
            ]
            for y in range(self.img_height)
        ]
        self.end_board = [
            [
                [self.img_x_start + x, self.img_y_start + y, self.img[y][x], (x, y)]
                for x in range(self.img_width)
            ]
            for y in range(self.img_height)
        ]
        self.direction_board = [
            [
                [
                    -1
                    if (self.end_board[y][x][0] - self.current_board[y][x][0]) < 0
                    else 1,
                    -1
                    if (self.end_board[y][x][1] - self.current_board[y][x][1]) < 0
                    else 1,
                ]
                for x in range(self.img_width)
            ]
            for y in range(self.img_height)
        ]

    def update_reverse(self, reverse, start_reverse):
        """
        Function to update whether or not to reverse the Focus
        :param reverse: True / False
        """
        self.reverse = reverse
        self.start_reverse = start_reverse
        if start_reverse < self.start_frame:
            raise Exception(
                f"the frame to start the reverse can not be less than the start frame\n\tstart_frame: {self.start_frame}, start_reverse: {self.start_reverse}"
            )

    def update_start_frame(self, frame_number):
        """
        Updates the frame at which the Focus Effect should start
        :param frame_number: Frame to start
        """
        self.start_frame = frame_number

    def solved(self, end_state):
        """
        Function that determines if the image has been moved back to its
        original shape
        """
        b1 = self.current_board
        b2 = self.end_board
        b3 = self.start_board
        if end_state == "end":
            for y in range(len(b1)):
                for x in range(len(b1[y])):
                    if b1[y][x][0] == b2[y][x][0] and b1[y][x][1] == b2[y][x][1]:
                        pass
                    else:
                        return False
            return True
        elif end_state == "start":
            for y in range(len(b1)):
                for x in range(len(b1[y])):
                    if b1[y][x][0] == b3[y][x][0] and b1[y][x][1] == b3[y][x][1]:
                        pass
                    else:
                        return False
            return True
        else:
            raise Exception(f"unkown solved board state for FocusRenderer: {end_state}")

    def render_img_frame(self, frame_number):
        """
        Renders the next image frame into the image buffer
        """
        if frame_number >= self.start_reverse:
            if not self.solved(end_state="start"):
                for y in range(len(self.current_board)):
                    for x in range(len(self.current_board[y])):
                        x_check, y_check = False, False
                        # MOVE X IF NEEDED
                        if self.current_board[y][x][0] != self.start_board[y][x][0]:
                            self.current_board[y][x][0] -= self.direction_board[y][x][0]
                        else:
                            x_check = True
                        # MOVE Y IF NEEDED
                        if self.current_board[y][x][1] != self.start_board[y][x][1]:
                            self.current_board[y][x][1] -= self.direction_board[y][x][1]
                        else:
                            y_check = True

                        if x_check and y_check:
                            self.current_board[y][x][2] = None
                self.image_buffer.clear_buffer(val=None)
                for row in self.current_board:
                    for value in row:
                        self.image_buffer.put_char(
                            value[0], value[1], value[2], transparent=self.transparent
                        )
            else:
                self.image_buffer.clear_buffer(val=None)
        elif frame_number >= self.start_frame:
            if not self.solved(end_state="end"):
                for y in range(len(self.current_board)):
                    for x in range(len(self.current_board[y])):
                        # MOVE X IF NEEDED
                        if self.current_board[y][x][0] != self.end_board[y][x][0]:
                            self.current_board[y][x][0] += self.direction_board[y][x][0]

                        # MOVE Y IF NEEDED
                        if self.current_board[y][x][1] != self.end_board[y][x][1]:
                            self.current_board[y][x][1] += self.direction_board[y][x][1]
                self.image_buffer.clear_buffer(val=None)
                for row in self.current_board:
                    for value in row:
                        self.image_buffer.put_char(
                            value[0], value[1], value[2], transparent=self.transparent
                        )


class BackgroundColorRenderer(BaseRenderer):
    def __init__(
        self,
        screen,
        frames,
        time,
        img,
        on_color_code,
        effect_type="static",
        background=" ",
        transparent=False,
    ):
        super(BackgroundColorRenderer, self).__init__(
            screen, frames, time, effect_type, background, transparent
        )

        self.img = img
        self.img_height = len(self.img)
        self.img_width = len(self.img[0])
        self.img_y_start = (self.height - len(self.img)) // 2
        self.img_x_start = (self.width - len(self.img[0])) // 2
        self.current_img_x = self.img_x_start
        self.current_img_y = self.img_y_start

        if not on_color_code:
            raise Exception("a color code must be provided to BackgroundColorRenderer")
        if (
            not isinstance(on_color_code, int)
            or on_color_code < 0
            or on_color_code > 255
        ):
            raise Exception("the color code must be an int value 0-255")
        self.on_color_code = on_color_code

    def render_img_frame(self, frame_number):
        for y in range(self.height):
            for x in range(self.width):
                if (
                    (y >= self.img_y_start)
                    and (y < (self.img_y_start + self.img_height))
                    and (x >= self.img_x_start)
                    and (x < (self.img_x_start + self.img_width))
                ):
                    self.image_buffer.put_char(
                        x,
                        y,
                        bruhcolored(
                            self.img[y - self.img_y_start][x - self.img_x_start],
                            on_color=self.on_color_code,
                        ).colored,
                    )
