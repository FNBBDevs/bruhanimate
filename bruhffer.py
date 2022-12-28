class Buffer:
    def __init__(self, height, width):
        self._height = height
        self._width = width
        line = [u" " for _ in range(self._width)]
        self.buffer = [line[:] for _ in range(self._height)]
    

    def get_buffer_changes(self, in_buf):
        """
        General application is front.get_changes(back)
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
        width = w if w else self._width
        height = h if h else self._height
        line = [u" " for _ in range(width)]

        if x == 0 and y == 0 and not w and not y:
            self.buffer = [line[:] for _ in range(height)]
        else:
            for i in range(y, y + height):
                self.buffer[i][x:x + width] = line[:]

    def get_char(self, x, y):
        return self.buffer[y][x]

    def put_char(self, x, y, val):
        if 0 <= y < self._height and 0 <= x < self._width:
            self.buffer[y][x] = val
        else:
            return
    
    def put_at(self, x, y, text):
        pass

    def grab_chunk(self, x, y, width):
        return self.buffer[y][x:x+width]

    def sync_with(self, in_buf):
        self.buffer = [line[:] for line in in_buf.buffer]

    def height(self):
        return self._height

    def width(self):
        return self._width