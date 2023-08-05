import re
from functools import reduce
import numpy as np
from hestia_earth.schema import NodeType

from .tools import flatten


def pivot_csv(filepath: str, exclude_columns=[]):
    """
    Pivot the values of term.@id columns, forming new columns with values taken from the respective .value columns.

    Note that this function requires pandas, which is not included in the package requirements by default due to size.

    Parameters
    ----------
    filepath : str
        Path to the CSV to be pivoted.

    exclude_columns : list
        Which columns to exclude.

    Returns
    -------
    pandas.DataFrame
        Pivoted pandas dataframe
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("Run `pip install pandas~=1.2.0` to use this functionality")

    df = pd.read_csv(filepath, index_col=None)

    term_columns_to_pivot = df.filter(regex=r'^.*\.[a-zA-Z]+\.[\d]+\.term\.@id$')
    term_columns_to_pivot = list(filter(lambda x: x not in exclude_columns, term_columns_to_pivot))

    df_out = df.copy()

    # drop all columns for pivot
    term_columns_no_pivot = list(df.filter(regex=r'^.*\.[a-zA-Z]+\.[\d]').columns.values)
    df_out.drop(term_columns_no_pivot, axis=1, inplace=True)

    out = []
    for column in term_columns_to_pivot:
        stem = column.rstrip('.term.@id')
        value_col = '.'.join([stem, 'value'])

        # handle node without value column
        if value_col not in df:
            df[value_col] = '-'

        p = df.pivot(columns=[column], values=[value_col])

        p = p.dropna(axis=1, how='all')
        p = p.droplevel(axis=1, level=0)
        p = p.rename(lambda x: '.'.join([re.sub(r'(\.[\d]+)$', '', stem), x, 'value']), axis=1)

        out.append(p)

    pivoted_columns = pd.concat(out, axis=1)
    return pd.concat((df_out, pivoted_columns), axis=1)


def _replace_ids(df):
    # in columns, first letter is always lower case
    node_types = [e.value[0].lower() + e.value[1:] for e in NodeType]
    # add extra subvalues
    subvalues = ['source', 'defaultSource', 'site', 'organisation', 'cycle']
    node_types = node_types + flatten([v + '.' + value for v in node_types] for value in subvalues)
    columns = reduce(lambda prev, curr: {**prev, curr + '.@id': curr + '.id'}, node_types, {})
    return df.rename(columns=columns)


def _clean_term_columns(df):
    columns = ['name', 'termType', 'units']
    cols = [c for c in df.columns if all([not c.endswith('.' + v) for v in columns])]
    return df[cols]


def _replace_nan_values(df, col: str, columns: list):
    for index, row in df.iterrows():
        try:
            value = row[col]
            if np.isnan(value):
                for empty_col in columns:
                    df.loc[index, empty_col] = np.nan
        except TypeError:
            continue
    return df


def _empty_impact_na_values(df):
    impacts_columns = [c for c in df.columns if '.impacts.']
    impacts_values_columns = [c for c in impacts_columns if c.endswith('.value')]
    for col in impacts_values_columns:
        col_prefix = col.replace('.value', '')
        same_col = [c for c in impacts_columns if c.startswith(col_prefix) and c != col]
        _replace_nan_values(df, col, same_col)
    return df


def format_for_upload(filepath: str):
    """
    Format downloaded file for upload on Hestia platform.
    Will replace all instances of `@id` to `id`, and drop the columns ending by `name`, `termType` or `units`.

    Parameters
    ----------
    filepath : str
        Path to the CSV to be formatted.

    Returns
    -------
    pandas.DataFrame
        Formatted pandas dataframe
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("Run `pip install pandas~=1.2.0` to use this functionality")

    df = pd.read_csv(filepath, index_col=None, na_values='')

    # replace @id with id for top-level Node
    df = _replace_ids(df)

    # drop all term columns that are not needed
    df = _clean_term_columns(df)

    # empty values for impacts which value are empty
    df = _empty_impact_na_values(df)

    return df
