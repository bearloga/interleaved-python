import pkg_resources
import pandas as pd

def load_example_data(preference):
    """Gets a DataFrame of simulated sessions

    Parameters
    ----------
    preference : { 'none', 'a', 'b' }
        Overall simulated preference.

    Returns
    -------
    Pandas DataFrame with columns:
        timestamp        : datetime64
        search_id        : object
        event            : object
        position         : float64
        ranking_function : object

    """

    file_name = "no" if preference == "none" else preference
    file_name = "data/interleaved_" + file_name + "-pref.csv"
    stream = pkg_resources.resource_stream(__name__, file_name)
    return pd.read_csv(stream, parse_dates=['timestamp'], na_values='NA')
