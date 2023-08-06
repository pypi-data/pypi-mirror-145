# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the symbol legend options

This class is internal and is only exposed via inheritance
"""

# pylint: disable=relative-beyond-top-level
# pylint: disable=protected-access

from .base_legend import BaseLegend

class OptionsLegend(BaseLegend):
    """A class representing the legend options
    """

    def show_legend(self, show: bool):
        """Set whether the legend is shown

        Args:
            show (bool): Should the legend be shown
        """
        self._data.general_settings.show_legend = show

    def set_legend_location(self, inside_viewport: bool, corner: str):
        """Set where in the plot the legend is to be shown

        Args:
            inside_viewport (bool): If True, the legend will be shown inside the viewport
            corner (str): A string indicating the desired location of the legend

        Raises:
            ValueError: if the corner is not a valid string
        """
        self._set_legend_location(self._data.general_settings.symbol_legend, inside_viewport, corner)

    def show_legend_frame(self, show_frame: bool):
        """Set whether the frame should be shown around the legend

        The default value is True.

        Args:
            show_frame (bool): If True; a frame will be shown around the legend
        """
        self._show_legend_frame(self._data.general_settings.symbol_legend, show_frame)
