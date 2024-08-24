import random

from bruhcolor import bruhcolored
from bruhutil import FLAKE_COLORS, FLAKE_FLIPS, FLAKE_JUMPS, FLAKE_WEIGHT_CHARS, FLAKES, NEXT_FLAKE_MOVE
from bruheffect import BaseEffect


class _FLAKE:
    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.weight = 1
        self.color = FLAKE_COLORS[index]
        self.char = bruhcolored(FLAKES[index], color=self.color).colored
        self.current_position = "center"
        self.on_ground = False
        self.full = False

    def flip_flake(self):
        if self.char == FLAKE_FLIPS[self.index][0]:
            self.char = FLAKE_FLIPS[self.index][1]
        else:
            self.char = FLAKE_FLIPS[self.index][0]

    def next_position(self, frame_number):
        if self.on_ground:
            return

        if frame_number % self.index != 0:
            return

        if random.random() < 0.10:
            return

        self.prev_x = self.x
        self.prev_y = self.y

        self.y = self.y + random.choice(FLAKE_JUMPS[self.index])

        next_position = random.choice(["left", "center", "right"])

        next_flake_move = (
            NEXT_FLAKE_MOVE[(self.current_position, next_position)]
            if self.current_position != next_position
            else None
        )

        if next_flake_move:
            self.x = self.x + next_flake_move
            self.current_position = next_position

    def update_position(self, x, y):
        self.prev_x = self.x
        self.prev_y = self.y
        self.x = x
        self.y = y

    def set_to_on_ground(self):
        self.weight = 1
        self.on_ground = True
        self.color = 190 if random.random() < 0.01 else 255
        self.char = bruhcolored(
            FLAKE_WEIGHT_CHARS[self.weight], color=self.color
        ).colored

    def increment_flake_weight(self):
        if self.weight < 18:
            self.weight += 1

        self.update_ground_flake()

        if self.weight == 18:
            self.full = True

    def update_ground_flake(self):
        if not self.full:
            if self.char != list(FLAKE_WEIGHT_CHARS.values())[-1]:
                if self.weight in FLAKE_WEIGHT_CHARS.keys():
                    self.char = bruhcolored(
                        FLAKE_WEIGHT_CHARS[self.weight], color=self.color
                    ).colored

    def __str__(self):
        return self.char

    def __repr__(self):
        return self.char

    def __len__(self):
        return 1

    def __eq__(self, other):
        return self.char == other

    def copy(self):
        new_flake = _FLAKE(index=self.index, x=self.x, y=self.y)
        new_flake.weight = self.weight
        new_flake.char = self.char
        new_flake.current_position = self.current_position
        new_flake.color = self.color
        new_flake.on_ground = self.on_ground
        new_flake.x = self.x
        new_flake.y = self.y
        new_flake.prev_x = self.prev_x
        new_flake.prev_y = self.prev_y
        new_flake.full = self.full
        return new_flake


