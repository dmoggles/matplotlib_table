import pytest
import pandas as pd
import numpy as np

from unittest.mock import Mock, patch, MagicMock, call
from mpltable.table import Table
from dataclasses import asdict
from matplotlib.axes import Axes


class TestTableValidateColWidth:
    @pytest.fixture
    def table_data(self):
        return pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]})

    def test__validate_col_widths_with_valid_widths(self, table_data):
        # Given
        ax_mock = MagicMock(spec=Axes)
        table = Table(table_data, ax_mock)
        table.col_widths = {"a": 0.2, "b": 0.3, "c": 0.5}

        # When
        table._validate_col_widths()

        # Then
        assert True  # No assertion needed, if there are no assertions it's considered a passing test

    def test__validate_col_widths_with_invalid_type(self, table_data):
        # Given
        ax_mock = MagicMock(spec=Axes)
        table = Table(table_data, ax_mock)
        table.col_widths = ["a", "b", "c"]

        # When / Then
        with pytest.raises(AssertionError):
            table._validate_col_widths()

    def test__validate_col_widths_with_invalid_key_type(self, table_data):
        # Given
        ax_mock = MagicMock(spec=Axes)
        table = Table(table_data, ax_mock)
        table.col_widths = {1: 0.2, 2: 0.3, 3: 0.5}

        # When / Then
        with pytest.raises(AssertionError):
            table._validate_col_widths()

    def test__validate_col_widths_with_invalid_value_type(self, table_data):
        # Given
        ax_mock = MagicMock(spec=Axes)
        table = Table(table_data, ax_mock)
        table.col_widths = {"a": "foo", "b": 0.3, "c": 0.5}

        # When / Then
        with pytest.raises(AssertionError):
            table._validate_col_widths()

    def test__validate_col_widths_with_invalid_value_range(self, table_data):
        # Given
        ax_mock = MagicMock(spec=Axes)
        table = Table(table_data, ax_mock)
        table.col_widths = {"a": 0.2, "b": 1.3, "c": 0.5}

        # When / Then
        with pytest.raises(AssertionError):
            table._validate_col_widths()

    def test__validate_col_widths_with_invalid_value_sum(self, table_data):
        # Given
        ax_mock = MagicMock(spec=Axes)
        table = Table(table_data, ax_mock)
        table.col_widths = {"a": 0.2, "b": 0.3, "c": 0.6}

        # When / Then
        with pytest.raises(AssertionError):
            table._validate_col_widths()

    @patch("mpltable.table.Table._validate_col_widths")
    def test_table_creation_calls__validate_col_widths(self, mock__validate_col_widths, table_data):
        # Given
        ax_mock = MagicMock(spec=Axes)

        # When
        table = Table(table_data, ax_mock)

        # Then
        mock__validate_col_widths.assert_called_once()


class TestTableBoundariesFromUserProvidedColWidths:
    @pytest.fixture
    def table_data(self):
        return pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]})

    def test__boundaries_from_user_provided_col_widths(self, table_data):
        # Given
        ax_mock = MagicMock(spec=Axes)
        table = Table(table_data, ax_mock)
        table.col_widths = {"a": 0.2, "b": 0.3, "c": 0.5}

        # When
        boundaries = table._boundaries_from_user_provided_col_widths()

        # Then
        assert boundaries == [0, 0.2, 0.5, 1.0]


class TestTableSetupXCellBoundaries:
    @pytest.fixture
    def table(self):
        data = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]})
        ax = Mock(spec=Axes)
        return Table(data, ax)

    def test_setup_x_cell_boundaries_with_col_widths(self, table):
        table.col_widths = {"a": 0.2, "b": 0.5, "c": 0.3}
        table._setup_x_cell_boundaries()
        expected = np.array([0.0, 0.2, 0.7, 1.0])
        assert np.allclose(table._x_cell_bondaries, expected)

    def test_setup_x_cell_boundaries_without_col_widths(self, table):
        table._setup_x_cell_boundaries()
        expected = np.array([0.0, 1 / 3, 2 / 3, 1.0])
        assert np.allclose(table._x_cell_bondaries, expected)

    def test_setup_x_cell_boundaries_with_one_column(self, table):
        ax = Mock(spec=Axes)
        table = Table(pd.DataFrame({"a": [1, 2, 3]}), ax)
        table._setup_x_cell_boundaries()
        expected = np.array([0.0, 1.0])
        assert np.allclose(table._x_cell_bondaries, expected)

    def test_setup_x_cell_boundaries_with_empty_data(self, table):
        ax = Mock(spec=Axes)
        table = Table(pd.DataFrame(), ax)
        with pytest.raises(ValueError):
            table._setup_x_cell_boundaries()


