class Buffer:
    """
    Class for creating and managing a buffer
    """
    def __init__(self, height, width):
        self._height = height
        self._width = width
        line = [u" " for _ in range(self._width)]
        self.buffer = [line[:] for _ in range(self._height)]
    
    def get_buffer_changes(self, in_buf):
        """
        Return all the differences between this buffer
        and buffer that was passed in
        :param in_buf: buffer to compare this buffer to
        """
        res = []
        if  self._height != len(in_buf.buffer) or self._width != len(in_buf.buffer[0]):
            return None
        for y in range(self._height):
            for x in range(self._width):
                if self.buffer[y][x] != in_buf.buffer[y][x]:
                    res.append((x, y, in_buf.buffer[y][x]))
        return res

    def clear_buffer(self, x=0, y=0, w=None, h=None):
        """
        Clear a section of this buffer
        :param x: x position to start the clear
        :param y: y position to start the clear
        :param w: width of the section to be cleared
        :param h: height of the section to be cleared
        """
        width = w if w else self._width
        height = h if h else self._height
        line = [u" " for _ in range(width)]

        if x == 0 and y == 0 and not w and not y:
            self.buffer = [line[:] for _ in range(height)]
        else:
            for i in range(y, y + height):
                self.buffer[i][x:x + width] = line[:]

    def get_char(self, x, y):
        """
        Return the value at the given location
        """
        return self.buffer[y][x]

    def put_char(self, x, y, val):
        """
        Put the value at the given location
        """
        if 0 <= y < self._height and 0 <= x < self._width:
            if self.buffer[y][x] != val:
                self.buffer[y][x] = val
        else:
            return
    
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
            self.buffer[y] = self.buffer[y][:x] + [c for c in text] + self.buffer[y][x + len(text):]
        else:
            for i, c in enumerate(text):
                if c != " ":
                    self.put_char(x+i, y, c)
    
    def put_at_center(self, y, text):
        """
        Puts the given text in the center of the row given by y.
        :param y: row to place the text.
        :param text: text to write to the buffers.
        """
        x = (self._width // 2) - len(text) // 2
        for i, c in enumerate(text):
            self.put_char(x+i, y, c)
        
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
        updates = self.get_buffer_changes(in_buf)
        for update in updates:
            self.buffer[update[1]][update[0]] = update[2]

    def height(self):
        """
        Height attribute
        """
        return self._height

    def width(self):
        """
        Width attribute
        """
        return self._width