import pandas as pd
from matplotlib.axes import Axes
import numpy as np

from unittest.mock import MagicMock, call
import pytest
from table import Table
from options import TitleOptions


@pytest.fixture
def table_data():
    return pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], columns=["A", "B", "C"])


def test_setup_x_cell_boundaries():
    # Create a test DataFrame with 3 columns
    data = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6], "col3": [7, 8, 9]})
    ax_mock = MagicMock(spec=Axes)
    table = Table(data, ax_mock)

    # Call the _setup_x_cell_boundaries() function
    table._setup_x_cell_boundaries()

    # Check that the x_cell_boundaries attribute was set correctly
    expected_x_cell_boundaries = np.array([0.0, 0.33333333, 0.66666667, 1.0])
    np.testing.assert_allclose(table._x_cell_bondaries, expected_x_cell_boundaries)


def test_setup_y_cell_boundaries():
    # Define a sample DataFrame and ax object
    data = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
    ax = MagicMock(spec=Axes)
    table = Table(data, ax, show_column_names=False)

    # Call the _setup_y_cell_boundaries method
    table._setup_y_cell_boundaries()

    # Check that the y cell boundaries are set correctly
    expected_y_cell_bondaries = np.array([1.0, 0.66666667, 0.33333333, 0.0])
    np.testing.assert_allclose(table._y_cell_bondaries, expected_y_cell_bondaries)
    ax.set_xlim.assert_not_called()
    ax.set_ylim.assert_not_called()


def test_setup_x_cell_boundaries_with_column_names():
    # Define a sample DataFrame and ax object
    data = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
    ax = MagicMock(spec=Axes)
    table = Table(data, ax, show_column_names=True)

    # Call the _setup_x_cell_boundaries method
    table._setup_x_cell_boundaries()

    # Check that the x cell boundaries are set correctly
    expected_x_cell_bondaries = np.array([0.0, 0.33333333, 0.66666667, 1.0])
    np.testing.assert_allclose(table._x_cell_bondaries, expected_x_cell_bondaries)
    ax.set_xlim.assert_not_called()
    ax.set_ylim.assert_not_called()


def test_setup_y_cell_boundaries_with_column_names():
    # Define a sample DataFrame and ax object
    data = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
    ax = MagicMock(spec=Axes)
    table = Table(data, ax, show_column_names=True)

    # Call the _setup_y_cell_boundaries method
    table._setup_y_cell_boundaries()

    # Check that the y cell boundaries are set correctly
    expected_y_cell_bondaries = np.array([1.0, 0.75, 0.5, 0.25, 0.0])
    np.testing.assert_allclose(table._y_cell_bondaries, expected_y_cell_bondaries)
    ax.set_xlim.assert_not_called()
    ax.set_ylim.assert_not_called()


def test_setup_ax():
    # Create a mock Axes object
    ax = MagicMock(spec=Axes)

    # Create a Table object with show_column_names=True
    table = Table(data=pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}), ax=ax, show_column_names=True)

    # Call _setup_ax
    table._setup_ax()

    # Check that the xlim and ylim of ax were set correctly
    ax.set_xlim.assert_called_once_with(0, 1)
    ax.set_ylim.assert_called_once_with(0, 1)

    # Check that axis was turned off
    ax.axis.assert_called_once_with("off")


def test_draw_column_names():
    # Create a mock Axes object
    ax = MagicMock(spec=Axes)

    # Create a Table object with show_column_names=True
    table = Table(data=pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}), ax=ax, show_column_names=True)

    # Call _draw_column_names
    table._draw_column_names()

    # Check that the text method of ax was called twice with the expected arguments
    ax.text.assert_any_call(0.25, 0.875, "A", ha="center", va="center", **table._col_headers_text_kwargs)
    ax.text.assert_any_call(0.75, 0.875, "B", ha="center", va="center", **table._col_headers_text_kwargs)

    # Check that ax.text was called exactly twice
    assert ax.text.call_count == 2


def test_draw_the_cell_text(table_data):
    mock_ax = MagicMock(spec=Axes)

    # Create the table
    table = Table(table_data, mock_ax, show_column_names=True)

    # Call the function to be tested
    table._draw_the_cell_text(0, 0, 1)

    # Check if the expected method was called on the mocked object
    mock_ax.text.assert_called_once_with(
        0.16666666666666666, 0.875, 1, ha="center", va="center", **table._cell_text_kwargs
    )


