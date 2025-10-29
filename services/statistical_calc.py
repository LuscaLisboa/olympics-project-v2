import pandas as pd


def total_calc(df: pd.DataFrame) -> dict[str, int]:
    """
    Return total of values not null within each column of DataFrame.

    Args:
        df (pd.DataFrame):

    Returns:
        dict: {name_column: total_of_values}
    """

    return df.count().to_dict()

def average_calc(df: pd.DataFrame) -> dict[str, int]:
    """
    Return average within each column of DataFrame.

    Args:
        df (pd.DataFrame):

    Returns:
        dict: {name_column: average_of_values}
    """

    return df.mean().to_dict()