class TestTableSetupTableBoundaries:
    @pytest.fixture
    def table(self):
        # create a mock Table object
        table = Table(
            MagicMock(spec=pd.DataFrame), MagicMock(spec=Axes)
        )  # set up some default values for the Table object
        table._title_options = Mock()
        table._title_options.location = None
        table._title_options.height = 0.0
        table._table_title = None
        return table

    def test_setup_table_boundaries_top_title(self, table):
        # set up the mock Table object with a top title
        table._title_options.location = "top"
        table._title_options.height = 0.2
        table._table_title = "Table Title"
        # run the function to be tested
        table._setup_table_boundaries()
        # check the results
        assert np.allclose(table._table_title_boundaries, np.array([0.8, 1.0]))
        assert np.allclose(table._table_boundaries, np.array([0.0, 0.8]))

    def test_setup_table_boundaries_bottom_title(self, table):
        # set up the mock Table object with a bottom title
        table._title_options.location = "bottom"
        table._title_options.height = 0.2
        table._table_title = "Table Title"
        # run the function to be tested
        table._setup_table_boundaries()
        # check the results
        assert np.allclose(table._table_title_boundaries, np.array([0.0, 0.2]))
        assert np.allclose(table._table_boundaries, np.array([0.2, 1.0]))

    def test_setup_table_boundaries_no_title(self, table):
        # set up the mock Table object with no title
        # (the default values are already set in the fixture)
        # run the function to be tested
        table._setup_table_boundaries()
        # check the results
        assert np.allclose(table._table_title_boundaries, np.array([0.0, 0.0]))
        assert np.allclose(table._table_boundaries, np.array([0.0, 1.0]))


class TestTableSetupYCellBoundaries:
    @pytest.fixture
    def table(self):
        table = Table(
            MagicMock(spec=pd.DataFrame), MagicMock(spec=Axes)
        )  # set up some default values for the Table object
        table._show_column_names = True
        table._table_boundaries = np.array([0.1, 0.9])
        return table

    def test_setup_y_cell_boundaries_with_show_column_names(self, table):
        table.data.shape = (3, 2)
        table._show_column_names = True
        table._table_boundaries = np.array([0.1, 0.9])

        table._setup_y_cell_boundaries()

        expected_y_cell_boundaries = np.array([0.9, 0.7, 0.5, 0.3, 0.1])
        assert np.allclose(table._y_cell_bondaries, expected_y_cell_boundaries)

    def test_setup_y_cell_boundaries_without_show_column_names(self, table):
        table._data.shape = (4, 2)
        table._show_column_names = False
        table._table_boundaries = np.array([0.1, 0.9])
        table._setup_y_cell_boundaries()

        expected_y_cell_boundaries = np.array([0.9, 0.7, 0.5, 0.3, 0.1])
        assert np.allclose(table._y_cell_bondaries, expected_y_cell_boundaries)


class TestTableCreateDimensions:
    @patch("mpltable.table.Table._setup_table_boundaries")
    @patch("mpltable.table.Table._setup_x_cell_boundaries")
    @patch("mpltable.table.Table._setup_y_cell_boundaries")
    def test_calls_all_setup_methods(self, mock_setup_y, mock_setup_x, mock_setup_table):
        table = Table(MagicMock(spec=pd.DataFrame), MagicMock(spec=Axes))
        table._create_dimensions()
        mock_setup_y.assert_called_once_with()
        mock_setup_x.assert_called_once_with()
        mock_setup_table.assert_called_once_with()


