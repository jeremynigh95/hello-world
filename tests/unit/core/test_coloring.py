import pytest

from core.coloring import PALETTE, color_for_length


def test_black_for_first_band():
    assert color_for_length(1) == "#000000"
    assert color_for_length(10) == "#000000"


def test_empty_string_length_is_black():
    assert color_for_length(0) == "#000000"


def test_dark_blue_for_second_band():
    assert color_for_length(11) == "#00008B"
    assert color_for_length(20) == "#00008B"


def test_band_boundaries_advance_every_ten():
    assert color_for_length(21) == "#006400"
    assert color_for_length(31) == "#8B0000"


def test_lengths_beyond_palette_clamp_to_last_color():
    assert color_for_length(1000) == PALETTE[-1]


def test_negative_length_raises():
    with pytest.raises(ValueError):
        color_for_length(-1)
