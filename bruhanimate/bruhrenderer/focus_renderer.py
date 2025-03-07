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

import random
from typing import List
from .base_renderer import BaseRenderer
from ..bruhutil.bruhtypes import EffectType


class FocusRenderer(BaseRenderer):
    """
    A Renderer that takes an image and randomly spreads the characters around the screen.
    The characters are then pulled to the middle of the screen
    """

    def __init__(
        self,
        screen,
        img: List[str],
        frames: int = 100,
        frame_time: float = 0.1,
        effect_type: EffectType = "static",
        background: str = " ",
        transparent: bool = False,
        collision: bool = False,
        start_frame: int = 0,
        reverse: bool = False,
        start_reverse: int = None,
        loop: bool = True,
    ):
        super(FocusRenderer, self).__init__(
            screen, frames, frame_time, effect_type, background, transparent, collision
        )
        self.background = background if background else " "
        self.transparent = transparent if transparent else False
        self.img = img
        self.start_frame = start_frame
        self.reverse = reverse
        self.start_reverse = start_reverse
        if self.start_reverse:
            self.frame_gap = start_reverse - start_frame
        self.loop = True if loop == True and reverse == True else False
        self.loops = 1

        if self.reverse and self.start_reverse == None:
            raise Exception(
                "if reverse is enabled, and start_reverse frame must be provided"
            )

        if self.reverse and start_reverse < self.start_frame:
            raise Exception(
                f"the frame to start the reverse can not be less than the start frame\n\tstart_frame: {self.start_frame}, start_reverse: {self.start_reverse}"
            )

        if self.img:
            self._set_img_attributes()

    def _set_img_attributes(self):
        """
        Sets attributes for the image, such as its height and width,
        and initializes boards to track character positions.
        """
        self.img_height = len(self.img)
        self.img_width = len(self.img[0])
        self.img_y_start = (self.height - len(self.img)) // 2
        self.img_x_start = (self.width - len(self.img[0])) // 2
        self.current_img_x = self.img_x_start
        self.current_img_y = self.img_y_start
        
        # Initialize start board with characters at random positions
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
        
        # Initialize current board with characters at start positions
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
        
        # Initialize end board with characters at target positions
        self.end_board = [
            [
                [self.img_x_start + x, self.img_y_start + y, self.img[y][x], (x, y)]
                for x in range(self.img_width)
            ]
            for y in range(self.img_height)
        ]
        
        # Initialize direction board to track character movement
        self.direction_board = [
            [
                [
                    (
                        -1
                        if (self.end_board[y][x][0] - self.current_board[y][x][0]) < 0
                        else 1
                    ),
                    (
                        -1
                        if (self.end_board[y][x][1] - self.current_board[y][x][1]) < 0
                        else 1
                    ),
                ]
                for x in range(self.img_width)
            ]
            for y in range(self.img_height)
        ]

    def update_reverse(self, reverse: bool, start_reverse: int) -> None:
        """
        Updates the state of reverse and start_reverse attributes.

        Args:

            reverse (bool): Whether to enable or disable reverse.
            start_reverse (int): The frame number at which to start the reverse.

        Raises:

            Exception: If reverse is enabled but start_reverse is not provided,
                or if start_reverse is less than the current start_frame.
        """
        self.reverse = reverse
        self.start_reverse = start_reverse
        if start_reverse < self.start_frame:
            raise Exception(
                f"the frame to start the reverse can not be less than the start frame\n\tstart_frame: {self.start_frame}, start_reverse: {self.start_reverse}"
            )

    def update_start_frame(self, frame_number):
        """
        Updates the state of the start frame attribute.

        Args:

            frame_number (int): The new start frame number.

        Returns:
            None
        """
        self.start_frame = frame_number

    def solved(self, end_state):
        """
        Checks whether the current board is in a desired state.

        Args:

            end_state (str): The desired state to check against. Can be "end",
                "start", or any other value for custom checks.

        Returns:
            bool: Whether the current board matches the desired state.
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
            raise Exception(f"unknown solved board state for FocusRenderer: {end_state}")

    def render_img_frame(self, frame_number):
        """
        Renders the image on the screen based on the current frame number.

        Args:

            frame_number (int): The current frame number.

        Returns:
            None
        """
        if self.reverse and frame_number >= self.start_reverse:
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
                if self.loop:
                    self.loops += 1
                    self.start_frame = self.start_reverse + self.frame_gap
                    self.start_reverse = self.start_frame + self.frame_gap
                    self._set_img_attributes()
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
