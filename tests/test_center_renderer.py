from bruhanimate.bruhrenderer.center_renderer import CenterRenderer


class MockScreen:
    def __init__(self, height=20, width=40):
        self.height = height
        self.width = width

    def begin_frame(self):
        pass

    def flush_frame(self):
        pass

    def print_at(self, text, x, y, width):
        pass

    def has_resized(self):
        return False


def test_center_renderer_init():
    screen = MockScreen(20, 40)
    img = ["HELLO", "WORLD"]
    renderer = CenterRenderer(
        screen, img, frames=10, frame_time=0.01, effect_type="static"
    )

    assert renderer.img == img
    assert renderer.img_height == 2
    assert renderer.img_width == 5
    assert renderer.img_x_start == (40 - 5) // 2
    assert renderer.img_y_start == (20 - 2) // 2


def test_center_renderer_render_img_frame():
    screen = MockScreen(10, 20)
    img = ["XXX", "XXX"]
    renderer = CenterRenderer(screen, img, frames=10, effect_type="static")

    # Render the first frame (where image is placed)
    renderer.render_img_frame(0)

    # Check if the image buffer contains the image at the center
    # Center y: (10-2)//2 = 4
    # Center x in put_at_center: width//2 - len(text)//2 -> 10 - 3//2 -> 9
    assert renderer.image_buffer.get_char(9, 4) == "X"
    assert renderer.image_buffer.get_char(10, 4) == "X"
    assert renderer.image_buffer.get_char(11, 4) == "X"
    assert renderer.image_buffer.get_char(9, 5) == "X"
    assert renderer.image_buffer.get_char(10, 5) == "X"
    assert renderer.image_buffer.get_char(11, 5) == "X"

    # Check surrounding area
    assert (
        renderer.image_buffer.get_char(8, 4) is None
        or renderer.image_buffer.get_char(8, 4) == " "
    )
    assert (
        renderer.image_buffer.get_char(9, 3) is None
        or renderer.image_buffer.get_char(9, 3) == " "
    )


def test_center_renderer_render_img_frame_smart_transparent():
    screen = MockScreen(10, 20)
    img = [" X ", "XXX"]
    renderer = CenterRenderer(screen, img, frames=10, effect_type="static")
    renderer.update_smart_transparent(True)

    renderer.render_img_frame(0)

    # Center y: (10-2)//2 = 4
    # smart_transparent uses img_x_start: (20-3)//2 = 8
    assert renderer.image_buffer.get_char(9, 4) == "X"
    assert renderer.image_buffer.get_char(8, 4) is None  # It was a space " X "
