"""
Top level Table class that is used to draw the table
on the provided ax object.
"""

import pandas as pd
from matplotlib.axes import Axes
import numpy as np
from typing import Dict, Any
from mpltable.options import (
    TitleOptions,
    BorderOptions,
    CellOptions,
    ColumnHeaderOptions,
)
import math


class Table:
    def __init__(
        self,
        data: pd.DataFrame,
        ax: Axes,
        show_column_names: bool = True,
        col_widths: Dict[str, float] = None,
        col_header_options: Dict[str, Any] = None,
        cell_options: Dict[str, Any] = None,
        table_title: str = None,
        title_options: Dict[str, Any] = None,
        background_color: str = None,
        header_separator_kwargs: Dict[str, Any] = None,
        column_separator_kwargs: Dict[str, Any] = None,
        row_separator_kwargs: Dict[str, Any] = None,
        border_options: Dict[str, Dict[str, Any]] = None,
    ):
        self._data = data
        self._ax = ax
        self._show_column_names = show_column_names
        self._col_header_options = (
            ColumnHeaderOptions(**col_header_options) if col_header_options else ColumnHeaderOptions()
        )
        self._cell_options = CellOptions(**cell_options) if cell_options else CellOptions()
        self._table_title = table_title
        self._title_options = TitleOptions(**title_options) if title_options else TitleOptions()
        self._col_widths = col_widths or {}
        self._background_color = background_color
        self._header_separator_kwargs = header_separator_kwargs or {}
        self._column_separator_kwargs = column_separator_kwargs or {}
        self._row_separator_kwargs = row_separator_kwargs or {}
        self._border_options = BorderOptions(**border_options) if border_options else BorderOptions()
        self._validate_settings()

    @property
    def show_column_names(self):
        """
        Whether to show the column names in the table.
        """
        return self._show_column_names

    @show_column_names.setter
    def show_column_names(self, value):
        self._show_column_names = value

    @property
    def data(self):
        """
        The data of the table.
        """
        return self._data

    @property
    def table_title(self):
        """
        The title of the table.
        """
        return self._table_title

    @table_title.setter
    def table_title(self, value):
        self._table_title = value

    @property
    def background_color(self):
        """
        The background color of the table.
        """
        return self._background_color

    @background_color.setter
    def background_color(self, value):
        self._background_color = value

    @property
    def header_separator_kwargs(self):
        """
        The keyword arguments to pass to the line rendering function for the header separator.
        """
        return self._header_separator_kwargs

    @header_separator_kwargs.setter
    def header_separator_kwargs(self, value):
        self._header_separator_kwargs = value or {}

    @property
    def column_separator_kwargs(self):
        """
        The keyword arguments to pass to the line rendering function for the column separators.
        """
        return self._column_separator_kwargs

    @column_separator_kwargs.setter
    def column_separator_kwargs(self, value):
        self._column_separator_kwargs = value or {}

    @property
    def row_separator_kwargs(self):
        """
        The keyword arguments to pass to the line rendering function for the row separators.
        """
        return self._row_separator_kwargs

    @row_separator_kwargs.setter
    def row_separator_kwargs(self, value):
        self._row_separator_kwargs = value or {}

    @property
    def col_header_options(self) -> ColumnHeaderOptions:
        """
        The options for the column headers.
        """
        return self._col_header_options

    @property
    def cell_options(self) -> CellOptions:
        """
        The options for the cells.
        """
        return self._cell_options

    @property
    def col_widths(self):
        """
        The column widths of the table.
        """
        return self._col_widths

    @col_widths.setter
    def col_widths(self, value):
        self._col_widths = value or {}

    @property
    def border_options(self) -> BorderOptions:
        """
        The border options for the table.
        """
        return self._border_options

    def _validate_settings(self):
        """
        Validate the provided settings.
        """

        self._validate_col_widths()

    def _validate_col_widths(self):
        """
        Validate the provided column widths.
        """
        if not self._col_widths:
            return
        assert isinstance(self._col_widths, dict), f"col_widths must be a dictionary, got {type(self._col_widths)}"
        assert all(
            isinstance(key, str) for key in self._col_widths.keys()
        ), f"col_widths keys must be strings, got {self._col_widths.keys()}"
        assert all(
            isinstance(value, (int, float)) for value in self._col_widths.values()
        ), f"col_widths values must be numbers, got {self._col_widths.values()}"
        assert all(
            0 <= value <= 1 for value in self._col_widths.values()
        ), f"col_widths values must be between 0 and 1, got {self._col_widths.values()}"
        assert np.isclose(
            sum(self._col_widths.values()), 1
        ), f"col_widths values must sum to 1, got {sum(self._col_widths.values())}"
        assert set(self._col_widths.keys()) == set(
            self._data.columns
        ), f"col_widths keys must match the column names in the data, got {set(self._col_widths.keys())} and {set(self._data.columns)}"

    def _boundaries_from_user_provided_col_widths(self):
        """
        Calculate the cell boundaries from the user provided column widths.
        """
        boundaries = [0]
        for col_name in self._data.columns:
            boundaries.append(boundaries[-1] + self._col_widths[col_name])
        return boundaries

    def _setup_x_cell_boundaries(self):
        """
        Setup the x cell boundaries.
        """
        if self._col_widths:
            self._x_cell_bondaries = self._boundaries_from_user_provided_col_widths()
        else:
            if self._data.shape[1] == 0:
                raise ValueError("The table has no columns")
            self._x_cell_bondaries = np.linspace(0, 1, self._data.shape[1] + 1)

    def _setup_table_boundaries(self):
        """
        Setup the table title boundaries.
        """

        if self._title_options.location == "top" and self._table_title is not None:
            self._table_title_boundaries = np.array(
                [
                    1 - self._title_options.height,
                    1,
                ]
            )
            self._table_boundaries = np.array(
                [
                    0,
                    1 - self._title_options.height,
                ]
            )
        elif self._title_options.location == "bottom" and self._table_title is not None:
            self._table_title_boundaries = np.array(
                [
                    0,
                    self._title_options.height,
                ]
            )
            self._table_boundaries = np.array(
                [
                    self._title_options.height,
                    1,
                ]
            )
        else:
            self._table_title_boundaries = np.array(
                [
                    0,
                    0,
                ]
            )
            self._table_boundaries = np.array(
                [
                    0,
                    1,
                ]
            )

    def _setup_y_cell_boundaries(self):
        """
        Setup the y cell boundaries.
        """
        n_rows = self.data.shape[0] + 1 if self.show_column_names else self.data.shape[0]

        self._y_cell_bondaries = np.linspace(self._table_boundaries[1], self._table_boundaries[0], n_rows + 1)

    def _create_dimensions(self):
        """
        Create the dimensions of the table.
        """
        self._setup_table_boundaries()
        self._setup_x_cell_boundaries()
        self._setup_y_cell_boundaries()

    def _setup_ax(self):
        """
        Setup the ax object.
        """
        self._ax.set_xlim(0, 1)
        self._ax.set_ylim(0, 1)
        if self._background_color:
            for spine in self._ax.spines.values():
                spine.set_visible(False)
            self._ax.set_xticks([])
            self._ax.set_yticks([])
            if self._background_color:
                self._ax.set_facecolor(self._background_color)
        else:
            self._ax.axis("off")

    def _draw_column_names(self):
        """
        Draw the column names on the table.
        """
        for i, column_name in enumerate(self._data.columns):
            x = self._get_cell_x_coordinate(
                self._x_cell_bondaries[i],
                self._x_cell_bondaries[i + 1],
                self._col_header_options.padding,
                self._col_header_options.alignment,
            )
            y = (self._y_cell_bondaries[0] + self._y_cell_bondaries[1]) / 2
            self._ax.text(
                x,
                y,
                column_name,
                ha=self._col_header_options.alignment,
                va="center",
                **self._col_header_options.text_kwargs,
            )

    @staticmethod
    def _get_cell_x_coordinate(left_boundary: float, right_boundary: float, padding: float, alignment: str):
        """
        create cell text x coordinate
        """
        assert 0 <= padding <= 1, f"padding must be between 0 and 1, got {padding}"
        assert alignment in [
            "left",
            "right",
            "center",
        ], f"alignment must be one of 'left', 'right', or 'center', got {alignment}"
        assert (
            left_boundary < right_boundary
        ), f"left_boundary must be less than right_boundary, got {left_boundary} and {right_boundary}"

        if alignment == "left":
            return left_boundary + padding
        elif alignment == "right":
            return right_boundary - padding
        elif alignment == "center":
            return (left_boundary + right_boundary) / 2

        raise ValueError(f"Invalid alignment option: {alignment}")

    def _draw_the_cell_text(self, i: int, j: int, cell):
        """
        Draw the text of the cell.
        """

        x = self._get_cell_x_coordinate(
            self._x_cell_bondaries[j],
            self._x_cell_bondaries[j + 1],
            self._cell_options.padding,
            self._cell_options.alignment,
        )
        y = (self._y_cell_bondaries[i] + self._y_cell_bondaries[i + 1]) / 2
        self._ax.text(
            x,
            y,
            cell,
            ha=self._cell_options.alignment,
            va="center",
            **self._cell_options.text_kwargs,
        )

    def _draw_cell_texts(self):
        """
        Draw the cell texts on the table.
        """
        for i, row in self._data.iterrows():
            for j, cell in enumerate(row):
                self._draw_the_cell_text(i + int(self._show_column_names), j, cell)

    def _get_title_x_loc(self):
        """
        Get the x location of the title.
        """
        if self._title_options.alignment == "left":
            x = self._title_options.padding
        elif self._title_options.alignment == "right":
            x = 1 - self._title_options.padding
        else:
            x = 0.5

        return x

    def _draw_table_title(self):
        """
        Draw the table title on the table.
        """

        x = self._get_title_x_loc()

        y = (self._table_title_boundaries[0] + self._table_title_boundaries[1]) / 2
        self._ax.text(
            x,
            y,
            self._table_title,
            ha=self._title_options.alignment,
            va="center",
            **self._title_options.text_kwargs,
        )

    def _draw_title_separator_line(self):
        self._ax.hlines(
            self._table_title_boundaries[0],
            0,
            1,
            **self._title_options.separator_kwargs,
        )

    def _draw_header_separator_line(self):
        self._ax.hlines(
            self._y_cell_bondaries[1],
            0,
            1,
            **self._header_separator_kwargs,
        )

    def _draw_column_separator_lines(self):
        if self.show_column_names and not self.col_header_options.extend_column_separator:
            start = 1
        else:
            start = 0
        for x in self._x_cell_bondaries[1:-1]:
            self._ax.vlines(
                x,
                self._y_cell_bondaries[start],
                self._table_boundaries[0],
                **self._column_separator_kwargs,
            )

    def _draw_row_separator_lines(self):
        if self._show_column_names:
            start = 2
        else:
            start = 1

        self._ax.hlines(
            self._y_cell_bondaries[start:-1],
            0,
            1,
            **self._row_separator_kwargs,
        )

    def _draw_separator_lines(self):
        if self._table_title and self._title_options.separator_kwargs:
            self._draw_title_separator_line()
        if self._show_column_names and self._header_separator_kwargs:
            self._draw_header_separator_line()
        if self._column_separator_kwargs:
            self._draw_column_separator_lines()
        if self._row_separator_kwargs:
            self._draw_row_separator_lines()

    def _draw_bottom_border(self):
        if self._border_options.bottom:
            self._ax.hlines(
                self._table_boundaries[0],
                0,
                1,
                **self._border_options.bottom,
            )

    def _draw_top_border(self):
        if self._border_options.top:
            self._ax.hlines(
                self._table_boundaries[1],
                0,
                1,
                **self._border_options.top,
            )

    def _draw_left_border(self):
        if self._border_options.left:
            self._ax.vlines(
                0,
                self._table_boundaries[0],
                self._table_boundaries[1],
                **self._border_options.left,
            )

    def _draw_right_border(self):
        if self._border_options.right:
            self._ax.vlines(
                1,
                self._table_boundaries[0],
                self._table_boundaries[1],
                **self._border_options.right,
            )

    def _draw_borders(self):
        self._draw_bottom_border()
        self._draw_top_border()
        self._draw_left_border()
        self._draw_right_border()

    def draw(self):
        """
        Draw the table on the provided ax object.
        """
        self._create_dimensions()
        self._setup_ax()

        if self._table_title is not None:
            self._draw_table_title()

        if self._show_column_names:
            self._draw_column_names()

        self._draw_separator_lines()
        self._draw_borders()

        self._draw_cell_texts()