class TestTableSetupAx:
    def test_setup_ax_with_background_color(self):
        ax = MagicMock(
            spines=MagicMock(values=MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock(), MagicMock()]))
        )
        table = Table(MagicMock(spec=pd.DataFrame), ax)
        table._background_color = "white"
        table._setup_ax()

        ax.set_xlim.assert_called_once_with(0, 1)
        ax.set_ylim.assert_called_once_with(0, 1)
        for spine in ax.spines.values():
            spine.set_visible.assert_called_once_with(False)
        ax.set_xticks.assert_called_once_with([])
        ax.set_yticks.assert_called_once_with([])
        ax.set_facecolor.assert_called_once_with("white")

    def test_setup_ax_without_background_color(self):
        ax = MagicMock(spec=Axes)
        table = Table(MagicMock(spec=pd.DataFrame), ax)
        table._background_color = None
        table._setup_ax()

        ax.set_xlim.assert_called_once_with(0, 1)
        ax.set_ylim.assert_called_once_with(0, 1)
        ax.axis.assert_called_once_with("off")


class TestTableDrawColumnNear:
    def test_draws_column_names(self):
        # Define mock data and options for the Table
        data = MagicMock()
        data.columns = ["A", "B", "C"]
        ax = MagicMock(spec=Axes)
        table = Table(data, ax)
        table.col_header_options.padding = 0.05
        table.col_header_options.alignment = "center"
        table.col_header_options.text_kwargs = {"fontsize": 12}
        table._get_cell_x_coordinate = MagicMock(side_effect=[0.125, 0.375, 0.75])
        # Define mock x and y cell boundaries for the table
        table._x_cell_bondaries = np.array([0.0, 0.25, 0.5, 1.0])
        table._y_cell_bondaries = np.array([1, 0.5, 0.0])
        # Call the function to be tested
        table._draw_column_names()

        # Assert that the text method of the axis object is called three times with the expected arguments
        ax.text.assert_any_call(0.125, 0.75, "A", ha="center", va="center", fontsize=12)
        ax.text.assert_any_call(0.375, 0.75, "B", ha="center", va="center", fontsize=12)
        ax.text.assert_any_call(0.75, 0.75, "C", ha="center", va="center", fontsize=12)
        table._get_cell_x_coordinate.assert_has_calls(
            [
                call(0.0, 0.25, 0.05, "center"),
                call(0.25, 0.5, 0.05, "center"),
                call(0.5, 1.0, 0.05, "center"),
            ],
            any_order=False,
        )

    def test_uses_padding_and_alignment_options(self):
        # Define mock data and options for the Table
        data = MagicMock()
        data.columns = ["A", "B", "C"]
        ax = MagicMock(spec=Axes)
        table = Table(data, ax=ax)
        table.col_header_options.alignment = "left"
        table.col_header_options.padding = 0.1
        table.col_header_options.text_kwargs = {"fontsize": 12}
        table._get_cell_x_coordinate = MagicMock(side_effect=[0.075, 0.325, 0.725])

        # Define mock x and y cell boundaries for the table
        table._x_cell_bondaries = np.array([0.0, 0.25, 0.5, 1.0])
        table._y_cell_bondaries = np.array([1, 0.5, 0.0])

        # Define mock axis object and set it to the table

        # Call the function to be tested
        table._draw_column_names()

        # Assert that the text method of the axis object is called three times with the expected arguments
        ax.text.assert_any_call(0.075, 0.75, "A", ha="left", va="center", fontsize=12)
        ax.text.assert_any_call(0.325, 0.75, "B", ha="left", va="center", fontsize=12)
        ax.text.assert_any_call(0.725, 0.75, "C", ha="left", va="center", fontsize=12)

        table._get_cell_x_coordinate.assert_has_calls(
            [
                call(0.0, 0.25, 0.1, "left"),
                call(0.25, 0.5, 0.1, "left"),
                call(0.5, 1.0, 0.1, "left"),
            ],
            any_order=False,
        )


