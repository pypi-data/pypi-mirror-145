import io
import csv
import re

from numpy.testing import assert_array_equal

from mavecore.validation import constants
from mavecore.validation.exceptions import ValidationError

from mavecore.validation.utilities import is_null


def is_null(value):
    """
    Checks if a stripped/lowercase value is one of the recognized NA or NULL string values.

    Parameters
    __________
    value : str
        The value to be checked as null or not.

    Returns
    _______
    bool
        True value is NoneType, is an empty string, or if value matches the stated regex patterns in
        constants.null_values_re.
    """
    value = str(value).strip().lower()
    return constants.null_values_re.fullmatch(value) or not value


class WordLimitValidator:
    """
    This class

    Attributes
    __________
    message : str
        Message template to describe how many words a field is limited to.
    code : str

    counter : str

    """

    message = "This field is limited to {} words."
    code = "invalid"
    counter = re.compile(r"\w+\b", flags=re.IGNORECASE)

    def __init__(self, word_limit, message=None, code=None):
        # check the code parameter type
        """
        This constructor sets the values of the WordLimitValidator class attributes
        message, code, and counter.

        Parameters
        __________
        word_limit : int
            The word limit assigned to the word limit attribute.
        message : str
            (default = None) The message assigned to the message attribute.
        code :
            (default = None) The code assigned to the code attribute.
        """
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        self.word_limit = int(word_limit)

    def __call__(self, value):
        """
        Parameters
        __________
        value :

        Returns
        _______

        Raises
        ______
        ValidationError
            If
        """
        if not value:
            return
        if len(self.counter.findall(value)) > self.word_limit:
            raise ValidationError(self.message.format(self.word_limit))


def read_header_from_io(file, label=None, msg=None):
    # TODO
    # confirm types for parameters
    """
    This takes a file and reads the header from that file.

    Parameters
    __________
    file :
    label : str
        (default = None)
    msg : str
        (default = None) The message that is printed in the event of an error is raised.

    Returns
    _______
    str
        The header that was read from io.

    Raises
    ______
    ValidationError
        If a header could not be parsed from file. Columns must be coma delimited. Column names
        with commas must be escaped by enclosing them in double quotes.
    """
    if label is None:
        label = "uploaded"

    try:
        header_line = file.readline()
        if isinstance(header_line, bytes):
            header_line = header_line.decode()
        file.seek(0)
        f = io.StringIO(header_line.strip())
        return [h.strip() for h in csv.DictReader(f, delimiter=",").fieldnames]
    except Exception:
        if not msg:
            msg = (
                "A header could not be parsed from your {} file. Make sure"
                "Columns are comma delimited. Column names with commas must be"
                "escaped by enclosing them in double quotes.".format(label)
            )
        raise ValidationError(msg)


def validate_has_hgvs_in_header(header, label=None, msg=None):
    """
    Parameters
    __________
    header :
    label :
        default = None
    msg :
        default = None

    Raises
    ______
    ValidationError
        If
    """
    if label is None:
        label = "Uploaded"
    params = {}
    if msg is None:
        msg = (
            "Your %(label)s file must define either a nucleotide hgvs column "
            "'%(col_nt)s' or a protein hgvs column '%(col_p)s'. "
            "Columns are case-sensitive and must be comma delimited."
        )
        params = {
            "label": label,
            "col_nt": constants.hgvs_nt_column,
            "col_p": constants.hgvs_pro_column,
        }
    if not set(header) & set(constants.hgvs_columns):
        raise ValidationError(msg)


def validate_at_least_one_additional_column(header, label=None, msg=None):
    # TODO
    # verify parameter types
    """
    This function checks the passed header to see if there exists additional columns besides the three
    specified by constants.hgvs_nt_column, constants.hgvs_splice_column, and constants.hgvs_pro_column.

    Parameters
    __________
    header :
    label :
        default = None
    msg :
        default = None

    Raises
    ______
    ValidationError
        If there are not additional columns in the header argument.
    """
    if label is None:
        label = "Uploaded"
    params = {}
    if not any(v not in constants.hgvs_columns for v in header):
        if msg is None:
            msg = (
                "Your %(label)s file must define at "
                "least one additional column different "
                "from '{}', '{}' and '{}'.".format(
                    constants.hgvs_nt_column,
                    constants.hgvs_splice_column,
                    constants.hgvs_pro_column,
                )
            )
            params = {"label": label}
        raise ValidationError(msg)


