# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the SeismicLineView class
"""

# pylint: disable=relative-beyond-top-level
# pylint: disable=protected-access

from typing import Union

import ctypes

from ..inv.investigation import Investigation
from ..utils import _color_name_to_int

from .options_colorscale import OptionsColorscale
from .predefined_view import PredefinedView


class SeismicLineView(OptionsColorscale, PredefinedView):
    """A class representing a SeismicLineView

    The view defines how a seismic line should be displayed.
    It allows control of both what data should be displayed and how the the data should be rendered.
    """

    def __init__(self, investigation: Investigation):
        super().__init__(investigation, "Seismic")

    def copy(self):
        """Create a copy of this view

        Returns:
            SeismicLineView: the copied view
        """
        copy = SeismicLineView(None)
        copy._investigation = self._investigation
        copy._plot_type = self._plot_type
        copy._options = self._options
        copy._data.CopyFrom(self._data)
        copy._dataset_priority_order = list(self._dataset_priority_order)
        return copy

    def set_property(self, property_name: str):
        """Set the property to be shown in the view

        Args:
            property_name (str): The name of the property to be displayed

        Raises:
            ValueError: if the property_name is not a valid
        """
        del self._data.log_tracks_settings.selected_properties[:]
        self._data.log_tracks_settings.selected_properties.append(self.__get_property_id(property_name))

    def set_inline(self, value: int):
        """Set the inline to be displayed in the view

        Args:
            value (int): The inline to be shown

        Raises:
            ValueError: if the value is not valid
        """
        if value < self._options.seismic_line_settings.range_inline.min or value > self._options.seismic_line_settings.range_inline.max:
            raise ValueError(f"value must be between {self._options.seismic_line_settings.range_inline.min} and {self._options.seismic_line_settings.range_inline.max}")

        self._data.seismic_line_settings.selected_line_type = "il"
        self._data.seismic_line_settings.selected_inline = value

    def set_crossline(self, value: int):
        """Set the crossline to be displayed in the view

        Args:
            value (int): The crossline to be shown

        Raises:
            ValueError: if the value is not valid
        """
        if value < self._options.seismic_line_settings.range_crossline.min or value > self._options.seismic_line_settings.range_crossline.max:
            raise ValueError(f"value must be between {self._options.seismic_line_settings.range_crossline.min} and {self._options.seismic_line_settings.range_crossline.max}")

        self._data.seismic_line_settings.selected_line_type = "xl"
        self._data.seismic_line_settings.selected_xline = value

    def show_area_density(self, show: bool):
        """Set whether the area density should be shown in the view

        Args:
            show (bool): Should the area density plot be shown
        """
        self._data.log_tracks_settings.show_area_density = show

    def set_interpolate_area_density(self, interpolate: bool):
        """Set whether the area density should be interpolated when shown in the view

        Args:
            interpolate (bool): Should the area density be interpolated
        """
        self._data.log_tracks_settings.area_density_interpolation = "interpolate" if interpolate else "coarse"

    def show_wiggles(self, show: bool):
        """Set whether the seismic wiggles should be shown in the view

        Args:
            show (bool): Should the wiggles be shown
        """
        self._data.log_tracks_settings.show_wiggles = show

    def show_left_wiggle_fill(self, show: bool):
        """Set whether the left wiggle should be filled

        Args:
            show (bool): Should the left wiggle be filled
        """
        self._data.log_tracks_settings.show_left_wiggle_fill = show

    def set_left_wiggle_color(self, color: Union[int, str]):
        """Set the color to be used for the left wiggle fill

        Args:
            color (Union[int, str]): Either the int value or the matplotlib colorname to be used

        Raises:
            ValueError: if color is not an int or a recognised matplotlib colorname
        """
        if isinstance(color, int):
            col = color
        elif isinstance(color, str):
            col = _color_name_to_int(color)
        else:
            raise ValueError("color must be int or str")

        self._data.log_tracks_settings.color_left_wiggle_fill = ctypes.c_int32(col).value

    def show_right_wiggle_fill(self, show: bool):
        """Set whether the right wiggle should be filled

        Args:
            show (bool): Should the right wiggle be filled
        """
        self._data.log_tracks_settings.show_right_wiggle_fill = show

    def set_right_wiggle_color(self, color: Union[int, str]):
        """Set the color to be used for the right wiggle fill

        Args:
            color (Union[int, str]): Either the int value or the matplotlib colorname to be used

        Raises:
            ValueError: if color is not an int or a recognised matplotlib colorname
        """
        if isinstance(color, int):
            col = color
        elif isinstance(color, str):
            col = _color_name_to_int(color)
        else:
            raise ValueError("color must be int or str")

        self._data.log_tracks_settings.color_right_wiggle_fill = ctypes.c_int32(col).value

    ######################################################################
    # Private methods
    ######################################################################

    def __get_property_id(self, name: str):
        option_id = next((x.id for x in self._options.log_tracks_settings.available_properties if x.name == name), None)
        if option_id is None:
            options = [x.name for x in self._options.log_tracks_settings.available_properties]
            raise ValueError(f"name must be one of {str(options)}")
        return option_id
