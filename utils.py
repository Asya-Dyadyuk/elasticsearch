import pandas as pd


def is_numeric(value):
    """
    Checks if the value is numeric (int or float).

    Args:
        value: The value to check.

    Returns:
        True if the value is numeric, otherwise False.
    """
    return isinstance(value, (int, float))


def is_integer_value(value):
    """
    Checks if the value is an integer (no decimal part).

    Args:
        value: The value to check.

    Returns:
        True if the value is an integer, otherwise False.
    """
    return isinstance(value, (int, float)) and value.is_integer()


def find_numeric_columns(df):
    """
    Finds columns in the DataFrame containing at least one numeric value.
    Returns a dictionary describing the numeric types of the columns.

    Args:
        df: The DataFrame to analyze.

    Returns:
        A dictionary describing the types of numeric columns.
    """
    numeric_columns = {}
    for column in df.columns:
        # Filter numeric values from the column
        numeric_values = df[column].dropna().apply(lambda x: x if is_numeric(x) else None)
        if not numeric_values.isna().all():
            if all(is_integer_value(val) for val in numeric_values.dropna()):
                numeric_columns[column] = 'integer'
            else:
                numeric_columns[column] = 'float'
    return numeric_columns


def is_valid_date(date_string):
    """
    Checks if the date string is valid according to the format '%m/%d/%Y'.

    Args:
        date_string: The date string to check.

    Returns:
        True if the date string is valid, otherwise False.
    """
    try:
        pd.to_datetime(date_string, format='%m/%d/%Y', errors='raise')
        return True
    except ValueError:
        return False


def find_date_columns(df):
    """
    Finds columns in the DataFrame containing at least one valid date.
    Returns a dictionary with columns and their first valid date.

    Args:
        df: The DataFrame to analyze.

    Returns:
        A dictionary where the keys are column names and the values are the first valid dates.
    """
    date_columns = {}
    for column in df.columns:
        valid_dates = df[column].dropna().apply(lambda x: x if is_valid_date(x) else None)
        if not valid_dates.isna().all():
            date_columns[column] = valid_dates.dropna().iloc[0]
    return date_columns
