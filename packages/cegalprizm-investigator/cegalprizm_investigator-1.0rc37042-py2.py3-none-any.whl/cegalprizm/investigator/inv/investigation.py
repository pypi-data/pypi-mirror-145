# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the Investigation class
"""

from typing import Callable, Dict, Iterable, List, Sequence, Tuple, Union

import os.path

import pandas

# pylint: disable=relative-beyond-top-level
# pylint: disable=import-outside-toplevel

from .. import logger
from ..constants import DATASET_DIMENSION_NAME
from ..exceptions import CegalHubError
from ..hub_context import InvPyHubContext
from ..investigations import _get_available_investigations
from ..named_tuples import ContinuousPropertyTuple, DimensionPropertyNameTuple, DiscretePropertyTuple, DiscreteTagInfoTuple
from ..protos import investigation_pb2
from ..protos import investigator_api_pb2
from ..utils import _pack_payloads
from ..utils import _get_file_chunks

from .continuous_dimension import ContinuousDimension
from .discrete_dimension import DiscreteDimension
from .discrete_dimension import _get_discrete_entries
from .dataset import Dataset

class Investigation:
    """A class representing a Blueback Investigation

    The investigation object forms the entry point for all API access to a specific investigation.
    """

    def __init__(self,
                 context: InvPyHubContext,
                 path: str = None,
                 investigation_id: str = None):

        self._info: investigator_api_pb2.InvestigationSummary = None
        self._hub_context: InvPyHubContext = context
        self._continuous_dimensions: investigator_api_pb2.ContinuousDimensionInfoCollection = None
        self._discrete_dimensions: investigator_api_pb2.DiscreteDimensionInfoCollection = None
        self._classification_groups: investigation_pb2.Classifications = None
        self._dataset_additional_discrete: list[Tuple[str, investigation_pb2.DiscreteGroup]] = None
        self._restrictions:  investigation_pb2.Restrictions = None
        self._datasets: investigator_api_pb2.DatasetInfoCollection = None

        if path and not os.path.exists(path):
            print(f"File '{path}'does not exist")
            return

        if path is not None:
            result = self._hub_context.do_client_streaming("investigator.UploadInvPyFile", _pack_payloads(_get_file_chunks(path)))
            if result[0]:
                response = investigator_api_pb2.InvestigationSummary()
                result[1].Unpack(response)
                self._info = response
            else:
                raise CegalHubError(result[1])

        elif investigation_id is not None:
            for info in _get_available_investigations(self._hub_context):
                if self._info is None and info.id == investigation_id:
                    self._info = info

        if self._info is None:
            logger.warning("Investigation cannot be accessed")
            return

        self.refresh()

        logger.info(f"Investigation: {self._info.id}")

    @property
    def id(self) -> str:
        """The identifier of this investigation

        Returns:
            str: The investigation identifier
        """
        return self._info.id

    @property
    def name(self) -> str:
        """The name of this investigation

        Returns:
            str: The investigation name
        """
        return self._info.name

    @property
    def num_continuous_dimensions(self) -> int:
        """The number of continuous dimensions

        Returns:
            int: The number of continuous dimensions
        """
        return len(self.continuous_dimension_names)

    @property
    def continuous_dimension_names(self) -> List[str]:
        """The names of the continuous dimensions

        Returns:
            list[str]: the names of the continuous dimensions
        """
        return [dimension.name for dimension in self._continuous_dimensions.values]

    @property
    def continuous_dimension_property_names(self) -> List[DimensionPropertyNameTuple]:
        """A list of containing a tuple of continuous dimension name and the property name

        Returns:
            List[Tuple[str, str]]:  A list of tuples containing the dimension name and property name for each continuous dimension
        """
        return [DimensionPropertyNameTuple(dimension.name, dimension.property_name) for dimension in self._continuous_dimensions.values]

    @property
    def num_discrete_dimensions(self) -> int:
        """The number of discrete dimensions

        Returns:
            int: The number of discrete dimensions
        """
        return len(self.discrete_dimension_names)

    @property
    def discrete_dimension_names(self) -> List[str]:
        """The names of the discrete dimensions

        Returns:
            list[str]: the names of the discrete dimensions
        """
        names = []
        if len(self.dataset_names) > 0:
            names.append(DATASET_DIMENSION_NAME)
        for dimension in self._discrete_dimensions.values:
            names.append(dimension.name)
        for classification_group in self._classification_groups.values:
            names.append(classification_group.name)
        for additional_discrete in self._dataset_additional_discrete:
            names.append(additional_discrete[1].name)
        return names

    @property
    def discrete_dimension_property_names(self) -> List[DimensionPropertyNameTuple]:
        """A list of containing a tuple of discrete dimension name and the property name

        Returns:
            List[Tuple[str, str]]:  A list of tuples containing the dimension name and property name for each discrete dimension
        """
        result = []
        if len(self.dataset_names) > 0:
            result.append(DimensionPropertyNameTuple(DATASET_DIMENSION_NAME, DATASET_DIMENSION_NAME))
        for dimension in self._discrete_dimensions.values:
            result.append(DimensionPropertyNameTuple(dimension.name, dimension.property_name))
        for classification_group in self._classification_groups.values:
            result.append(DimensionPropertyNameTuple(classification_group.name, classification_group.property_name))
        for additional_discrete in self._dataset_additional_discrete:
            result.append(DimensionPropertyNameTuple(additional_discrete[1].name, additional_discrete[1].property_name))
        return result

    @property
    def discrete_dimension_tags(self) -> Dict[str, List[str]]:
        """Returns a dictionary containing each discrete dimension name as a key
        and a list of the "tags" as the values

        Returns:
            Dict[str, List[str]]: A dictionary of dimension names and tags
        """
        result = {}
        for (key, value) in self._discrete_tuples().items():
            result[key] = [t[2] for t in value]
        return result

    @property
    def filter_names(self) -> List[str]:
        """The names of any filters

        Returns:
            list[str]: the names of any filters
        """
        names = []
        for restriction in self._restrictions.values:
            if investigation_pb2.RestrictionTypeEnum.Name(restriction.type) == 'Filter':
                names.append(restriction.name)
        return names

    @property
    def dataset_names(self) -> List[str]:
        """The names of the datasets

        Returns:
            list[str]: the names of the datasets
        """
        return [t[1] for t in self._get_datasets(self._datasets)]

    @property
    def available_units(self) -> Dict[str, List[str]]:
        """The available units for each continuous dimension

        Returns:
            Dict[str, list[str]]: a list of valid unit symbols for each continuous dimension name
        """
        return {dimension.name: dimension.available_units for dimension in self._continuous_dimensions.values}

    @property
    def invariant_units(self) -> Dict[str, str]:
        """The invariant units for each continuous dimension

        Returns:
            Dict[str, str]: the invariant unit symbol for each continuous dimension name
        """
        return {dimension.name: dimension.invariant_units for dimension in self._continuous_dimensions.values}

    @property
    def display_units(self) -> Dict[str, str]:
        """The display units for each continuous dimension

        Returns:
            Dict[str, str]: the display unit symbol for each continuous dimension name
        """
        return {dimension.name: dimension.display_units for dimension in self._continuous_dimensions.values}

    @property
    def supported_plots(self) -> List[str]:
        """A list of the plot types in which this investigation can be shown

        Returns:
            List[str]: A list of strings describing the plot types in which this investigation can be shown
        """
        return [investigator_api_pb2._PLOTENUM.values[p.plot].name.lower() for p in self._info.supported_plots if len(p.error_message) == 0]

    def get_continuous_settings(self, name: str) -> ContinuousDimension:
        """Gets the continuous dimension settings for the specified dimension name

        Args:
            name (str): The name of the continuous dimension to be used

        Raises:
            ValueError: if the name is not a valid continuous dimension

        Returns:
            ContinuousDimension: The continuous dimension object
        """
        settings = next((x for x in self._continuous_dimensions.values if x.name == name), None)
        if settings is None:
            raise ValueError(f"name must be one of {str(self.continuous_dimension_names)}")
        return ContinuousDimension(settings)

    def get_discrete_settings(self, name: str) -> DiscreteDimension:
        """Gets the discrete dimension settings for the specified dimension name

        Args:
            name (str): The name of the discrete dimension to be used

        Raises:
            ValueError: if the name is not a valid discrete dimension

        Returns:
            DiscreteDimension: The discrete discrete object
        """
        settings = next((x for x in self._discrete_dimensions.values if x.name == name), None)
        if settings is None:
            raise ValueError(f"name must be one of {str(self.discrete_dimension_names)}")
        return DiscreteDimension(settings)

    def get_dataset_settings(self, name: str) -> Dataset:
        """Gets the settings for the specified dataset name

        Args:
            name (str): The name of the dataset to be used

        Raises:
            ValueError: if the name is not a valid dataset

        Returns:
            Dataset: The dataset object
        """
        settings = next((x[0] for x in self._get_datasets(self._datasets) if x[1] == name), None)
        if settings is None:
            raise ValueError(f"name must be one of {str(self.dataset_names)}")
        return Dataset(settings)

    def as_dataframe(self,
                     dataset_name: str = None,
                     continuous_columns: Union[str, Sequence[str]] = "all",
                     continuous_units: str = "display",
                     discrete_columns: Union[str, Sequence[str]] = "all",
                     discrete_data_as: str = "string",
                     include_filters: Union[str, Sequence[str]] = "all") -> pandas.DataFrame:
        """A dataframe of all the points with both continuous and discrete dimensions

        Args:
            dataset_name (str, optional): The name of the dataset being output to the dataframe. Defaults to None.
            continuous_columns (Union[str, Sequence[str]], optional): Defaults to 'all'.
                                - 'all' will include all continuous dimensions from the investigation
                                - a list of continuous dimension names that should be included (see Investigation.continuous_dimension_names property)
                                - None which will include no continuous dimensions in the dataframe
            continuous_units (str, optional): Defaults to 'display'.
                                - 'display' will result in continuous values in invariant units
                                - 'invariant' will result in continuous values in invariant units
                                - a dictionary of continuous dimension names: a unit string (see Investigation.available_units property)
            discrete_columns (Union[str, Sequence[str]], optional): Defaults to 'all'.
                                - 'all' will include all discrete dimensions from the investigation
                                - a list of discrete dimension names that should be included (see Investigation.discrete_dimension_names property)
                                - None which will include no discrete dimensions in the dataframe
            discrete_data_as (str, optional): Defaults to 'string'.
                                - 'string' will cause discrete data tag to be returned as name
                                - 'value' will cause discrete data tag to be returned as int
            include_filters (Union[str, Sequence[str]], optional): Defaults to 'all'.
                                - 'all' will include all filters as boolean columns in the dataframe
                                - a list of filter names that should be included (see Investigation.filter_names property)
                                - None which will include no filter columns in the dataframe

        Raises:
            CegalHubError: if an unexpected error is reported by Hub

        Returns:
            pandas.DataFrame: A dataframe
        """
        from .to_dataframe import _to_dataframe

        return _to_dataframe(self,
                             dataset_name,
                             continuous_columns,
                             continuous_units,
                             discrete_columns,
                             discrete_data_as,
                             include_filters)

    def _get_datasets(self, dataset_collection, prefix: str = '') -> Iterable[Tuple[investigation_pb2.Dataset, str]]:
        for dataset in dataset_collection.values:
            if len(dataset.kids.values) == 0:
                yield tuple([dataset, prefix + dataset.name])
            else:
                for dataset_tuple in self._get_datasets(dataset.kids, prefix + dataset.name + '/'):
                    yield dataset_tuple

    def _get_additional_discrete(self) -> Iterable[Tuple[str, investigation_pb2.DiscreteGroup]]:
        for dataset_tuple in self._get_datasets(self._datasets):
            for visibility in dataset_tuple[0].data_visibilities:
                yield (dataset_tuple[0].id, visibility)

    def _discrete_tuples(self) -> Dict[str, List[DiscreteTagInfoTuple]]:
        result = {}
        if len(self.dataset_names) > 0:
            result[DATASET_DIMENSION_NAME] = [DiscreteTagInfoTuple(index, t[0].id, t[1]) for index, t in enumerate(self._get_datasets(self._datasets))]
        for dimension in self._discrete_dimensions.values:
            result[dimension.name] = [DiscreteTagInfoTuple(tag.value.index, tag.id, tag.option_name) for tag in _get_discrete_entries(dimension.group.options)]
        for classification_group in self._classification_groups.values:
            result[classification_group.name] = [DiscreteTagInfoTuple(entry.index, "", entry.name) for entry in classification_group.entries]
        for additional_discrete in self._dataset_additional_discrete:
            result[additional_discrete[1].name] = [DiscreteTagInfoTuple(tag.value.index, tag.id, tag.option_name) for tag in additional_discrete[1].options]
        return result

    def update(self):
        """Update the investigation with any recent changes

        Apply any recent changes to continuous/discrete dimensions or dataset settings to the investigation and therefore these changes will be visible when creating new plots etc

        Raises:
            CegalHubError: if an unexpected error is reported by Hub

        """
        from .update import _update_investigation
        _update_investigation(self)

    def refresh(self):
        """Refresh the investigation object

        This will fetch any changes made remotely to the investigation.
        It will override any local changes continuous/discrete dimensions or dataset settings that have not been applied by calling :func:update() method

        Raises:
            CegalHubError: if an unexpected error is reported by Hub
        """
        from .refresh import _refresh
        _refresh(self)

    def create_predictor(self, name: str, func: Callable, inputs: Sequence[ContinuousPropertyTuple], output: ContinuousPropertyTuple):
        """Create a new prediction equation in the investigation

        A new python prediction equation will be created in the investigation.
        Predictions will be made by invoking the provided func.

        Args:
            name (str): The name of the prediction to be used
            func (Callable): The function that performs the prediction
            inputs (Sequence[ContinuousPropertyTuple]):  a list of tuples each containing a continuous dimension name and a unit string
            output (ContinuousPropertyTuple): a tuple of continuous dimension name and a unit string

        Raises:
            CegalHubError: if an unexpected error is reported by Hub
            ValueError: if any of the inputs are not valid
        """
        from .models import _save_predictor
        _save_predictor(self, name, func, inputs, output)

    def create_classifier(self, name: str, func: Callable, inputs: Sequence[ContinuousPropertyTuple], output: DiscretePropertyTuple):
        """Create a new classification equation in the investigation

        A new python classification equation will be created in the investigation.
        Classifications will be made by invoking the provided func.

        Args:
            name (str): The name of the classification to be used
            func (Callable): The function that performs the classification
            inputs (Sequence[ContinuousPropertyTuple]): a list of tuples each containing a continuous dimension name and a unit string
            output (DiscretePropertyTuple): a tuple of discrete name and a list of discrete tags

        Raises:
            CegalHubError: if an unexpected error is reported by Hub
            ValueError: if any of the inputs are not valid
        """
        from .models import _save_classifier
        _save_classifier(self, name, func, inputs, output)
