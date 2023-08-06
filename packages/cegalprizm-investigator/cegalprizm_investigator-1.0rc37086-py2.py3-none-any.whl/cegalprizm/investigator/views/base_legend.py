# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the colorscale options class

This class is internal and is only exposed via inheritance
"""

# pylint: disable=relative-beyond-top-level
# pylint: disable=protected-access

from ..protos import predefined_view_pb2
from .predefined_view import PredefinedView

_CORNER_OPTIONS = ["top-left", "top-right", "bottom-left", "bottom-right"]

class BaseLegend(PredefinedView):

    def _set_legend_location(self, legend_settings: predefined_view_pb2.SettingsLegend, inside_viewport: bool, corner: str):
        if corner not in _CORNER_OPTIONS:
            raise ValueError(f"corner must be one of {str(_CORNER_OPTIONS)}")
        legend_settings.inside_viewport = inside_viewport
        legend_settings.show_at_top = "top" in corner
        legend_settings.show_at_left = "left" in corner

    def _show_legend_frame(self, legend_settings, show_frame: bool):
        legend_settings.show_frame = show_frame
