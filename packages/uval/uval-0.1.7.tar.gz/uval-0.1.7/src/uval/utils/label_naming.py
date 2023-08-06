# -*- coding: utf-8 -*-
"""
    We defined a 'short' form of label names.
    That means, if we have a bag with volume id
    BAGGAGE_20171205_081937_012345
    and a label called
    BAGGAGE_20171205_081937_012345_label_2,
    we can write the label as '%_label_2'.

    To escape a '%' as actual character, we use '%%' in the short form.

    This module provides functions to convert between the two forms.
"""

import re

_lonely_percent_regex = re.compile(r"(?<!%)%(?!%)")  # A '%' with no '%' before or after


def label_short_to_long(volume_id: str, short_label_id: str) -> str:
    """
        This function will restore the full label_id if it is a short form.
        For a definition of the short and long form, see this module's docstring.
    Args:
        volume_id: The ID which represents a image file containing the volume
        short_label_id: A shortened version of label id containing '%' character

    Returns:
        Extended label_id, in which '%' is replaced by the volume_id
    """
    if "%" not in short_label_id:
        raise ValueError(f"Given short id '{short_label_id}' must contain '%' character")

    return _lonely_percent_regex.sub(volume_id, short_label_id).replace("%%", "%")


def label_long_to_short(volume_id: str, long_label_id: str) -> str:
    """
        This function will shorten the full label_id if possible.
        For a definition of the short and long form, see this module's docstring.
    Args:
        volume_id: The ID which represents a image file containing the volume
        long_label_id: Full id of label with no '%' inside

    Returns:
        Shortened label_id, in which the volume_id is replaced by '%'
    """
    if volume_id not in long_label_id:
        raise ValueError(f"The long id {long_label_id} must contain the '{volume_id}' short id")

    return long_label_id.replace("%", "%%").replace(volume_id, "%")