class SnowEffect(BaseEffect):
    def __init__(
        self,
        buffer,
        background,
        img_start_x=None,
        img_start_y=None,
        img_width=None,
        img_height=None,
        collision=False,
        show_info=False,
    ):
        super(SnowEffect, self).__init__(buffer, background)
        self.image_present = (
            True if img_start_x and img_start_y and img_width and img_height else False
        )
        self.collision = collision
        self.total_ground_flakes = 0
        self._show_info = show_info
        self._flakes = []
        self._ground_flakes = [
            [None for _ in range(self.buffer.width())]
            for __ in range(self.buffer.height())
        ]
        self._image_collide_flakes = [None for _ in range(self.buffer.width())]
        self.smart_transparent = False

    def update_collision(
        self,
        img_start_x,
        img_start_y,
        img_width,
        img_height,
        collision,
        image_buffer=None,
    ):
        """
        Function to set whether or not to visually see the snow collide with the ground
        or images if they are present
        :param img_start_x: where the image starts on the screen
        :param img_start_y: where the image starts on the screen
        :param img_width:   the width of the image
        :param img_height:  the height of the image
        :param collision:   update collision variable
        """
        self.image_present = (
            True if img_start_x and img_start_y and img_width and img_height else False
        )
        self.collision = collision
        if self.image_present:
            self.img_start_x = img_start_x
            self.img_start_y = img_start_y
            self.img_height = img_height
            self.img_width = img_width
            self.img_end_y = img_start_y + img_height
            self.image_buffer = image_buffer
            self.image_x_boundaries = (img_start_x, img_start_x + img_width)
            self.image_y_boundaries = (img_start_y, img_start_y + img_height)
        else:
            self.image_buffer = None

    def show_info(self, show_info: bool):
        self._show_info = show_info

    def render_frame(self, frame_number):
        # calc each flakes next position
        for flake in self._flakes:
            flake.next_position(frame_number)

        # generate the next set of flakes
        for x in range(self.buffer.width()):
            if random.random() < 0.01:
                flake = _FLAKE(index=random.choice([1, 3, 7]), x=x, y=0)
                self._flakes.append(flake)

        if self.smart_transparent and frame_number == 0 and self.image_present:
            self.smart_boundLine = {}
            for x in range(self.img_width):
                tmp_flag = False
                for y in range(self.img_height):
                    if self.image_buffer.buffer[y + self.img_start_y][
                        x + self.img_start_x
                    ] not in [" ", None]:
                        self.smart_boundLine[x + self.img_start_x] = (
                            y + self.img_start_y - 1
                        )
                        tmp_flag = True
                        break
                if not tmp_flag:
                    self.smart_boundLine[x + self.img_start_x] = None

        # determine what flakes are hitting the ground or need to be deleted
        for idx, flake in enumerate(self._flakes):
            # ground flake
            if (
                flake.x >= 0
                and flake.x < self.buffer.width()
                and flake.y >= self.buffer.height() - 1
            ):
                # true_y = flake.y

                # need to set the y value to be the actual net available y val
                # what isn't a valid y value?
                # a -> value that exceeds the buffer height
                # b -> value that intercepts a full flake in the column
                true_y = None
                for y in range(self.buffer.height() - 1, -1, -1):
                    if (
                        self._ground_flakes[y][flake.x] is None
                        or not self._ground_flakes[y][flake.x].full
                    ):
                        true_y = y
                        break

                if true_y is None:
                    break

                if (
                    isinstance(self._ground_flakes[true_y][flake.x], _FLAKE)
                    and not self._ground_flakes[true_y][flake.x].full
                ):
                    ground_flake: _FLAKE = self._ground_flakes[true_y][flake.x]
                    ground_flake.increment_flake_weight()
                    self._ground_flakes[true_y][flake.x] = ground_flake.copy()
                    del ground_flake
                elif isinstance(self._ground_flakes[true_y][flake.x], _FLAKE):
                    tmp_flake = flake.copy()
                    tmp_flake.set_to_on_ground()
                    tmp_flake.y = true_y - 1
                    self._ground_flakes[true_y - 1][flake.x] = tmp_flake
                else:
                    tmp_flake = flake.copy()
                    tmp_flake.set_to_on_ground()
                    tmp_flake.y = true_y
                    self._ground_flakes[true_y][flake.x] = tmp_flake
                self._flakes[idx] = None
                self.buffer.put_char(flake.prev_x, flake.prev_y, " ")
            elif flake.x < 0 or flake.x >= self.buffer.width():
                self._flakes[idx] = None
                self.buffer.put_char(flake.prev_x, flake.prev_y, " ")
            else:
                # image collision flake
                if not self.smart_transparent:
                    if (
                        self.image_present
                        and flake.x >= self.image_x_boundaries[0]
                        and flake.x <= self.image_x_boundaries[1]
                        and flake.y >= self.image_y_boundaries[0]
                        and flake.y <= self.image_y_boundaries[1]
                    ):
                        # colliding with image
                        if isinstance(self._image_collide_flakes[flake.x], _FLAKE):
                            ground_flake: _FLAKE = self._image_collide_flakes[
                                flake.x
                            ].copy()
                            ground_flake.increment_flake_weight()
                            self._image_collide_flakes[flake.x] = ground_flake
                            del ground_flake
                        else:
                            tmp_flake = flake.copy()
                            tmp_flake.set_to_on_ground()
                            tmp_flake.y = self.image_y_boundaries[0] - 1
                            self._image_collide_flakes[flake.x] = tmp_flake
                        self._flakes[idx] = None
                        self.buffer.put_char(flake.prev_x, flake.prev_y, " ")
                elif frame_number != 0:
                    if self.image_present and flake.x in self.smart_boundLine.keys():
                        if start_bound := self.smart_boundLine[flake.x]:
                            if flake.y >= start_bound and flake.y <= self.img_end_y:
                                # colliding with image
                                self._flakes[idx] = None
                                self.buffer.put_char(flake.prev_x, flake.prev_y, " ")

                                if isinstance(
                                    self.buffer.get_char(flake.x, start_bound), _FLAKE
                                ):
                                    ground_flake: _FLAKE = self._image_collide_flakes[
                                        flake.x
                                    ].copy()
                                    ground_flake.increment_flake_weight()
                                    self._image_collide_flakes[flake.x] = ground_flake
                                    del ground_flake
                                else:
                                    tmp_flake = flake.copy()
                                    tmp_flake.set_to_on_ground()
                                    tmp_flake.y = start_bound
                                    self._image_collide_flakes[flake.x] = tmp_flake

        self._flakes = [flake for flake in self._flakes if flake]

        # place the flakes into the buffer
        for flake in self._flakes:
            self.buffer.put_char(flake.x, flake.y, flake)
            self.buffer.put_char(flake.prev_x, flake.prev_y, " ")

        # place the ground flakes
        if self.collision:
            for y in range(self.buffer.height()):
                for x in range(self.buffer.width()):
                    flake = self._ground_flakes[y][x]
                    if flake:
                        self.buffer.put_char(flake.x, flake.y, flake)
            for flake in self._image_collide_flakes:
                if flake:
                    self.buffer.put_char(flake.x, flake.y, flake)

        if self._show_info:
            self.buffer.put_at(0, 1, f"Width: {self.buffer.width()}")
            self.buffer.put_at(0, 2, f"Height: {self.buffer.height()}")
            self.buffer.put_at(0, 3, f"Collision Enabled: {self.collision}")
            self.buffer.put_at(0, 4, f"Total  flakes: {len(self._flakes):3d}")
            self.buffer.put_at(
                0,
                5,
                f"Ground flakes: {sum([sum([1 for x in range(len(self._ground_flakes[0])) if self._ground_flakes[y][x]]) for y in range(len(self._ground_flakes))]):3d}",
            )
            self.buffer.put_at(
                0,
                6,
                f"Full flakes: {sum([1 for flake in [j for sub in self._ground_flakes for j in sub] if flake and flake.full]):3d}",
            )
            self.buffer.put_at(0, 7, f"Image present: {self.image_present}")
            if self.image_present:
                self.buffer.put_at(
                    0,
                    8,
                    f"Total flakes on image: {len([0 for _ in self._image_collide_flakes if _]):3d}",
                )
                self.buffer.put_at(
                    0, 9, f"Image x boundaries: {self.image_x_boundaries}"
                )
                self.buffer.put_at(
                    0, 10, f"Image y boundaries: {self.image_y_boundaries}"
                )
                self.buffer.put_at(0, 11, f"Image y bottom: {self.img_end_y}")

        # for flake in [j for sub in self._ground_flakes for j in sub]:
        #     if flake:
        #         print(f"{flake.weight} - {flake.char} - {flake.full}")

