"""
A renderer that applies background colors to ASCII art.

This module provides functionality for rendering ASCII art with customizable background
colors. It extends the BaseRenderer class to add background color capabilities while
maintaining compatibility with other rendering features.

Example:
    Basic usage with a simple ASCII art image::

        from bruhanimate import Screen, BackgroundColorRenderer
        
        def demo(screen):
            renderer = BackgroundColorRenderer(
                screen=screen,
                img=["Hello", "World"],
                on_color_code=27  # Light blue background
            )
            renderer.run()
        
        Screen.show(demo)

Note:
    The background color is applied using ANSI color codes (0-255).
    Common colors include:

    - 27: Light blue
    
    - 196: Red
    
    - 46: Green
    
    - 226: Yellow
"""

from typing import List
from .base_renderer import BaseRenderer
from bruhcolor import bruhcolored
from ..bruhutil.bruhtypes import EffectType


class BackgroundColorRenderer(BaseRenderer):
    """
    A renderer that applies background colors to ASCII art.

    This renderer allows you to display ASCII art with a specified background color.
    It centers the image on the screen and maintains the original text appearance
    while adding the background color effect.

    Args:
        screen: The screen object to render to
        img (List[str]): The ASCII art image as a list of strings
        frames (int, optional): Number of frames to render. Defaults to 100.
        frame_time (float, optional): Time between frames in seconds. Defaults to 0.1.
        effect_type (EffectType, optional): The type of effect to apply. Defaults to "static".
        background (str, optional): Background character. Defaults to " ".
        transparent (bool, optional): Whether to use transparency. Defaults to False.
        collision (bool, optional): Whether to enable collision detection. Defaults to False.
        on_color_code (int, optional): ANSI color code (0-255) for background. Defaults to 27.

    Attributes:
        img (List[str]): The stored ASCII art image
        img_height (int): Height of the image in characters
        img_width (int): Width of the image in characters
        img_y_start (int): Starting Y position for centered image
        img_x_start (int): Starting X position for centered image
        current_img_x (int): Current X position during rendering
        current_img_y (int): Current Y position during rendering
        on_color_code (int): The ANSI color code for the background

    Raises:
        Exception: If no color code is provided or if the color code is invalid

    Example:
        Creating a renderer with a red background::

            renderer = BackgroundColorRenderer(
                screen=screen,
                img=["▄▄▄", "███", "▀▀▀"],
                on_color_code=196,  # Red background
                frame_time=0.05
            )
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
        on_color_code: int = 27,
    ):
        """Initialize the BackgroundColorRenderer with the specified parameters."""
        super(BackgroundColorRenderer, self).__init__(
            screen, frames, frame_time, effect_type, background, transparent, collision
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
        """
        Render a single frame of the image with the background color.

        This method applies the background color to each character of the image
        while maintaining the original character appearance. The image is centered
        on the screen.

        Args:
            frame_number (int): The current frame number being rendered

        Note:
            This method is called internally by the renderer's main loop.
            It should not typically be called directly.

        Example:
            Internal rendering process::

                for frame in range(frames):
                    renderer.render_img_frame(frame)
                    renderer.display_frame()
        """
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