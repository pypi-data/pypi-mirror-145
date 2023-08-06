# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the InvestigatorWindowPredefinedView class

This class is internal and is only exposed via inheritance
"""

from typing import Dict, List, Sequence

from cegalprizm.investigator.views.options_colorscale import OptionsColorscale

# pylint: disable=relative-beyond-top-level
# pylint: disable=protected-access

from ..constants import DATASET_DIMENSION_NAME
from ..protos import predefined_view_pb2
from .options_colorscale import OptionsColorscale
from .options_legend import OptionsLegend
from .predefined_view import PredefinedView

_CORNER_OPTIONS = ["top-left", "top-right", "bottom-left", "bottom-right"]


class InvestigatorWindowPredefinedView(OptionsColorscale, OptionsLegend, PredefinedView):
    """A class representing a InvestigatorWindowPredefinedView

    The view defines features that are common to multiple different views.
    """

    ######################################################################
    # Tree Data
    ######################################################################

    def set_datasets_visible(self, dataset_names: Sequence[str]):
        """Set which datasets should be visible in the view

        By default, all datasets will be visible in the view.

        Note: This new list of datasets will replace any previous list supplied.

        Args:
            dataset_names (Sequence[str]): A list of dataset names to be made visible

        Raises:
            ValueError: if any dataset_names are not valid
        """
        if dataset_names is None:
            raise ValueError("dataset_names must be defined")
        if len(dataset_names) == 0:
            raise ValueError("dataset_names must contain at least 1 entry")
        for name in dataset_names:
            if name not in self._investigation.dataset_names:
                raise ValueError(f"dataset_names list should only contain {str(self._investigation.dataset_names)}")

        tree_data = next((x for x in self._data.tree_data if x.tree_name == 'dataset'), None)
        del tree_data.values[:]
        discrete_tuples = self._investigation._discrete_tuples()
        tuples = discrete_tuples[DATASET_DIMENSION_NAME]
        for dataset_tuple in tuples:
            show = dataset_tuple[2] in dataset_names
            tree_data.values.append(predefined_view_pb2.VisibleNodeIdentity(id=dataset_tuple[1], is_visible=show))

    def set_discrete_visible(self, tags: Dict[str, List[str]]):
        """Set which discrete tags should be visible in the view

        By default, all discrete tags will be visible in the view.

        Note: This new list of discrete tags will replace any previous list supplied.

        Args:
            tags (Sequence[str]): The list of discrete tags to be made visible

        Raises:
            ValueError: if any tags are not valid
        """
        if tags is None:
            raise ValueError("tags must be defined")

        if len(tags) == 0:
            raise ValueError("tags must contain at least 1 entry")

        discrete_tuples = self._investigation._discrete_tuples()
        del discrete_tuples[DATASET_DIMENSION_NAME]

        for name in tags:
            if name not in discrete_tuples.keys():
                raise ValueError(f"tags dictionary should only contain entries for {str(discrete_tuples.keys())}")
            else:
                for tag in tags[name]:
                    valid_discrete_entries = [x.name for x in discrete_tuples[name]]
                    if tag not in valid_discrete_entries:
                        raise ValueError(f"tags[{name}] should only contain entries for {str(valid_discrete_entries)}")

        tree_data = next((x for x in self._data.tree_data if x.tree_name == 'discrete'), None)
        del tree_data.values[:]
        for key in discrete_tuples.keys():
            visible_tags = tags[key]
            tuples = discrete_tuples[key]
            for named_tuple in tuples:
                show = named_tuple[2] in visible_tags
                tree_data.values.append(predefined_view_pb2.VisibleNodeIdentity(id=named_tuple[1], is_visible=show))

    def set_dataset_priority(self, dataset_names: Sequence[str]):
        """Set the priority order of the datasets

        Args:
            dataset_names (Sequence[str]): A list of dataset names in priority order

        Raises:
            ValueError: if any dataset_names are not valid
        """
        if dataset_names is None:
            raise ValueError("dataset_names must be defined")
        if len(dataset_names) == 0:
            raise ValueError("dataset_names must contain at least 1 entry")
        for name in dataset_names:
            if name not in self._investigation.dataset_names:
                raise ValueError(f"dataset_names list should only contain {str(self._investigation.dataset_names)}")

        discrete_tuples = self._investigation._discrete_tuples()
        tuples = discrete_tuples[DATASET_DIMENSION_NAME]
        self._dataset_priority_order = []
        for name in dataset_names:
            dataset_id = next((t[1] for t in tuples if t[2] == name), None)
            if dataset_id is not None:
                self._dataset_priority_order.append(dataset_id)

    ######################################################################
    # Display by data settings
    ######################################################################

    def set_color_by(self, color_by_option: str):
        """Sets what attribute in the investigation is used to determine the color of the data in the view

        Args:
            color_by_option (str): The name of the attribute in the investigation

        Raises:
            ValueError: if the color_by_option is not valid
        """
        color_by_id = self._get_color_by_id(color_by_option)
        self._data.display_by_data.selected_color_by = color_by_id

    ######################################################################
    # Data settings
    ######################################################################

    def show_data(self, show: bool):
        """Set whether the data should be shown

        Args:
            show (bool): Should the data be shown
        """
        self._data.data_settings.show_data = show

    def set_split_by(self, split_by_option: str):
        """Sets what discrete attribute in the investigation is used to split the plots in the view

        Args:
            split_by_option (str): The name of the attribute in the investigation

        Raises:
            ValueError: if the split_by_option is not valid
        """
        option = next((x.id for x in self._options.data_settings.available_split_by_options if x.name == split_by_option), None)
        if option is None:
            options = [x.name for x in self._options.data_settings.available_split_by_options]
            raise ValueError(f"split_by_option must be one of {str(options)}")
        self._data.data_settings.selected_split_by_option = option

    def set_highlight(self, highlight_option: str):
        """Sets what discrete attribute in the investigation is used as the highlight option in the view

        Args:
            highlight_option (str): The name of the attribute in the investigation

        Raises:
            ValueError: if the highlight_option is not valid
        """
        option = next((x.id for x in self._options.data_settings.available_highlight_options if x.name == highlight_option), None)
        if option is None:
            options = [x.name for x in self._options.data_settings.available_highlight_options]
            raise ValueError(f"highlight_option must be one of {str(options)}")
        self._data.data_settings.selected_highlight_option = option
