from unittest.mock import patch

from bruhanimate.bruhutil.utils import INF, VALID_EFFECTS, sleep


def test_sleep_function():
    """Test that the sleep function calls time.sleep and sys.stdout.flush."""
    with (
        patch("bruhanimate.bruhutil.utils.time.sleep") as mock_time_sleep,
        patch("bruhanimate.bruhutil.utils.sys.stdout.flush") as mock_flush,
    ):
        sleep(0.1)

        mock_flush.assert_called_once()
        mock_time_sleep.assert_called_once_with(0.1)


def test_constants():
    """Test that core constants are available and correct."""
    assert INF == float("inf")
    assert isinstance(VALID_EFFECTS, list)
    assert "static" in VALID_EFFECTS
    assert "rain" in VALID_EFFECTS
