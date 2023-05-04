"""
Top level Table class that is used to draw the table
on the provided ax object.
"""

import pandas as pd
from matplotlib.axes import Axes
import numpy as np
from typing import Dict, Any
from options import TitleOptions


class Table:
    def __init__(
        self,
        data: pd.DataFrame,
        ax: Axes,
        show_column_names: bool = True,
        col_headers_text_kwargs: Dict[str, Any] = None,
        cell_text_kwargs: Dict[str, Any] = None,
        table_title: str = None,
        title_options: Dict[str, Any] = None,
    ):
        self._data = data
        self._ax = ax
        self._show_column_names = show_column_names
        self._col_headers_text_kwargs = col_headers_text_kwargs or {}
        self._cell_text_kwargs = cell_text_kwargs or {}
        self._table_title = table_title
        self._title_options = TitleOptions(**title_options) if title_options else TitleOptions()

        self._create_dimensions()

    def _setup_x_cell_boundaries(self):
        """
        Setup the x cell boundaries.
        """
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
        n_rows = self._data.shape[0] + 1 if self._show_column_names else self._data.shape[0]

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
        self._ax.axis("off")

    def _draw_column_names(self):
        """
        Draw the column names on the table.
        """
        for i, column_name in enumerate(self._data.columns):
            x = (self._x_cell_bondaries[i] + self._x_cell_bondaries[i + 1]) / 2
            y = (self._y_cell_bondaries[0] + self._y_cell_bondaries[1]) / 2
            self._ax.text(x, y, column_name, ha="center", va="center", **self._col_headers_text_kwargs)

    def _draw_the_cell_text(self, i: int, j: int, cell):
        """
        Draw the text of the cell.
        """
        x = (self._x_cell_bondaries[j] + self._x_cell_bondaries[j + 1]) / 2
        y = (self._y_cell_bondaries[i] + self._y_cell_bondaries[i + 1]) / 2
        self._ax.text(x, y, cell, ha="center", va="center", **self._cell_text_kwargs)

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
            x, y, self._table_title, ha=self._title_options.alignment, va="center", **self._title_options.text_kwargs
        )

    def draw(self):
        """
        Draw the table on the provided ax object.
        """
        self._setup_ax()

        if self._table_title is not None:
            self._draw_table_title()

        if self._show_column_names:
            self._draw_column_names()

        self._draw_cell_texts()