def validate_header_contains_no_null_columns(header, label=None, msg=None):
    """
    This function checks that the header parameter does not contain any null columns that
    are not in the case-insensitive null values listed in constants.readable_null_values.

    Parameters
    __________
    header :
    label :
        (default = None)
    msg :
        (default = None)

    Raises
    ______
    ValidationError
         If the file header contains blank/empty/whitespace. Only columns or the
         case-insensitive null values listed in constants.readable_null_values
         are permitted.
    """
    if label is None:
        label = "File"
    any_null = any([is_null(v) for v in header])
    if any_null:
        if msg is None:
            msg = (
                "%(label)s file header cannot contain blank/empty/whitespace "
                "only columns or the following case-insensitive null "
                "values: {}.".format(
                    label, ", ".join(constants.readable_null_values_list)
                )
            )
        raise ValidationError(msg)


def validate_datasets_define_same_variants(scores, counts):
    """
    Checks if two `pd.DataFrame` objects parsed from uploaded files
    define the same variants.

    Parameters
    ----------
    scores : `pd.DataFrame`
        Scores dataframe parsed from an uploaded scores file.
    counts : `pd.DataFrame`
        Scores dataframe parsed from an uploaded counts file.

    Raises
    ______
    ValidationError
        If score and counts files do not define the same variants.
    """
    try:
        assert_array_equal(
            scores[constants.hgvs_nt_column].sort_values().values,
            counts[constants.hgvs_nt_column].sort_values().values,
        )
        assert_array_equal(
            scores[constants.hgvs_splice_column].sort_values().values,
            counts[constants.hgvs_splice_column].sort_values().values,
        )
        assert_array_equal(
            scores[constants.hgvs_pro_column].sort_values().values,
            counts[constants.hgvs_pro_column].sort_values().values,
        )
    except AssertionError:
        raise ValidationError(
            "Your score and counts files do not define the same variants. "
            "Check that the hgvs columns in both files match."
        )


def validate_scoreset_score_data_input(file):
    """
    Validator function for checking that the scores file input contains
    at least the column 'hgvs' and 'score'. Returns the file to position 0
    after reading the header (first line).

    Parameters
    ----------
    file : :class:`io.FileIO`
        An open file handle in read mode.

    Raises
    ______
    ValidationError
        If score data file is missing the required column constants.required_score_column
    """
    file.seek(0)
    header = read_header_from_io(file, label="Score")
    validate_header_contains_no_null_columns(header, label="Score")
    validate_has_hgvs_in_header(header, label="Score")
    validate_at_least_one_additional_column(header, label="Score")

    if constants.required_score_column not in header:
        raise ValidationError(
            "Score data file is missing the required column "
            + constants.required_score_column
            + "."
            + "Columns are case-sensitive and must be comma delimited."
        )


def validate_scoreset_count_data_input(file):
    """
    Validator function for checking that the counts file input contains
    at least the column 'hgvs'. Returns the file to position 0
    after reading the header (first line).

    Parameters
    ----------
    file : :class:`io.FileIO`
        File parsed by a `django` form.
    """
    file.seek(0)
    header = read_header_from_io(file, label="Count")
    validate_header_contains_no_null_columns(header, label="Count")
    validate_has_hgvs_in_header(header, label="Count")
    validate_at_least_one_additional_column(header, label="Count")


def validate_scoreset_json(dict_):
    """
    Checks a given dictionary to ensure that it is suitable to be used
    as the `dataset_columns` attribute in a :class:`ScoreSet` instance.

    Parameters
    ----------
    dict_ : dict
        Dictionary of keys mapping to a list.

    Raises
    ______
    ValidationError
        If scoreset data is missing the required key.
    ValidationError
        If header values are not strings.
    ValidationError
        If
    ValidationError
        If missing required column constants.required_score_column for score dataset.
    ValidationError
        If encountered unexpected keys extras.
    """
    required_columns = [constants.score_columns, constants.count_columns]

    for key in required_columns:
        if key not in dict_.keys():
            raise ValidationError("Scoreset data is missing the required key " + key)

        columns = dict_[key]
        if not all([isinstance(c, str) for c in columns]):
            raise ValidationError("Header values must be strings.")

        if not isinstance(columns, list):
            type_ = type(columns).__name__
            raise ValidationError(
                "Value for " + key.replace("_", " ") + " must be a list not " + type_
            )

        # Check score columns is not-empty and at least contains hgvs and score
        if key == constants.score_columns:
            if constants.required_score_column not in columns:
                raise ValidationError(
                    "Missing required column constants.required_score_column "
                    "for score dataset."
                )

    # Check there are not unexpected columns supplied to the scoreset json
    # field.
    extras = [k for k in dict_.keys() if k not in set(required_columns)]
    if len(extras) > 0:
        extras = [k for k in dict_.keys() if k not in required_columns]
        raise ValidationError("Encountered unexpected keys extras")
