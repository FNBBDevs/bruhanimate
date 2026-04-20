"""Headless unit tests for the double-buffer rendering optimizations."""
from bruhanimate.bruhutil.bruhffer import Buffer


def make(h, w, val):
    b = Buffer(h, w)
    b.clear_buffer(val=val)
    return b


def test_row_skip():
    a = Buffer(5, 10)
    b = Buffer(5, 10)
    a.clear_buffer(val='x')
    b.clear_buffer(val='x')
    b.put_char(3, 2, 'Y')

    changes = list(a.get_buffer_changes(b))
    assert changes == [(2, 3, 'Y')], f"expected [(2,3,'Y')], got {changes}"
    print("PASS  row-skip: only 1 changed cell yielded out of 50")


def test_identical_buffers():
    a = Buffer(10, 20)
    b = Buffer(10, 20)
    assert list(a.get_buffer_changes(b)) == []
    print("PASS  identical buffers: zero changes yielded")


def test_pointer_rotation():
    """
    Simulate two frames of the 3-buffer pointer rotation that replaced sync_with.
    Verifies that last_displayed and current_buffer track correctly without any data copy.
    """
    current  = make(4, 8, 'A')
    display  = make(4, 8, 'B')
    last_dis = make(4, 8, ' ')

    # --- Frame 0 ---
    current.clear_buffer(val='0')                    # render_to_back_buffer
    current, display = display, current              # swap_buffers -> display='0', current='B'

    changes = list(last_dis.get_buffer_changes(display))
    assert len(changes) == 32, f"frame0: expected 32 changes, got {len(changes)}"

    last_dis, current = display, last_dis            # pointer rotation

    assert last_dis.buffer[0][0] == '0', "last_dis should now track frame 0"
    assert current.buffer[0][0] == ' ',  "current should be the recycled slot"

    # --- Frame 1 ---
    current.clear_buffer(val='1')                    # render_to_back_buffer (clears recycled slot)
    current, display = display, current              # swap_buffers -> display='1', current='0'

    changes = list(last_dis.get_buffer_changes(display))
    assert len(changes) == 32,      f"frame1: expected 32 changes, got {len(changes)}"
    assert changes[0][2] == '1',    f"changed value should be '1', got {changes[0][2]}"

    last_dis, current = display, last_dis

    assert last_dis.buffer[0][0] == '1', "last_dis should now track frame 1"
    assert current.buffer[0][0] == '0', "current should be recycled frame-0 slot"

    print("PASS  pointer rotation: 3-buffer swap correct over 2 frames (no sync_with copy)")


def test_screen_batching():
    """Mock the Screen interface to verify begin_frame/flush_frame accumulates correctly."""

    class MockScreen:
        def __init__(self):
            self._buffering = False
            self._frame_parts = []
            self._current_x = 0
            self._current_y = 0
            self.writes = []

        def begin_frame(self):
            self._buffering = True
            self._frame_parts = []

        def print_at(self, text, x, y, width):
            # Mirrors the new Windows path: ANSI cursor seq + text
            cursor = (
                f"\x1b[{y+1};{x+1}H"
                if x != self._current_x or y != self._current_y
                else ""
            )
            piece = cursor + str(text)
            if self._buffering:
                self._frame_parts.append(piece)
            else:
                self.writes.append(piece)
            self._current_x = x + width
            self._current_y = y

        def flush_frame(self):
            if self._frame_parts:
                self.writes.append("".join(self._frame_parts))
                self._frame_parts = []
            self._buffering = False

    screen = MockScreen()

    # Simulate present_frame calling print_at for 5 changed cells in a row
    screen.begin_frame()
    for i in range(5):
        screen.print_at(str(i), i, 0, 1)
    screen.flush_frame()

    assert len(screen.writes) == 1, f"expected 1 batched write, got {len(screen.writes)}"
    # Cursor starts at (0,0) so the first cell at (0,0) needs no seq; adjacent cells also omit it
    assert screen.writes[0] == "01234", f"got {screen.writes[0]!r}"
    print("PASS  screen batching (ANSI path): 5 adjacent cells -> 1 write, no redundant cursor seqs")

    # Non-adjacent cells each get their own cursor sequence
    screen._current_x = -1  # force cursor mismatch on next call
    screen.begin_frame()
    screen.print_at("A", 0, 0, 1)   # cursor moved -> seq added
    screen.print_at("B", 5, 2, 1)   # non-adjacent -> seq added
    screen.flush_frame()

    assert len(screen.writes) == 2, f"expected 2 total writes, got {len(screen.writes)}"
    assert screen.writes[1] == "\x1b[1;1HA\x1b[3;6HB", f"got {screen.writes[1]!r}"
    print("PASS  screen batching (ANSI path): non-adjacent cells each carry cursor seq")

    # Calls outside begin/flush go direct (not buffered)
    screen.print_at("X", 10, 0, 1)
    assert len(screen.writes) == 3, f"expected 3 writes after direct call, got {len(screen.writes)}"
    print("PASS  screen batching: direct print_at (outside frame) writes immediately")


if __name__ == "__main__":
    test_row_skip()
    test_identical_buffers()
    test_pointer_rotation()
    test_screen_batching()
    print("\nAll tests passed.")
