import re
from mavecore.validation.exceptions import ValidationError

MAVEDB_EXPERIMENTSET_URN_DIGITS = 8
MAVEDB_TMP_URN_DIGITS = 16
MAVEDB_URN_MAX_LENGTH = 64
MAVEDB_URN_NAMESPACE = "mavedb"


# Temp URN patterns
# --------------------------------------------------------------------------- #
MAVEDB_TMP_URN_PATTERN = r"^tmp:[A-Za-z0-9]{{{width}}}$".format(
    width=MAVEDB_TMP_URN_DIGITS
)
MAVEDB_TMP_URN_RE = re.compile(MAVEDB_TMP_URN_PATTERN)


# Experimentset Pattern/Compiled RE
MAVEDB_EXPERIMENTSET_URN_PATTERN = r"^urn:{namespace}:\d{{{width}}}$".format(
    namespace=MAVEDB_URN_NAMESPACE, width=MAVEDB_EXPERIMENTSET_URN_DIGITS
)
MAVEDB_EXPERIMENTSET_URN_RE = re.compile(MAVEDB_EXPERIMENTSET_URN_PATTERN)

# Experiment Pattern/Compiled RE
MAVEDB_EXPERIMENT_URN_PATTERN = r"{pattern}-([a-z]+|0)$".format(
    pattern=MAVEDB_EXPERIMENTSET_URN_PATTERN[:-1]
)
MAVEDB_EXPERIMENT_URN_RE = re.compile(MAVEDB_EXPERIMENT_URN_PATTERN)

# Scoreset Pattern/Compiled RE
MAVEDB_SCORESET_URN_PATTERN = r"{pattern}-\d+$".format(
    pattern=MAVEDB_EXPERIMENT_URN_PATTERN[:-1]
)
MAVEDB_SCORESET_URN_RE = re.compile(MAVEDB_SCORESET_URN_PATTERN)

# Variant Pattern/Compiled RE
MAVEDB_VARIANT_URN_PATTERN = r"{pattern}#\d+$".format(
    pattern=MAVEDB_SCORESET_URN_PATTERN[:-1]
)
MAVEDB_VARIANT_URN_RE = re.compile(MAVEDB_VARIANT_URN_PATTERN)

# Any Pattern/Compiled RE
MAVEDB_ANY_URN_PATTERN = "|".join(
    [
        r"({pattern})".format(pattern=p)
        for p in (
            MAVEDB_EXPERIMENTSET_URN_PATTERN,
            MAVEDB_EXPERIMENT_URN_PATTERN,
            MAVEDB_SCORESET_URN_PATTERN,
            MAVEDB_VARIANT_URN_PATTERN,
            MAVEDB_TMP_URN_PATTERN,
        )
    ]
)
MAVEDB_ANY_URN_RE = re.compile(MAVEDB_ANY_URN_PATTERN)


def validate_mavedb_urn(urn):
    # TODO, currently not functioning in MaveDB
    """
    This function validates a MaveDB urn and raises an error if it is not valid.

    Parameters
    __________
    urn : str
        The MaveDB urn to be validated.

    Raises
    ______
    ValidationError
        If the MaveDB urn is not valid.
    """
    if not MAVEDB_ANY_URN_RE.match(urn):
        raise ValidationError("{}'s is not a valid urn.".format(urn))


def validate_mavedb_urn_experimentset(urn):
    """
    This function validates a Experiment Set urn and raises an error if it is not valid.

    Parameters
    __________
    urn : str
        The Experiment Set urn to be validated.

    Raises
    ______
    ValidationError
        If the Experiment Set urn is not valid.
    """
    if not (MAVEDB_EXPERIMENTSET_URN_RE.match(urn) or MAVEDB_TMP_URN_RE.match(urn)):
        raise ValidationError(
            # "Error test"
            "{}'s is not a valid Experiment Set urn.".format(urn)
        )


def validate_mavedb_urn_experiment(urn):
    """
    This function validates an Experiment urn and raises an error if it is not valid.

    Parameters
    __________
    urn : str
        The Experiment urn to be validated.

    Raises
    ______
    ValidationError
        If the Experiemnt urn is not valid.
    """
    if not (MAVEDB_EXPERIMENT_URN_RE.match(urn) or MAVEDB_TMP_URN_RE.match(urn)):
        raise ValidationError(
            "{}'s is not a valid Experiment urn.".format(urn)
        )


def validate_mavedb_urn_scoreset(urn):
    """
    This function validates a Scoreset urn and raises an error if it is not valid.

    Parameters
    __________
    urn : str
        The Scoreset urn to be validated

    Raises
    ______
    ValidationError
        If the Scoreset urn is not valid.
    """
    if not (MAVEDB_SCORESET_URN_RE.match(urn) or MAVEDB_TMP_URN_RE.match(urn)):
        raise ValidationError("{}'s is not a valid score set urn.".format(urn))


def validate_mavedb_urn_variant(urn):
    """
    This function validates a MaveDB Variant urn and raises an error if it is not valid.

    Parameters
    __________
    urn : str
        The MaveDB Variant urn to be validated.

    Raises
    ______
    ValidationError
        If the MaveDB Variant urn is not valid.
    """
    if not (MAVEDB_VARIANT_URN_RE.match(urn) or MAVEDB_TMP_URN_RE.match(urn)):
        raise ValidationError("{}'s is not a valid Variant urn.".format(urn))
