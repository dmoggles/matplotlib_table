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

    Methods:
    - __post_init__(self): A special method that is called after the class is initialized to check that the specified options are valid.
      Raises an AssertionError if any of the options are invalid.
    """

    text_kwargs: Dict[str, Any] = None
    location: str = "top"
    height: float = 0.1
    alignment: str = "center"
    padding: float = 0.01

    def __post_init__(self):
        self.text_kwargs = self.text_kwargs or {}
        assert self.location in ["top", "bottom"]
        assert self.alignment in ["left", "center", "right"]
        assert 0 <= self.height <= 1
        assert 0 <= self.padding <= 1
        assert self.height + self.padding <= 1