class TestTableGetCellXCoordinate:
    def test_left_alignment(self):
        left_boundary = 1.0
        right_boundary = 3.0
        padding = 0.1
        alignment = "left"
        expected_result = 1.1
        result = Table._get_cell_x_coordinate(left_boundary, right_boundary, padding, alignment)
        assert result == pytest.approx(expected_result)

    def test_right_alignment(self):
        left_boundary = 1.0
        right_boundary = 3.0
        padding = 0.1
        alignment = "right"
        expected_result = 2.9
        result = Table._get_cell_x_coordinate(left_boundary, right_boundary, padding, alignment)
        assert result == pytest.approx(expected_result)

    def test_center_alignment(self):
        left_boundary = 1.0
        right_boundary = 3.0
        padding = 0.1
        alignment = "center"
        expected_result = 2.0
        result = Table._get_cell_x_coordinate(left_boundary, right_boundary, padding, alignment)
        assert result == pytest.approx(expected_result)

    def test_invalid_alignment(self):
        left_boundary = 1.0
        right_boundary = 3.0
        padding = 0.1
        alignment = "invalid"
        with pytest.raises(
            AssertionError,
            match="alignment must be one of 'left', 'right', or 'center', got invalid",
        ):
            Table._get_cell_x_coordinate(left_boundary, right_boundary, padding, alignment)

    def test_negative_padding(self):
        left_boundary = 1.0
        right_boundary = 3.0
        padding = -0.1
        alignment = "left"
        with pytest.raises(AssertionError, match=f"padding must be between 0 and 1, got -0.1"):
            Table._get_cell_x_coordinate(left_boundary, right_boundary, padding, alignment)

    def test_padding_greater_than_one(self):
        left_boundary = 1.0
        right_boundary = 3.0
        padding = 1.1
        alignment = "left"
        with pytest.raises(AssertionError, match=f"padding must be between 0 and 1, got 1.1"):
            Table._get_cell_x_coordinate(left_boundary, right_boundary, padding, alignment)

    def test_left_boundary_greater_than_right_boundary(self):
        left_boundary = 3.0
        right_boundary = 1.0
        padding = 0.1
        alignment = "left"
        with pytest.raises(
            AssertionError,
            match=f"left_boundary must be less than right_boundary, got 3.0 and 1.0",
        ):
            Table._get_cell_x_coordinate(left_boundary, right_boundary, padding, alignment)


class TestTableDrawTheCellText:
    @pytest.fixture
    def mock_table(self):
        data = MagicMock(pd.DataFrame)
        ax = MagicMock(spec=Axes)
        table = Table(data, ax)

        table._x_cell_bondaries = [0.0, 1.0, 2.0]
        table._y_cell_bondaries = [0.0, 1.0, 2.0]
        table._cell_options = MagicMock()
        table._cell_options.padding = 0.1
        table._cell_options.alignment = "left"
        table._cell_options.text_kwargs = {"fontsize": 12}
        return table

    def test_draw_the_cell_text(self, mock_table):
        i = 1
        j = 1
        cell = "test"

        with patch.object(Table, "_get_cell_x_coordinate", return_value=1.1) as mock_get_cell_x_coordinate:
            mock_table._draw_the_cell_text(i, j, cell)

            # Verify that _get_cell_x_coordinate was called with the correct arguments
            mock_get_cell_x_coordinate.assert_called_once_with(1.0, 2.0, 0.1, "left")

            # Verify that ax.text was called with the correct arguments
            mock_table._ax.text.assert_called_once_with(1.1, 1.5, cell, ha="left", va="center", fontsize=12)


class TestTableDrawCellTexts:
    @pytest.fixture
    def mock_table(self):
        table = Table(None, None)
        table._data = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
        table._show_column_names = True
        return table

    def test_draw_cell_texts(self, mock_table):
        with patch.object(Table, "_draw_the_cell_text") as mock_draw_the_cell_text:
            mock_table._draw_cell_texts()

            # Verify that _draw_the_cell_text was called the correct number of times
            assert mock_draw_the_cell_text.call_count == 4

            # Verify that _draw_the_cell_text was called with the correct arguments
            calls = [
                ((1, 0, 1),),
                ((1, 1, 3),),
                ((2, 0, 2),),
                ((2, 1, 4),),
            ]
            mock_draw_the_cell_text.assert_has_calls(calls, any_order=True)


