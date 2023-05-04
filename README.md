# Table Class

The `Table` class is used to draw a table on a provided Matplotlib `Axes` object. It takes in a Pandas `DataFrame` and some additional options such as whether to show column names, text formatting options for column headers and cells, and a table title.

## Constructor

To create a new `Table` object, call the constructor with the following parameters:

```python
Table(data: pd.DataFrame,
      ax: Axes,
      show_column_names: bool = True,
      col_headers_text_kwargs: Dict[str, Any] = None,
      cell_text_kwargs: Dict[str, Any] = None,
      table_title: str = None,
      title_options: Dict[str, Any] = None)
```

### Parameters

- `data`: a Pandas `DataFrame` containing the data to be displayed in the table.
- `ax`: a Matplotlib `Axes` object on which to draw the table.
- `show_column_names`: a boolean value indicating whether to display the column names as the first row of the table. Defaults to `True`.
- `col_headers_text_kwargs`: a dictionary of keyword arguments to be passed to `matplotlib.pyplot.text` for formatting the column headers. Defaults to an empty dictionary.
- `cell_text_kwargs`: a dictionary of keyword arguments to be passed to `matplotlib.pyplot.text` for formatting the cell text. Defaults to an empty dictionary.
- `table_title`: a string containing the title of the table. Defaults to `None`.
- `title_options`: a dictionary of options for the table title. Acceptable options are:
    - `text_kwargs`: A dictionary of keyword arguments to pass to the text rendering function for the title. The keys and values of this dictionary will depend on the specific text rendering function being used.
    - `location`: A string indicating the location of the title, either "top" or "bottom".
    - `height`: A float between 0 and 1 indicating the height of the title as a fraction of the total height of the table. Acceptable values for this key are floats between 0 and 1, inclusive.
    - `alignment`: A string indicating the horizontal alignment of the title, either "left", "center", or "right".
    - `padding`: A float between 0 and 1 indicating the amount of padding to add around the title as a fraction of its height. Acceptable values for this key are floats between 0 and 1, inclusive.
## Public Methods

### `draw()`

Draws the table on the provided `Axes` object. Call this method after instantiating the `Table` object and setting any desired options.

## Example Usage

```python
import pandas as pd
import matplotlib.pyplot as plt
from table import Table

# Create a Pandas DataFrame with some data
data = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
})

# Create a new Matplotlib figure and axis
fig, ax = plt.subplots()

# Create a new Table object and set some options
table = Table(
    data=data,
    ax=ax,
    show_column_names=True,
    table_title='My Table'
)

# Draw the table
table.draw()

# Show the plot
plt.show()
```