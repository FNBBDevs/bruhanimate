from bruheffect import BaseEffect


class Line:
    def __init__(self, start_point, end_point):
        if start_point and end_point:
            self.start_point = (start_point[0] * 2, start_point[1] * 2)
            self.end_point = (end_point[0] * 2, end_point[1] * 2)
        else:
            self.start_point = None
            self.end_point = None

    def update_points(self, start_point, end_point):
        self.start_point = (start_point[0], start_point[1])
        self.end_point = (end_point[0], end_point[1])

    def get_points(self):
        return self.start_point, self.end_point


class DrawLinesEffect(BaseEffect):
    def __init__(self, buffer, background, char=None, thin=False):
        super(DrawLinesEffect, self).__init__(buffer, background)
        self.lines = []
        self.char = char
        self.thin = thin

    def add_line(self, start_point, end_point):
        self.lines.append(Line(start_point, end_point))

    def render_frame(self, frame_number):
        if frame_number == 0 and len(self.lines) > 0:
            for y in range(self.buffer.height()):
                self.buffer.put_at(0, y, self.background * self.buffer.width())
            for line in self.lines:
                if (
                    (line.start_point[0] < 0 and line.end_point[0]) < 0
                    or (
                        line.start_point[0] >= self.buffer.width() * 2
                        and line.end_point[0] > self.buffer.width() * 2
                    )
                    or (line.start_point[1] < 0 and line.end_point[1] < 0)
                    or (
                        line.start_point[1] >= self.buffer.height() * 2
                        and line.end_point[1] >= self.buffer.height() * 2
                    )
                ):
                    return

                line_chars = " ''^.|/7.\\|Ywbd#"
                dx = abs(line.end_point[0] - line.start_point[0])
                dy = abs(line.end_point[1] - line.start_point[1])

                cx = -1 if line.start_point[0] > line.end_point[0] else 1
                cy = -1 if line.start_point[1] > line.end_point[1] else 1

                def get_start(x, y):
                    c = self.buffer.get_char(x, y)
                    if c is not None:
                        return line_chars.find(c)
                    return 0

                def x_draw(ix, iy):
                    err = dx
                    px = ix - 2
                    py = iy - 2
                    next_char = 0
                    while ix != line.end_point[0]:
                        if ix < px or ix - px >= 2 or iy < py or iy - py >= 2:
                            px = ix & ~1
                            py = iy & ~1
                            next_char = get_start(px // 2, py // 2)
                        next_char |= 2 ** abs(ix % 2) * 4 ** (iy % 2)
                        err -= 2 * dy
                        if err < 0:
                            iy += cy
                            err += 2 * dx
                        ix += cx

                        if self.char is None:
                            self.buffer.put_char(
                                px // 2, py // 2, line_chars[next_char]
                            )
                        else:
                            self.buffer.put_char(px // 2, py // 2, self.char)

                def y_draw(ix, iy):
                    err = dy
                    px = ix - 2
                    py = iy - 2
                    next_char = 0

                    while iy != line.end_point[1]:
                        if ix < px or ix - px >= 2 or iy < py or iy - py >= 2:
                            px = ix & ~1
                            py = iy & ~1
                            next_char = get_start(px // 2, py // 2)
                        next_char |= 2 ** abs(ix % 2) * 4 ** (iy % 2)
                        err -= 2 * dx
                        if err < 0:
                            ix += cx
                            err += 2 * dy
                        iy += cy

                        if self.char is None:
                            self.buffer.put_char(
                                px // 2, py // 2, line_chars[next_char]
                            )
                        else:
                            self.buffer.put_char(px // 2, py // 2, self.char)

                if dy == 0 and self.thin and self.char is None:
                    pass
                elif dx > dy:
                    x_draw(line.start_point[0], line.start_point[1] + 1)
                else:
                    y_draw(line.start_point[0] + 1, line.start_point[1])