class TestTableGetTitleXLoc:
    @pytest.fixture
    def mock_table(self):
        table = Table(None, None)
        table._title_options = MagicMock()
        return table

    def test_left_alignment(self, mock_table):
        mock_table._title_options.alignment = "left"
        mock_table._title_options.padding = 0.1
        expected_result = 0.1
        result = mock_table._get_title_x_loc()
        assert result == pytest.approx(expected_result)

    def test_right_alignment(self, mock_table):
        mock_table._title_options.alignment = "right"
        mock_table._title_options.padding = 0.1
        expected_result = 0.9
        result = mock_table._get_title_x_loc()
        assert result == pytest.approx(expected_result)

    def test_center_alignment(self, mock_table):
        mock_table._title_options.alignment = "center"
        expected_result = 0.5
        result = mock_table._get_title_x_loc()
        assert result == pytest.approx(expected_result)


class TestTableDrawTableTitle:
    @pytest.fixture
    def mock_table(self):
        table = Table(None, None)
        table._ax = MagicMock()
        table._table_title = "Test Title"
        table._table_title_boundaries = [0.0, 1.0]
        table._title_options = MagicMock()
        table._title_options.alignment = "left"
        table._title_options.padding = 0.1
        table._title_options.text_kwargs = {}
        return table

    def test_draw_table_title(self, mock_table):
        with patch.object(Table, "_get_title_x_loc", return_value=0.1) as mock_get_title_x_loc:
            mock_table._draw_table_title()

            # Verify that _get_title_x_loc was called once
            mock_get_title_x_loc.assert_called_once()

            # Verify that ax.text was called with the correct arguments
            mock_table._ax.text.assert_called_once_with(0.1, 0.5, "Test Title", ha="left", va="center", **{})


class TestTableDrawTitleSeparatorLine:
    @pytest.fixture
    def mock_table(self):
        table = Table(None, None)
        table._ax = MagicMock()
        table._table_title_boundaries = [0.0, 1.0]
        table._title_options = MagicMock()
        table._title_options.separator_kwargs = {"color": "red"}
        return table

    def test_draw_title_separator_line(self, mock_table):
        mock_table._draw_title_separator_line()

        # Verify that ax.hlines was called with the correct arguments
        mock_table._ax.hlines.assert_called_once_with(0.0, 0, 1, color="red")


class TestTableDrawHeaderSeparatorLine:
    @pytest.fixture
    def mock_table(self):
        table = Table(None, None)
        table._ax = MagicMock()
        table._y_cell_bondaries = [0.0, 1.0, 2.0]
        table._header_separator_kwargs = {}
        return table

    def test_draw_header_separator_line(self, mock_table):
        mock_table._draw_header_separator_line()

        # Verify that ax.hlines was called with the correct arguments
        mock_table._ax.hlines.assert_called_once_with(1.0, 0, 1, **{})


class TestTableDrawColumnSeparatorLines:
    @pytest.fixture
    def mock_table(self):
        table = Table(None, None)
        table._ax = MagicMock()
        table._x_cell_bondaries = [0.0, 1.0, 2.0]
        table._y_cell_bondaries = [0.0, 1.0, 2.0]
        table._table_boundaries = [0.0, 1.0]
        table._column_separator_kwargs = {"color": "red"}
        return table

    def test_draw_column_separator_lines_show_column_names(self, mock_table):
        mock_table.show_column_names = True
        mock_table._col_header_options = MagicMock()
        mock_table._col_header_options.extend_column_separator = False
        mock_table._draw_column_separator_lines()

        # Verify that ax.vlines was called with the correct arguments
        mock_table._ax.vlines.assert_called_once_with(1.0, 1.0, 0.0, color="red")

    def test_draw_column_separator_lines_no_show_column_names(self, mock_table):
        mock_table.show_column_names = False
        mock_table._col_header_options = MagicMock()
        mock_table._col_header_options.extend_column_separator = False
        mock_table._draw_column_separator_lines()

        # Verify that ax.vlines was called with the correct arguments
        mock_table._ax.vlines.assert_called_once_with(1.0, 0.0, 0.0, color="red")

    def test_draw_column_separator_lines_extend_column_separator(self, mock_table):
        mock_table.show_column_names = True
        mock_table._col_header_options = MagicMock()
        mock_table._col_header_options.extend_column_separator = True
        mock_table._draw_column_separator_lines()

        # Verify that ax.vlines was called with the correct arguments
        mock_table._ax.vlines.assert_called_once_with(1.0, 0.0, 0.0, color="red")


