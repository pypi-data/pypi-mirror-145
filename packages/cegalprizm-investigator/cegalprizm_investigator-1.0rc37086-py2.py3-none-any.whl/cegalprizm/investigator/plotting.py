# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the methods to be used to plot investigations
"""

from typing import Sequence, Union

from io import BytesIO

import PIL.Image
from google.protobuf.any_pb2 import Any
import ipyplot

# pylint: disable=relative-beyond-top-level

from .exceptions import CegalHubError
from .protos import investigator_api_pb2
from .views.predefined_view_tuple import PredefinedViewTuple
from .views.predefined_view import PredefinedView


def plot(view: Union[PredefinedView, PredefinedViewTuple], width: int = 900, height: int = 600) -> PIL.Image.Image:
    """Creates plot based on the provided view

    This will display an image of a defined size based on the provided view.

    Args:
        view (Union[PredefinedView, PredefinedViewTuple]): Either the view or a tuple containing the label and view defining the plot
        width (int, optional): The width of the image to be displayed. Defaults to 900.
        height (int, optional): The height of the image to be displayed. Defaults to 600.

    Raises:
        CegalHubError: if an unexpected error is reported by Hub

    Returns:
        Image: The generated plot image (if not displayed)
    """
    img = None
    if isinstance(view, PredefinedView):
        img = __get_image(view, width, height)
    elif isinstance(view, PredefinedViewTuple) and isinstance(view.name, str) and isinstance(view.view, PredefinedView):
        img = __get_image(view, width, height)
    else:
        raise ValueError("view must be either a PredefinedView or PredefinedViewTuple")
    return img

def multi_plot(views: Sequence[Union[PredefinedView, PredefinedViewTuple]], width: int = 900, height: int = 600):
    """Creates a grid of plots based on the provided list of views

    This will display aa grid of images of a defined size based on the provided views.

    Args:
        views (Sequence[Union[PredefinedView, PredefinedViewTuple]]): A list of either views or tuples containing the label and view defining the plots
        width (int, optional): The width of the images to be displayed. Defaults to 900.
        height (int, optional): The height of the images to be displayed. Defaults to 600.

    Raises:
        CegalHubError: if an unexpected error is reported by Hub
    """
    images = []
    labels = []
    for view in views:
        img = None
        label = ""
        if isinstance(view, PredefinedView):
            img = __get_image(view, width, height)
        elif isinstance(view, PredefinedViewTuple) and isinstance(view.name, str) and isinstance(view.view, PredefinedView):
            label = view.name
            img = __get_image(view.view, width, height)
        labels.append(label)
        images.append(img)
    return ipyplot.plot_images(images, labels, img_width=width)

def __get_image(view: PredefinedView, width: int = 950, height: int = 600) -> PIL.Image.Image:
    msg = investigator_api_pb2.GetPlotImageRequest(view=view._data)
    msg.investigation_id.id = view._investigation.id
    msg.plot = investigator_api_pb2.PlotEnum.Value(view._plot_type)
    msg.width = width
    msg.height = height
    for dataset_id in view._dataset_priority_order:
        msg.dataset_priority_order.append(dataset_id)

    payload = Any()
    payload.Pack(msg)

    result = view._investigation._hub_context.do_unary_request("investigator.GetPredefinedImage", payload)
    if result[0]:
        response = investigator_api_pb2.GetPlotImageResponse()
        result[1].Unpack(response)
        with BytesIO(response.image) as file:
            img = PIL.Image.open(file)
            img.load()
            return img
    else:
        raise CegalHubError(result[1])