def test_draw_cell_texts():
    # Create a dummy table
    data = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
    ax_mock = MagicMock()
    table = Table(data, ax_mock, show_column_names=True)

    # Mock the _draw_the_cell_text method
    table._draw_the_cell_text = MagicMock()

    # Call the _draw_cell_texts method
    table._draw_cell_texts()

    # Assert that _draw_the_cell_text was called with the correct arguments
    expected_calls = [
        call(1, 0, 1),
        call(1, 1, 4),
        call(1, 2, 7),
        call(2, 0, 2),
        call(2, 1, 5),
        call(2, 2, 8),
        call(3, 0, 3),
        call(3, 1, 6),
        call(3, 2, 9),
    ]
    table._draw_the_cell_text.assert_has_calls(expected_calls)


def test_draw():
    mock_ax = MagicMock(spec=Axes)
    data = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    table = Table(data, mock_ax, show_column_names=True)
    table._draw_column_names = MagicMock()
    table._draw_cell_texts = MagicMock()

    table.draw()

    mock_ax.set_xlim.assert_called_once_with(0, 1)
    mock_ax.set_ylim.assert_called_once_with(0, 1)
    mock_ax.axis.assert_called_once_with("off")
    assert table._draw_column_names.call_count == 1
    assert table._draw_cell_texts.call_count == 1


def test_constructor():
    axes_mock = MagicMock(spec=Axes)
    data = pd.DataFrame(np.random.rand(3, 3), columns=["A", "B", "C"])

    show_column_names = True
    col_headers_text_kwargs = {"fontsize": 12}
    cell_text_kwargs = {"fontsize": 10}
    table_title = "My Table"
    title_options = {"location": "top", "height": 0.1, "alignment": "center", "padding": 0.01}

    table = Table(
        data=data,
        ax=axes_mock,
        show_column_names=show_column_names,
        col_headers_text_kwargs=col_headers_text_kwargs,
        cell_text_kwargs=cell_text_kwargs,
        table_title=table_title,
        title_options=title_options,
    )

    assert isinstance(table, Table)
    assert table._data.equals(data)
    assert table._ax == axes_mock
    assert table._show_column_names == show_column_names
    assert table._col_headers_text_kwargs == col_headers_text_kwargs
    assert table._cell_text_kwargs == cell_text_kwargs
    assert table._table_title == table_title
    assert table._title_options.location == "top"
    assert table._title_options.height == 0.1
    assert table._title_options.alignment == "center"
    assert table._title_options.padding == 0.01


@pytest.fixture
def title_mock_table():
    data = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    ax = MagicMock()
    return Table(data=data, ax=ax)


def test_setup_table_boundaries_with_top_location_and_table_title(title_mock_table):
    title_mock_table._table_title = "Title"
    title_mock_table._title_options = TitleOptions(location="top", height=0.1)
    title_mock_table._setup_table_boundaries()
    assert np.array_equal(title_mock_table._table_title_boundaries, np.array([0.9, 1]))
    assert np.array_equal(title_mock_table._table_boundaries, np.array([0, 0.9]))


def test_setup_table_boundaries_with_bottom_location_and_table_title(title_mock_table):
    title_mock_table._table_title = "Title"
    title_mock_table._title_options = TitleOptions(location="bottom", height=0.1)
    title_mock_table._setup_table_boundaries()
    assert np.array_equal(title_mock_table._table_title_boundaries, np.array([0, 0.1]))
    assert np.array_equal(title_mock_table._table_boundaries, np.array([0.1, 1]))


def test_setup_table_boundaries_with_no_title(title_mock_table):
    title_mock_table._table_title = None
    title_mock_table._setup_table_boundaries()
    assert np.array_equal(title_mock_table._table_title_boundaries, np.array([0, 0]))
    assert np.array_equal(title_mock_table._table_boundaries, np.array([0, 1]))


def test_setup_table_boundaries_with_no_title_and_bottom_location(title_mock_table):
    title_mock_table._table_title = None
    title_mock_table._title_options = TitleOptions(location="bottom", height=0.1)
    title_mock_table._setup_table_boundaries()
    assert np.array_equal(title_mock_table._table_title_boundaries, np.array([0, 0]))
    assert np.array_equal(title_mock_table._table_boundaries, np.array([0, 1]))


def test_get_title_x_loc_center():
    ax_mock = MagicMock()
    title_options = {}
    data = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    table = Table(data=data, ax=ax_mock, title_options=title_options)
    x = table._get_title_x_loc()
    assert x == 0.5


def test_get_title_x_loc_left():
    ax_mock = MagicMock()
    title_options = dict(alignment="left", padding=0.1)
    data = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    table = Table(data=data, ax=ax_mock, title_options=title_options)
    x = table._get_title_x_loc()
    assert x == 0.1


def test_get_title_x_loc_right():
    ax_mock = MagicMock()
    title_options = dict(alignment="right", padding=0.2)
    data = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    table = Table(data=data, ax=ax_mock, title_options=title_options)
    x = table._get_title_x_loc()
    assert x == 0.8