class TestTableDrawRowSeparatorLines:
    @pytest.fixture
    def mock_table(self):
        table = Table(None, None)
        table._ax = MagicMock()
        table._y_cell_bondaries = [0.0, 1.0, 2.0, 3.0]
        table._row_separator_kwargs = {"color": "red"}
        return table

    def test_draw_row_separator_lines_show_column_names(self, mock_table):
        mock_table._show_column_names = True
        mock_table._draw_row_separator_lines()

        # Verify that ax.hlines was called with the correct arguments
        mock_table._ax.hlines.assert_called_once_with([2.0], 0, 1, color="red")

    def test_draw_row_separator_lines_no_show_column_names(self, mock_table):
        mock_table._show_column_names = False
        mock_table._draw_row_separator_lines()

        # Verify that ax.hlines was called with the correct arguments
        mock_table._ax.hlines.assert_called_once_with([1.0, 2.0], 0, 1, color="red")


class TestTableDrawSeparatorLines:
    @pytest.fixture
    def mock_table(self):
        table = Table(None, None)
        table._table_title = "Test Title"
        table._show_column_names = True
        table._title_options = MagicMock()
        table._title_options.separator_kwargs = {"color": "red"}
        table._header_separator_kwargs = {"color": "red"}
        table._column_separator_kwargs = {"color": "red"}
        table._row_separator_kwargs = {"color": "red"}
        return table

    def test_draw_separator_lines(self, mock_table):
        with patch.object(Table, "_draw_title_separator_line") as mock_draw_title_separator_line, patch.object(
            Table, "_draw_header_separator_line"
        ) as mock_draw_header_separator_line, patch.object(
            Table, "_draw_column_separator_lines"
        ) as mock_draw_column_separator_lines, patch.object(
            Table, "_draw_row_separator_lines"
        ) as mock_draw_row_separator_lines:
            mock_table._draw_separator_lines()

            # Verify that the corresponding methods were called
            mock_draw_title_separator_line.assert_called_once()
            mock_draw_header_separator_line.assert_called_once()
            mock_draw_column_separator_lines.assert_called_once()
            mock_draw_row_separator_lines.assert_called_once()

    def test_draw_separator_lines_no_title(self, mock_table):
        mock_table._table_title = None
        with patch.object(Table, "_draw_title_separator_line") as mock_draw_title_separator_line, patch.object(
            Table, "_draw_header_separator_line"
        ) as mock_draw_header_separator_line, patch.object(
            Table, "_draw_column_separator_lines"
        ) as mock_draw_column_separator_lines, patch.object(
            Table, "_draw_row_separator_lines"
        ) as mock_draw_row_separator_lines:
            mock_table._draw_separator_lines()

            # Verify that the corresponding methods were called
            mock_draw_title_separator_line.assert_not_called()
            mock_draw_header_separator_line.assert_called_once()
            mock_draw_column_separator_lines.assert_called_once()
            mock_draw_row_separator_lines.assert_called_once()

    def test_draw_separator_lines_no_title_kwargs(self, mock_table):
        mock_table._title_options.separator_kwargs = None
        with patch.object(Table, "_draw_title_separator_line") as mock_draw_title_separator_line, patch.object(
            Table, "_draw_header_separator_line"
        ) as mock_draw_header_separator_line, patch.object(
            Table, "_draw_column_separator_lines"
        ) as mock_draw_column_separator_lines, patch.object(
            Table, "_draw_row_separator_lines"
        ) as mock_draw_row_separator_lines:
            mock_table._draw_separator_lines()

            # Verify that the corresponding methods were called
            mock_draw_title_separator_line.assert_not_called()
            mock_draw_header_separator_line.assert_called_once()
            mock_draw_column_separator_lines.assert_called_once()
            mock_draw_row_separator_lines.assert_called_once()

    def test_draw_separator_lines_no_column_names(self, mock_table):
        mock_table._show_column_names = False
        with patch.object(Table, "_draw_title_separator_line") as mock_draw_title_separator_line, patch.object(
            Table, "_draw_header_separator_line"
        ) as mock_draw_header_separator_line, patch.object(
            Table, "_draw_column_separator_lines"
        ) as mock_draw_column_separator_lines, patch.object(
            Table, "_draw_row_separator_lines"
        ) as mock_draw_row_separator_lines:
            mock_table._draw_separator_lines()

            # Verify that the corresponding methods were called
            mock_draw_title_separator_line.assert_called_once()
            mock_draw_header_separator_line.assert_not_called()
            mock_draw_column_separator_lines.assert_called_once()
            mock_draw_row_separator_lines.assert_called_once()

    def test_draw_separator_lines_no_header_kwargs(self, mock_table):
        mock_table._header_separator_kwargs = None
        with patch.object(Table, "_draw_title_separator_line") as mock_draw_title_separator_line, patch.object(
            Table, "_draw_header_separator_line"
        ) as mock_draw_header_separator_line, patch.object(
            Table, "_draw_column_separator_lines"
        ) as mock_draw_column_separator_lines, patch.object(
            Table, "_draw_row_separator_lines"
        ) as mock_draw_row_separator_lines:
            mock_table._draw_separator_lines()

            # Verify that the corresponding methods were called
            mock_draw_title_separator_line.assert_called_once()
            mock_draw_header_separator_line.assert_not_called()
            mock_draw_column_separator_lines.assert_called_once()
            mock_draw_row_separator_lines.assert_called_once()

    def test_draw_separator_lines_no_column_separator_kwargs(self, mock_table):
        mock_table._column_separator_kwargs = None
        with patch.object(Table, "_draw_title_separator_line") as mock_draw_title_separator_line, patch.object(
            Table, "_draw_header_separator_line"
        ) as mock_draw_header_separator_line, patch.object(
            Table, "_draw_column_separator_lines"
        ) as mock_draw_column_separator_lines, patch.object(
            Table, "_draw_row_separator_lines"
        ) as mock_draw_row_separator_lines:
            mock_table._draw_separator_lines()

            # Verify that the corresponding methods were called
            mock_draw_title_separator_line.assert_called_once()
            mock_draw_header_separator_line.assert_called_once()
            mock_draw_column_separator_lines.assert_not_called()
            mock_draw_row_separator_lines.assert_called_once()

    def test_draw_separator_lines_no_row_separator_kwargs(self, mock_table):
        mock_table._row_separator_kwargs = None
        with patch.object(Table, "_draw_title_separator_line") as mock_draw_title_separator_line, patch.object(
            Table, "_draw_header_separator_line"
        ) as mock_draw_header_separator_line, patch.object(
            Table, "_draw_column_separator_lines"
        ) as mock_draw_column_separator_lines, patch.object(
            Table, "_draw_row_separator_lines"
        ) as mock_draw_row_separator_lines:
            mock_table._draw_separator_lines()

            # Verify that the corresponding methods were called
            mock_draw_title_separator_line.assert_called_once()
            mock_draw_header_separator_line.assert_called_once()
            mock_draw_column_separator_lines.assert_called_once()
            mock_draw_row_separator_lines.assert_not_called()


