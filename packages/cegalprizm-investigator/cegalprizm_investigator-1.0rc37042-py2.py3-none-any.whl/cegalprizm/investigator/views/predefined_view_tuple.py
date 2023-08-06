# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of various named tuples used by Investigator
"""

from typing import List, NamedTuple

from .predefined_view import PredefinedView


class PredefinedViewTuple(NamedTuple):
    """This is a named tuple that defines the description of a view
    """

    name: str
    view: PredefinedView