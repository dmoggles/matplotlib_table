import dataclasses
from typing import Dict, Any


@dataclasses.dataclass(eq=True, repr=True, init=True)
class TitleOptions:
    """
    Provides options for configuring the appearance and positioning of a title in a table.

    Attributes:
    - text_kwargs: A dictionary of keyword arguments to pass to the text rendering function for the title.
    - location: A string indicating the location of the title, either "top" or "bottom".
    - height: A float between 0 and 1 indicating the height of the title as a fraction of the total height of the table.
    - alignment: A string indicating the horizontal alignment of the title, either "left", "center", or "right".
    - padding: A float between 0 and 1 indicating the amount of padding to add around the title as a fraction of its height.
    - separator_kwargs: A dictionary of keyword arguments to pass to the line rendering function for the separator line between the title and the table.
            If None, no separator line is drawn.

    Methods:
    - __post_init__(self): A special method that is called after the class is initialized to check that the specified options are valid.
      Raises an AssertionError if any of the options are invalid.
    """

    text_kwargs: Dict[str, Any] = None
    location: str = "top"
    height: float = 0.1
    alignment: str = "center"
    padding: float = 0.01
    separator_kwargs: Dict[str, Any] = None

    def __post_init__(self):
        self.text_kwargs = self.text_kwargs or {}
        self.separator_kwargs = self.separator_kwargs or {}
        assert self.location in ["top", "bottom"]
        assert self.alignment in ["left", "center", "right"]
        assert 0 <= self.height <= 1
        assert 0 <= self.padding <= 1
        assert self.height + self.padding <= 1


@dataclasses.dataclass(eq=True, repr=True, init=True)
class BorderOptions:
    """
    Provides options for configuring the appearance of the borders of a table.

    Attributes:
    - bottom: A dictionary of keyword arguments to pass to the line rendering function for the bottom border of the table.
            If None, no bottom border is drawn.
    - top: A dictionary of keyword arguments to pass to the line rendering function for the top border of the table.
            If None, no top border is drawn.
    - left: A dictionary of keyword arguments to pass to the line rendering function for the left border of the table.
            If None, no left border is drawn.
    - right: A dictionary of keyword arguments to pass to the line rendering function for the right border of the table.
            If None, no right border is drawn.

    """

    bottom: Dict[str, Any] = None
    top: Dict[str, Any] = None
    left: Dict[str, Any] = None
    right: Dict[str, Any] = None

    def __post_init__(self):
        self.bottom = self.bottom or {}
        self.top = self.top or {}
        self.left = self.left or {}
        self.right = self.right or {}


@dataclasses.dataclass(eq=True, repr=True, init=True)
class CellOptions:
    """
    Provides options for configuring the appearance of the cells in a table.

    Attributes:
    - text_kwargs: A dictionary of keyword arguments to pass to the text rendering function for the cells.
    - padding: A float between 0 and 1 indicating the amount of padding to add around the text in each cell as a fraction of the height of the cell.
    - alignment: A string indicating the horizontal alignment of the text in each cell, either "left", "center", or "right".
    """

    alignment: str = "left"
    padding: float = 0.01
    text_kwargs: Dict[str, Any] = None

    def __post_init__(self):
        self.text_kwargs = self.text_kwargs or {}
        assert self.alignment in ["left", "center", "right"]
        assert 0 <= self.padding <= 1


@dataclasses.dataclass(eq=True, repr=True, init=True)
class ColumnHeaderOptions:
    """
    Provides options for configuring the appearance of the column headers in a table.

    Attributes:
    - text_kwargs: A dictionary of keyword arguments to pass to the text rendering function for the column headers.
    - padding: A float between 0 and 1 indicating the amount of padding to add around the text in each column header as a fraction of the height of the column header.
    - alignment: A string indicating the horizontal alignment of the text in each column header, either "left", "center", or "right".
    - extend_column_separator: A boolean indicating whether the column separator lines should extend through the column headers.
    """

    alignment: str = "center"
    padding: float = 0.01
    text_kwargs: Dict[str, Any] = None
    extend_column_separator: bool = False

    def __post_init__(self):
        self.text_kwargs = self.text_kwargs or {}
        assert self.alignment in ["left", "center", "right"]
        assert 0 <= self.padding <= 1