class TestTableDrawBorders:
    @pytest.fixture
    def mock_table(self):
        table = Table(None, None)
        table._ax = MagicMock()
        table._table_boundaries = [0.0, 1.0]
        table._border_options = MagicMock()
        table._border_options.bottom = {"color": "red"}
        table._border_options.top = {"color": "blue"}
        table._border_options.left = {"color": "green"}
        table._border_options.right = {"color": "yellow"}
        return table

    def test_draw_bottom_border(self, mock_table):
        mock_table._draw_bottom_border()

        # Verify that ax.hlines was called with the correct arguments
        mock_table._ax.hlines.assert_called_once_with(0.0, 0, 1, color="red")

    def test_draw_top_border(self, mock_table):
        mock_table._draw_top_border()

        # Verify that ax.hlines was called with the correct arguments
        mock_table._ax.hlines.assert_called_once_with(1.0, 0, 1, color="blue")

    def test_draw_left_border(self, mock_table):
        mock_table._draw_left_border()

        # Verify that ax.vlines was called with the correct arguments
        mock_table._ax.vlines.assert_called_once_with(0.0, 0, 1, color="green")

    def test_draw_right_border(self, mock_table):
        mock_table._draw_right_border()

        # Verify that ax.vlines was called with the correct arguments
        mock_table._ax.vlines.assert_called_once_with(1.0, 0, 1, color="yellow")

    def test_draw_borders(self, mock_table):
        with patch.object(Table, "_draw_bottom_border") as mock_draw_bottom_border, patch.object(
            Table, "_draw_top_border"
        ) as mock_draw_top_border, patch.object(Table, "_draw_left_border") as mock_draw_left_border, patch.object(
            Table, "_draw_right_border"
        ) as mock_draw_right_border:
            mock_table._draw_borders()

            # Verify that the corresponding methods were called
            mock_draw_bottom_border.assert_called_once()
            mock_draw_top_border.assert_called_once()
            mock_draw_left_border.assert_called_once()
            mock_draw_right_border.assert_called_once()


