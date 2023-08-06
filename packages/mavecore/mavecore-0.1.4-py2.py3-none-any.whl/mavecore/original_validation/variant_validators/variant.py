from typing import Dict

from mavecore.validation.constants import (
    variant_score_data,
    variant_count_data,
    required_score_column,
)
from mavecore.validation.exceptions import ValidationError


def validate_columns_match(variant, scoreset) -> None:
    # TODO
    # document errors correctly, note key error
    """
    Validate that a child matches parents defined columns to keep
    data in sync.

    Parameters
    __________
    variant :
    scoreset :

    Raises
    ______
    ValidationError
        If variant score columns do not match scoreset score columns.
    ValidationError
        If variant count columns do not match scoreset count columns.
    """
    try:
        if variant.score_columns != scoreset.score_columns:
            raise ValidationError(
                f"Variant defines score columns '{variant.score_columns}' "
                f"but parent defines columns '{scoreset.score_columns}. "
            )
        if variant.count_columns != scoreset.count_columns:
            raise ValidationError(
                f"Variant defines count columns '{variant.count_columns}' "
                f"but parent defines columns '{scoreset.count_columns}. "
            )
    except KeyError as error:
        raise ValidationError(f"Missing key {str(error)}")


def validate_variant_json(data: Dict[str, Dict]) -> None:
    """
    Checks a given dictionary to ensure that it is suitable to be used
    as the `data` attribute in a :class:`Variant` instance.

    Parameters
    ----------
    data : dict[str, dict]
        Dictionary of keys mapping to a list.

    Raises
    ______
    ValidationError
        If missing the required key.
    ValidationError
        If missing the required column in variant's score data.
    ValidationError
        If encountered unexpected keys.
    ValidationError
        If value for key is not of type dict.
    """
    expected_keys = [variant_score_data, variant_count_data]
    for key in expected_keys:
        if key not in data.keys():
            raise ValidationError(f"Missing the required key {key}")

    if required_score_column not in data[variant_score_data]:
        raise ValidationError(
            f"Missing required column '{required_score_column}' in variant's score data."
        )

    extras = [k for k in data.keys() if k not in set(expected_keys)]
    if len(extras) > 0:
        extras = [k for k in data.keys() if k not in expected_keys]
        raise ValidationError("Encountered unexpected keys {extras}")

    # Check the correct data types are given.
    for key in expected_keys:
        if not isinstance(data[key], dict):
            type_ = type(data[key]).__name__
            raise ValidationError(f"Value for '{key}' must be a dict not {type_}.")
