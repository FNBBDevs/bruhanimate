import pytest

from bruhanimate.bruhutil.bruherrors import InvalidImageError
from bruhanimate.bruhutil.bruhimage import get_image, text_to_image


def test_get_image_valid():
    img = get_image("hey")
    assert isinstance(img, list)
    assert len(img) > 0
    assert isinstance(img[0], str)


def test_get_image_invalid():
    with pytest.raises(InvalidImageError):
        get_image("this_image_does_not_exist")


def test_text_to_image_basic():
    # pyfiglet is required for this to work properly
    img = text_to_image("TEST")
    assert isinstance(img, list)
    assert len(img) > 0

    # Ensure all lines are padded to the same length
    length = len(img[0])
    for line in img:
        assert len(line) == length


def test_text_to_image_padding():
    img = text_to_image("TEST", padding_top_bottom=2, padding_left_right=3)

    # Top 2 lines should be empty spaces
    assert img[0].strip() == ""
    assert img[1].strip() == ""

    # Bottom 2 lines should be empty spaces
    assert img[-1].strip() == ""
    assert img[-2].strip() == ""

    # Middle line should start with 3 spaces
    assert img[2].startswith("   ")
    assert img[2].endswith("   ")
