from mavecore.validation.constants import null_values_re

def is_null(value):
    """
    Returns True if a stripped/lowercase value in in `nan_col_values`.

    Parameters
    __________
    value : str
        The value to be checked as null or not.

    Returns
    _______
    bool
        True value is NoneType or if value matches the stated regex patterns in constants.null_values_re.
    """
    value = str(value).strip().lower()
    return null_values_re.fullmatch(value) or not value