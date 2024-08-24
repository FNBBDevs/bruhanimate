from ..bruhutil import Screen
from .base_renderer import BaseRenderer



class CenterRenderer(BaseRenderer):
    """
    A renderer to load an image in the center of the screen.
    Updates the image_buffer only
    """

    def __init__(
        self,
        screen: Screen,
        img: list[str],
        frames: int = 100,
        time: float = 0.1,
        effect_type: str = "static",
        background: str = " ",
        transparent: bool = False,
    ):
        super(CenterRenderer, self).__init__(
            screen, frames, time, effect_type, background, transparent
        )
        self.background = background
        self.transparent = transparent

        # Image attributes
        self.img = img
        self.img_height = len(self.img)
        self.img_width = len(self.img[0])
        self.img_y_start = (self.height - self.img_height) // 2
        self.img_x_start = (self.width - self.img_width) // 2
        self.current_img_x = self.img_x_start
        self.current_img_y = self.img_y_start
        self.none_fill_char = None

    def render_img_frame(self, frame_number):
        """
        Renders out the image to the center of the screen,
        if there is no image passed into the renderer then
        the background is rendered on it's own
        """

        # Image is only rendered once, on frame 0
        if frame_number == 0:
            if self.smart_transparent:
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
                            y,
                            self.img[y - self.img_y_start],
                            transparent=self.transparent,
                        )