class TestTableDraw:
    @pytest.fixture
    def mock_table(self):
        table = Table(None, None)
        table._table_title = "Test Title"
        table._show_column_names = True
        table._ax = MagicMock()
        return table

    def test_draw(self, mock_table):
        with patch.object(Table, "_create_dimensions") as mock_create_dimensions, patch.object(
            Table, "_setup_ax"
        ) as mock_setup_ax, patch.object(Table, "_draw_table_title") as mock_draw_table_title, patch.object(
            Table, "_draw_column_names"
        ) as mock_draw_column_names, patch.object(
            Table, "_draw_separator_lines"
        ) as mock_draw_separator_lines, patch.object(
            Table, "_draw_borders"
        ) as mock_draw_borders, patch.object(
            Table, "_draw_cell_texts"
        ) as mock_draw_cell_texts:
            mock_table.draw()

            # Verify that the corresponding methods were called
            mock_create_dimensions.assert_called_once()
            mock_setup_ax.assert_called_once()
            mock_draw_table_title.assert_called_once()
            mock_draw_column_names.assert_called_once()
            mock_draw_separator_lines.assert_called_once()
            mock_draw_borders.assert_called_once()
            mock_draw_cell_texts.assert_called_once()

    def test_draw_no_table_title(self, mock_table):
        mock_table._table_title = None
        with patch.object(Table, "_create_dimensions") as mock_create_dimensions, patch.object(
            Table, "_setup_ax"
        ) as mock_setup_ax, patch.object(Table, "_draw_table_title") as mock_draw_table_title, patch.object(
            Table, "_draw_column_names"
        ) as mock_draw_column_names, patch.object(
            Table, "_draw_separator_lines"
        ) as mock_draw_separator_lines, patch.object(
            Table, "_draw_borders"
        ) as mock_draw_borders, patch.object(
            Table, "_draw_cell_texts"
        ) as mock_draw_cell_texts:
            mock_table.draw()

            # Verify that the corresponding methods were called
            mock_create_dimensions.assert_called_once()
            mock_setup_ax.assert_called_once()
            mock_draw_table_title.assert_not_called()
            mock_draw_column_names.assert_called_once()
            mock_draw_separator_lines.assert_called_once()
            mock_draw_borders.assert_called_once()
            mock_draw_cell_texts.assert_called_once()

    def test_draw_no_column_names(self, mock_table):
        mock_table._show_column_names = False
        with patch.object(Table, "_create_dimensions") as mock_create_dimensions, patch.object(
            Table, "_setup_ax"
        ) as mock_setup_ax, patch.object(Table, "_draw_table_title") as mock_draw_table_title, patch.object(
            Table, "_draw_column_names"
        ) as mock_draw_column_names, patch.object(
            Table, "_draw_separator_lines"
        ) as mock_draw_separator_lines, patch.object(
            Table, "_draw_borders"
        ) as mock_draw_borders, patch.object(
            Table, "_draw_cell_texts"
        ) as mock_draw_cell_texts:
            mock_table.draw()

            # Verify that the corresponding methods were called
            mock_create_dimensions.assert_called_once()
            mock_setup_ax.assert_called_once()
            mock_draw_table_title.assert_called_once()
            mock_draw_column_names.assert_not_called()
            mock_draw_separator_lines.assert_called_once()
            mock_draw_borders.assert_called_once()
            mock_draw_cell_texts.assert_called_once()
