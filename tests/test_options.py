import pytest
from unittest.mock import MagicMock
from typing import Any, Dict
import dataclasses
from mpltable.options import TitleOptions, CellOptions, ColumnHeaderOptions


@pytest.fixture
def default_title_options():
    return TitleOptions()


class TestTitleOptions:
    def test_title_options_init(self, default_title_options):
        assert isinstance(default_title_options, TitleOptions)

    def test_title_options_eq(self, default_title_options):
        title_options_copy = TitleOptions()
        assert default_title_options == title_options_copy

    def test_title_options_repr(self, default_title_options):
        assert (
            str(default_title_options)
            == "TitleOptions(text_kwargs={}, location='top', height=0.1, alignment='center', padding=0.01, separator_kwargs={})"
        )

    def test_title_options_valid_location(self, default_title_options):
        with pytest.raises(AssertionError):
            TitleOptions(location="left")

    def test_title_options_valid_alignment(self, default_title_options):
        with pytest.raises(AssertionError):
            TitleOptions(alignment="top")

    def test_title_options_valid_height(self, default_title_options):
        with pytest.raises(AssertionError):
            TitleOptions(height=2)

    def test_title_options_valid_padding(self, default_title_options):
        with pytest.raises(AssertionError):
            TitleOptions(padding=2)

    def test_title_options_height_padding_sum(self, default_title_options):
        with pytest.raises(AssertionError):
            TitleOptions(height=0.9, padding=0.2)


class TestCellOptions:
    def test_default_values(self):
        cell_options = CellOptions()
        assert cell_options.alignment == "left"
        assert cell_options.padding == 0.01
        assert cell_options.text_kwargs == {}

    def test_valid_alignment(self):
        cell_options = CellOptions(alignment="center")
        assert cell_options.alignment == "center"

    def test_invalid_alignment(self):
        with pytest.raises(AssertionError):
            cell_options = CellOptions(alignment="middle")

    def test_valid_padding(self):
        cell_options = CellOptions(padding=0.5)
        assert cell_options.padding == 0.5

    def test_invalid_padding(self):
        with pytest.raises(AssertionError):
            cell_options = CellOptions(padding=-0.1)

    def test_custom_text_kwargs(self):
        cell_options = CellOptions(text_kwargs={"font_size": 12, "font_color": "blue"})
        assert cell_options.text_kwargs == {"font_size": 12, "font_color": "blue"}

    def test_custom_text_kwargs_empty_dict(self):
        cell_options = CellOptions(text_kwargs={})
        assert cell_options.text_kwargs == {}

    def test_custom_text_kwargs_none(self):
        cell_options = CellOptions(text_kwargs=None)
        assert cell_options.text_kwargs == {}


class TestColumnHeaderOptions:
    def test_default_values(self):
        column_header_options = ColumnHeaderOptions()
        assert column_header_options.alignment == "center"
        assert column_header_options.padding == 0.01
        assert column_header_options.text_kwargs == {}
        assert column_header_options.extend_column_separator == False

    def test_valid_alignment(self):
        column_header_options = ColumnHeaderOptions(alignment="center")
        assert column_header_options.alignment == "center"

    def test_invalid_alignment(self):
        with pytest.raises(AssertionError):
            column_header_options = ColumnHeaderOptions(alignment="middle")

    def test_valid_padding(self):
        column_header_options = ColumnHeaderOptions(padding=0.5)
        assert column_header_options.padding == 0.5

    def test_invalid_padding(self):
        with pytest.raises(AssertionError):
            column_header_options = ColumnHeaderOptions(padding=-0.1)

    def test_custom_text_kwargs(self):
        column_header_options = ColumnHeaderOptions(text_kwargs={"font_size": 12, "font_color": "blue"})
        assert column_header_options.text_kwargs == {
            "font_size": 12,
            "font_color": "blue",
        }

    def test_custom_text_kwargs_empty_dict(self):
        column_header_options = ColumnHeaderOptions(text_kwargs={})
        assert column_header_options.text_kwargs == {}

    def test_custom_text_kwargs_none(self):
        column_header_options = ColumnHeaderOptions(text_kwargs=None)
        assert column_header_options.text_kwargs == {}

    def test_extend_column_separator_true(self):
        column_header_options = ColumnHeaderOptions(extend_column_separator=True)
        assert column_header_options.extend_column_separator == True

    def test_extend_column_separator_false(self):
        column_header_options = ColumnHeaderOptions(extend_column_separator=False)
        assert column_header_options.extend_column_separator == False
