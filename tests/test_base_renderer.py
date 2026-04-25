import pytest

from bruhanimate.bruhrenderer.base_renderer import BaseRenderer
from bruhanimate.bruhutil.bruherrors import InvalidEffectTypeError


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


class DummyRenderer(BaseRenderer):
    def render_img_frame(self, frame_number: int):
        pass


def test_base_renderer_init():
    screen = MockScreen(20, 40)
    renderer = DummyRenderer(screen, frames=10, frame_time=0.01, effect_type="static")

    assert renderer.height == 20
    assert renderer.width == 40
    assert renderer.frames == 10
    assert renderer.frame_time == 0.01
    assert renderer.effect_type == "static"
    assert renderer.background == " "


def test_base_renderer_invalid_effect():
    screen = MockScreen(20, 40)
    with pytest.raises(InvalidEffectTypeError):
        DummyRenderer(screen, effect_type="this_is_not_a_real_effect")


def test_base_renderer_swap_buffers():
    screen = MockScreen(10, 10)
    renderer = DummyRenderer(screen, effect_type="static")

    initial_current = renderer.current_buffer
    initial_display = renderer.display_buffer

    renderer.swap_buffers()

    assert renderer.current_buffer == initial_display
    assert renderer.display_buffer == initial_current


def test_base_renderer_clear_back_buffer():
    screen = MockScreen(5, 5)
    renderer = DummyRenderer(screen, effect_type="static", background=".")

    # Fill the back buffer with something else
    renderer.current_buffer.put_char(0, 0, "X")
    assert renderer.current_buffer.get_char(0, 0) == "X"

    renderer.clear_back_buffer()

    # Check that it got cleared to the background character
    assert renderer.current_buffer.get_char(0, 0) == "."


def test_base_renderer_update_exit_stats():
    screen = MockScreen(10, 10)
    renderer = DummyRenderer(screen, effect_type="static")

    renderer.update_exit_stats(
        msg1="HELLO", msg2="WORLD", wipe=True, x_loc=2, y_loc=3, centered=False
    )

    assert renderer.exit_messages["msg1"] == "HELLO"
    assert renderer.exit_messages["msg2"] == "WORLD"
    assert renderer.exit_messages["wipe"] is True
    assert renderer.exit_messages["x_loc"] == 2
    assert renderer.exit_messages["y_loc"] == 3
    assert renderer.exit_messages["centered"] is False
