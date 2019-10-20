import pandas as pd
import ipywidgets as widgets
from IPython.display import display as displ
from datadict import DataDict


def _display_df(self, df_output: pd.DataFrame):
    out_df = widgets.Output()
    with out_df:
        displ(self.format(df_output))

    return out_df


def _display_dd(self, df_output: pd.DataFrame):
    data_dict = self._data_dict[['Name', 'Description']]
    data_dict = data_dict[data_dict['Name'].isin(df_output.columns)]
    dd_out = widgets.Output()
    with dd_out:
        styles = [
            dict(selector="th", props=[("text-align", "left")]),
            dict(selector="td", props=[("text-align", "left")]),
        ]
        displ(data_dict.style.format(self._formats).hide_index().set_table_styles(styles))

    dd_accordion = widgets.Accordion(children=[dd_out])
    dd_accordion.set_title(0, 'Data Description')
    dd_accordion.selected_index = None
    return dd_accordion


def _display_footer(self, df: pd.DataFrame, df_output: pd.DataFrame, title: str = None, excel_file: str = None):
    rows = f'{str(df_output.shape[0]) + " out of " if df.shape[0] != df_output.shape[0] else ""}{df.shape[0]:d}'
    columns = f'{df.shape[1]:d}'
    title_size = widgets.HTML(
        value=f'{title + " " if not title is None else ""}{rows} rows x {columns} columns')

    footer_elements = [title_size]
    if not excel_file is None:
        df_output.to_excel(excel_file)
        excel = widgets.HTML(
            value=f' | <a href="{excel_file}">Excel Download</a>')
        footer_elements += [excel]

    return widgets.HBox(footer_elements)


def display(self, df: pd.DataFrame, head: int = 10, stats: bool = False, title: str = None, excel_file: str = None):
    """
    Displays the given data frame in a Jupyter notebook. It formats the values based on the format specification in the data dictionary.

    Args:
        df: The data frame to display.
        head: The number of row to display from the top.
        stats: Whether to add the total and the average to the top of the data frame.
        title: The title to show at the top.
        excel_file: The name of the excel file that is accessible at the bottom of the page. If no excel file is specified, the link will not be available.

    Returns:
        Composite Jupyter widget with data frame.
    """
    df_output = df
    if stats:
        df_output = self.add_stats(df_output)

    if head is not None:
        df_output = df_output.head(head)

    main = self._display_df(df_output)
    dd = self._display_dd(df_output)
    footer = self._display_footer(df, df_output, title, excel_file)

    return widgets.VBox([main, footer, dd])


DataDict._display_df = _display_df
DataDict._display_dd = _display_dd
DataDict._display_footer = _display_footer
DataDict.display = display
