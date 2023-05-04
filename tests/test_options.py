import pytest
from unittest.mock import MagicMock
from typing import Any, Dict
import dataclasses
from options import TitleOptions


@pytest.fixture
def default_title_options():
    return TitleOptions()


def test_title_options_init(default_title_options):
    assert isinstance(default_title_options, TitleOptions)


def test_title_options_eq(default_title_options):
    title_options_copy = TitleOptions()
    assert default_title_options == title_options_copy


def test_title_options_repr(default_title_options):
    assert (
        str(default_title_options)
        == "TitleOptions(text_kwargs={}, location='top', height=0.1, alignment='center', padding=0.01)"
    )


def test_title_options_valid_location(default_title_options):
    with pytest.raises(AssertionError):
        TitleOptions(location="left")


def test_title_options_valid_alignment(default_title_options):
    with pytest.raises(AssertionError):
        TitleOptions(alignment="top")


def test_title_options_valid_height(default_title_options):
    with pytest.raises(AssertionError):
        TitleOptions(height=2)


def test_title_options_valid_padding(default_title_options):
    with pytest.raises(AssertionError):
        TitleOptions(padding=2)


def test_title_options_height_padding_sum(default_title_options):
    with pytest.raises(AssertionError):
        TitleOptions(height=0.9, padding=0.2)
