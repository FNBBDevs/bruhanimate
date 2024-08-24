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
        self._line = line = [u" " for _ in range(self._width)]
        self.buffer = [self._line[:] for _ in range(self._height)]
    
    def get_buffer_changes(self, in_buf):
        """
        Return all the differences between this buffer
        and buffer that was passed in
        :param in_buf: buffer to compare this buffer to
        """
        if self._height != in_buf.height() or self._width != in_buf.width():
            return None

        for y in range(self._height):
            for x in range(self._width):
                if self.buffer[y][x] != in_buf.buffer[y][x]:
                    yield y, x, in_buf.buffer[y][x]

    def clear_buffer(self, x=0, y=0, w=None, h=None, val=" "):
        """
        Clear a section of this buffer
        :param x: x position to start the clear
        :param y: y position to start the clear
        :param w: width of the section to be cleared
        :param h: height of the section to be cleared
        """
        width = w if w else self._width
        height = h if h else self._height
        line = [val for _ in range(width)]

        if x == 0 and y == 0 and not w and not y:
            self.buffer = [line[:] for _ in range(height)]
        else:
            for i in range(y, y + height):
                self.buffer[i][x:x + width] = line[:]
        
        return self

    def get_char(self, x, y):
        """
        Return the value at the given location
        """
        try:
            return self.buffer[y][x]
        except Exception:
            return None

    def put_char(self, x, y, val, transparent=False):
        """
        Put the value at the given location
        """
        if 0 <= y < self._height and 0 <= x < self._width:
            if self.buffer[y][x] != val:
                if transparent and val != " ":  
                    self.buffer[y][x] = val
                else:
                    self.buffer[y][x] = val

    def put_at(self, x, y, text, transparent=False):
        """
        Put text at a given x, y coordinate in the buffer
        :param x:    column position to start placing the text
        :param y:    row position to start placing the text
        :param text: the text to be placed
        """
        if x < 0:
            text = text[-x:]
            x = 0
        
        if x + len(text) > self._width:
            text = text[:self._width-x]
        
        if not transparent:
            for i, c in enumerate(text):
                self.put_char(x+i, y, c)
        else:
            for i, c in enumerate(text):
                if c != " ":
                    self.put_char(x+i, y, c)
    
    def put_at_center(self, y, text, transparent=False):
        """
        Puts the given text in the center of the row given by y.
        :param y: row to place the text.
        :param text: text to write to the buffers.
        """
        if not transparent:
            x = self._center - len(text) // 2
            for i, c in enumerate(text):
                self.put_char(x+i, y, c)
        else:
            x = self._center - len(text) // 2
            for i, c in enumerate(text):
                if c != " ":
                    self.put_char(x+i, y, c)

    def scroll(self, shift):
        """
        Scrolls the buffer up or down a number of lines denoted
        by the shift value. '-' -> scroll down, '+' -> scroll up
        :param shift: amount to shift up or down
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
        Shift the given line to the right by the value denoted
        by shift.
        :param y:     index of the row to shift
        :param shift: amount to shift the row by
        """
        self.buffer[y] = self.buffer[y][-shift:] + self.buffer[y][:-shift]

    def shift(self, shift):
        """
        Shift the entire buffer to the right by the value denoted
        by shift
        :param shift: amount to shift the row by
        """
        for y in range(self._height):
            self.buffer[y] = self.buffer[y][shift:] + self.buffer[y][:shift]

    def grab_slice(self, x, y, width):
        """
        Grabs a part of a row from this buffer
        :param x:     column position to start grabbing
        :param y:     row position to start grabbing
        :param width: number of chracters to grab
        """
        return self.buffer[y][x:x+width]

    def sync_with(self, in_buf):
        """
        Sync this buffer with the given buffer
        :param in_buf: buffer to be applied to this buffer
        """
        for y in range(self._height):
            self.buffer[y][:] = in_buf.buffer[y][:]
    
    def sync_over_top(self, in_buf):
        """
        Apply non-none values over top this buffer from
        the in_buffer
        :param in_buf: buffer to take non-none values from
        """
        for y in range(self._height):
            for x in range(self._width):
                if in_buf.buffer[y][x] != None:
                    self.buffer[y][x] = in_buf.buffer[y][x]

    def height(self):
        return self._height

    def width(self):
        return self._width
