from bruhanimate.bruhutil.bruhffer import Buffer


def test_buffer_init():
    """Verify buffer initialization."""
    b = Buffer(10, 20)
    assert b.height() == 10
    assert b.width() == 20
    assert len(b.buffer) == 10
    assert len(b.buffer[0]) == 20


def test_buffer_put_char():
    """Test placing a character in the buffer."""
    b = Buffer(5, 5)
    b.put_char(2, 2, "X")
    assert b.get_char(2, 2) == "X"
    assert b.get_char(0, 0) == " "


def test_buffer_put_at():
    """Test placing a string in the buffer."""
    b = Buffer(5, 10)
    b.put_at(2, 1, "HELLO")
    # Buffer is a list of lists of characters
    assert "".join(b.buffer[1][2:7]) == "HELLO"


def test_buffer_clear():
    """Test clearing the buffer."""
    b = Buffer(5, 5)
    b.put_char(0, 0, "X")
    b.clear_buffer(val=".")
    for row in b.buffer:
        for char in row:
            assert char == "."


def test_buffer_get_char_out_of_bounds():
    """Ensure get_char returns None for out-of-bounds coordinates."""
    b = Buffer(5, 5)
    assert b.get_char(10, 10) is None
    assert b.get_char(-1, -1) is None
