# mpltable

`mpltable` is a Python library that makes it easy to create and customize tables using matplotlib. It provides a simple `Table` class that can be used to draw tables on a given `Axes` object. This library offers various customization options such as column width, cell and header styles, title, separators, and border options.

## Installation

To install mpltable, run the following command:

```
pip install mpltable
```

## Usage

Below is a quick example of using mpltable to create a simple table.

```python
import pandas as pd
import matplotlib.pyplot as plt
from mpltable import Table

# Sample data
data = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
})

# Create a table with the data
fig, ax = plt.subplots()
table = Table(data, ax)
table.draw()

plt.show()
```

## Features

The `Table` class in mpltable provides several features for customizing your table:

- `show_column_names`: Display or hide column names in the table (default: `True`).
- `col_widths`: Set the column widths (default: equal width for all columns).
- `col_header_options`: Customize the appearance of the column headers.
- `cell_options`: Customize the appearance of the table cells.
- `table_title`: Set the table title (default: `None`).
- `title_options`: Customize the appearance and position of the table title.
- `background_color`: Set the background color of the table (default: `None`).
- `header_separator_kwargs`: Customize the separator line between header and data rows.
- `column_separator_kwargs`: Customize the separator lines between columns.
- `row_separator_kwargs`: Customize the separator lines between rows.
- `border_options`: Customize the appearance of the table borders.

### col_header_options
You can pass in a dictionary with the following settings
- `text_kwargs`: A dictionary of keyword arguments to pass to the text rendering function for the column headers.
- `padding`: A float between 0 and 1 indicating the amount of padding to add around the text in each column header as a fraction of the height of the column header.
- `alignment`: A string indicating the horizontal alignment of the text in each column header, either "left", "center", or "right".
- `extend_column_separator`: A boolean indicating whether the column separator lines should extend through the column headers.

### cell_options
You can pass in a dictionary with the following settings
- `text_kwargs`: A dictionary of keyword arguments to pass to the text rendering function for the cells.
- `padding`: A float between 0 and 1 indicating the amount of padding to add around the text in each cell as a fraction of the height of the cell.
- `alignment`: A string indicating the horizontal alignment of the text in each cell, either "left", "center", or "right".

### title_options
You can pass in a dictionary with the following settings
- `text_kwargs`: A dictionary of keyword arguments to pass to the text rendering function for the table title.
- `padding`: A float between 0 and 1 indicating the amount of padding to add around the text in the table title as a fraction of the height of the table title.
- `alignment`: A string indicating the horizontal alignment of the text in the table title, either "left", "center", or "right".
- `position`: A string indicating the position of the table title, either "top" or "bottom".
- `height`: A float between 0 and 1 indicating the height of the table title as a fraction of the height of the table.
- `separator_kwargs`: A dictionary of keyword arguments to pass to the line rendering function for the separator line between the table title and the table.

### border_options
You can pass in a dictionary with the following settings
- `bottom`: a dictionary of keyword arguments to pass to the line rendering function for the bottom border of the table.
- `top`: a dictionary of keyword arguments to pass to the line rendering function for the top border of the table.
- `left`: a dictionary of keyword arguments to pass to the line rendering function for the left border of the table.
- `right`: a dictionary of keyword arguments to pass to the line rendering function for the right border of the table.


Once the `Table` object has been instantiated, all these are converted into dataclasses and can be modified directly 
before calling the `draw` method. For example, to change the column widths, you can do the following:

```python
table.col_widths = [0.2, 0.3, 0.5]
table.draw()
```

For more examples and detailed usage instructions, please refer to the [documentation](https://github.com/yourusername/mpltable/blob/main/docs/README.md).

## License

mpltable is released under the [MIT License](https://github.com/yourusername/mpltable/blob/main/LICENSE).