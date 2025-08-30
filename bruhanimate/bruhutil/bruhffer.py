"""
Copyright 2023 Ethan Christensen
Copied, Guided, and Adapted from Asciimatics <https://github.com/peterbrittain/asciimatics/blob/master/asciimatics/screen.py>

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


class Buffer:
    """
    Class for creating and managing a buffer
    """

    def __init__(self, height, width):
        self._height = height
        self._width = width
        self._center = self._width // 2
        self._empty_line = [" " for _ in range(self._width)]
        self.buffer = [self._empty_line[:] for _ in range(self._height)]

    def get_buffer_changes(self, in_buf):
        """
        Compare this buffer with the given buffer and yield differences.

        Args:
            in_buf (Buffer): The buffer to compare with.

        Yields:
            Tuple[int, int, str]: A tuple containing the row index, column index,
                                  and the character from the input buffer that
                                  differs.
        """
        if self._height != in_buf.height() or self._width != in_buf.width():
            raise ValueError("Buffer dimensions must match")

        for y in range(self._height):
            for x in range(self._width):
                if self.buffer[y][x] != in_buf.buffer[y][x]:
                    yield y, x, in_buf.buffer[y][x]

    def clear_buffer(self, x=0, y=0, w=None, h=None, val=" "):
        """
        Clear a section of the buffer with a specific character.

        Args:
            x (int): The starting x-coordinate for the clear operation (default is 0).
            y (int): The starting y-coordinate for the clear operation (default is 0).
            w (int, optional): The width of the section to be cleared. If not specified,
                               clears to the end of the buffer's width.
            h (int, optional): The height of the section to be cleared. If not specified,
                               clears to the end of the buffer's height.
            val (str): The character to fill the cleared area with (default is a space).
        """
        width = w if w else self._width
        height = h if h else self._height
        line = [val for _ in range(width)]

        if x == 0 and y == 0 and not w and not h:
            self.buffer = [line[:] for _ in range(height)]
        else:
            for i in range(y, y + height):
                self.buffer[i][x : x + width] = line[:]

        return self

    def get_char(self, x, y):
        """
        Get the character at the specified location.

        Parameters:
            x (int): The column index.
            y (int): The row index.
        Returns:
            str or None: The character at the specified location, or None if out of bounds.
        """
        if 0 <= y < self._height and 0 <= x < self._width:
            return self.buffer[y][x]
        return None

    def put_char(self, x, y, val, transparent=False):
        """
        Place a character at the specified location.

        Parameters:
            x (int): The column index.
            y (int): The row index.
            val (str): The character to place.
            transparent (bool): If True, only place non-space characters.
        """
        if 0 <= y < self._height and 0 <= x < self._width:
            if self.buffer[y][x] != val:
                if transparent and val != " ":
                    self.buffer[y][x] = val
                elif not transparent:
                    self.buffer[y][x] = val

    def put_at(self, x, y, text, transparent=False):
        """
        Place text starting at the specified location.

        Parameters:
            x (int): The starting column index.
            y (int): The row index.
            text (str): The text to place.
            transparent (bool): If True, only place non-space characters.
        """
        if x < 0:
            text = text[-x:]
            x = 0

        if x + len(text) > self._width:
            text = text[: self._width - x]

        if not transparent:
            for i, c in enumerate(text):
                self.put_char(x + i, y, c)
        else:
            for i, c in enumerate(text):
                if c != " ":
                    self.put_char(x + i, y, c)

    def put_at_center(self, y, text, transparent=False):
        """
        Place text centered on the specified row.

        Parameters:
            y (int): The row index to place the text.
            text (str): The text to place.
            transparent (bool): If True, only place non-space characters.
        """
        if not transparent:
            x = self._center - len(text) // 2
            for i, c in enumerate(text):
                self.put_char(x + i, y, c)
        else:
            x = self._center - len(text) // 2
            for i, c in enumerate(text):
                if c != " ":
                    self.put_char(x + i, y, c)

    def scroll(self, shift):
        """
        Scroll the buffer up or down by a specified number of lines.

        Parameters:
            shift (int): The number of lines to scroll. Positive scrolls up, negative scrolls down.
        """
        if shift > 0:
            shift = min(shift, self._height)
            for y in range(0, self._height - shift):
                self.buffer[y] = self.buffer[y + shift]
            for y in range(self._height - shift, self._height):
                self.buffer[y] = self._line[:]
        else:
            shift = max(shift, -self._height)
            for y in range(self._height - 1, -shift - 1, -1):
                self.buffer[y] = self.buffer[y + shift]
            for y in range(0, -shift):
                self.buffer[y] = self._line[:]

    def shift_line(self, y, shift):
        """
        Shift the specified line to the right by a given amount.
        Args:
            y (int): The index of the row to shift.
            shift (int): The amount by which to shift the row.
        """
        self.buffer[y] = self.buffer[y][-shift:] + self.buffer[y][:-shift]

    def shift(self, shift):
        """
        Shift the entire buffer to the right by a specified amount.
        Args:
            shift (int): The amount by which to shift each row.
        """
        for y in range(self._height):
            self.buffer[y] = self.buffer[y][shift:] + self.buffer[y][:shift]

    def grab_slice(self, x, y, width):
        """
        Grab a segment from a specific row in the buffer.

        Args:
            x (int): The starting column index for the slice.
            y (int): The row index from which to grab the slice.
            width (int): Number of characters to include in the slice.

        Returns:
            list: A list containing the specified segment of the row.
        """
        return self.buffer[y][x : x + width]

    def sync_with(self, in_buf):
        """
        Synchronize this buffer with another buffer.
        Args:
            in_buf (Buffer): The buffer to synchronize with.
        """
        for y in range(self._height):
            self.buffer[y][:] = in_buf.buffer[y][:]

    def sync_over_top(self, in_buf):
        """
        Overlay non-None values from another buffer onto this buffer.

        Args:
            in_buf (Buffer): The buffer containing values to overlay.
        """
        for y in range(self._height):
            for x in range(self._width):
                if in_buf.buffer[y][x] is not None:
                    self.buffer[y][x] = in_buf.buffer[y][x]

    def height(self):
        """
        Get the height of the buffer.
        Returns:
            int: The height of the buffer.
        """
        return self._height

    def width(self):
        """
        Get the width of the buffer.

        Returns:
            int: The width of the buffer.
        """
        return self._width
