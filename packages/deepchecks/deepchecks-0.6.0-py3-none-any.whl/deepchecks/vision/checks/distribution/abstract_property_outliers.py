# ----------------------------------------------------------------------------
# Copyright (C) 2021-2022 Deepchecks (https://www.deepchecks.com)
#
# This file is part of Deepchecks.
# Deepchecks is distributed under the terms of the GNU Affero General
# Public License (version 3 or later).
# You should have received a copy of the GNU Affero General Public License
# along with Deepchecks.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------------
#
"""Module contains AbstractPropertyOutliers check."""
import typing as t
from abc import abstractmethod
from collections import defaultdict
from numbers import Number

import numpy as np

from deepchecks.utils.strings import format_number
from deepchecks import CheckResult
from deepchecks.core import DatasetKind
from deepchecks.core.errors import DeepchecksProcessError, NotEnoughSamplesError, DeepchecksValueError
from deepchecks.utils.outliers import iqr_outliers_range
from deepchecks.vision import SingleDatasetCheck, Context, Batch
from deepchecks.vision.utils import label_prediction_properties
from deepchecks.vision.utils.image_functions import prepare_thumbnail
from deepchecks.vision.vision_data import VisionData

__all__ = ['AbstractPropertyOutliers']


class AbstractPropertyOutliers(SingleDatasetCheck):
    """Find outliers samples with respect to the given properties.

    The check computes several properties and then computes the number of outliers for each property.
    The check uses `IQR <https://en.wikipedia.org/wiki/Interquartile_range#Outliers>`_ to detect outliers out of the
    single dimension properties.

    Parameters
    ----------
    properties : List[Dict[str, Any]], default: None
        List of properties. Replaces the default deepchecks properties.
        Each property is dictionary with keys 'name' (str), 'method' (Callable) and 'output_type' (str),
        representing attributes of said method. 'output_type' must be one of 'continuous'/'discrete'
    n_show_top : int , default: 5
        number of outliers to show from each direction (upper limit and bottom limit)
    iqr_percentiles: Tuple[int, int], default: (25, 75)
        Two percentiles which define the IQR range
    iqr_scale: float, default: 1.5
        The scale to multiply the IQR range for the outliers detection
    """

    def __init__(self,
                 properties: t.List[t.Dict[str, t.Any]] = None,
                 n_show_top: int = 5,
                 iqr_percentiles: t.Tuple[int, int] = (25, 75),
                 iqr_scale: float = 1.5,
                 **kwargs):
        super().__init__(**kwargs)
        if properties is not None:
            label_prediction_properties.validate_properties(properties)
            # Validate no property have class_id as output_type
            if any(p['output_type'] == 'class_id' for p in properties):
                raise DeepchecksValueError('Properties cannot have class_id as output_type for outliers checks')
            self.user_properties = properties
        else:
            self.user_properties = None

        self.iqr_percentiles = iqr_percentiles
        self.iqr_scale = iqr_scale
        self.n_show_top = n_show_top
        self._properties_results = None
        self._properties_funcs = None

    def initialize_run(self, context: Context, dataset_kind: DatasetKind):
        """Initialize the properties state."""
        self._properties_results = defaultdict(list)
        data = context.get_data_by_kind(dataset_kind)

        # Take either alternative properties if defined or default properties defined by the child class
        if self.user_properties is not None:
            self._properties_funcs = self.user_properties
        else:
            self._properties_funcs = self.get_default_properties(data)
            # Filter out properties that have class_id as output_type
            self._properties_funcs = [p for p in self._properties_funcs if p['output_type'] != 'class_id']

    def update(self, context: Context, batch: Batch, dataset_kind: DatasetKind):
        """Aggregate image properties from batch."""
        data_for_properties = self.get_relevant_data(batch)

        for single_property in self._properties_funcs:
            prop_name = single_property['name']
            property_values = single_property['method'](data_for_properties)
            _ensure_property_shape(property_values, data_for_properties, prop_name)
            self._properties_results[prop_name].extend(property_values)

    def compute(self, context: Context, dataset_kind: DatasetKind) -> CheckResult:
        """Compute final result."""
        data = context.get_data_by_kind(dataset_kind)
        result = {}
        images = defaultdict(list)

        # The values are in the same order as the batch order, so always keeps the same order in order to access
        # the original sample at this index location
        for name, values in self._properties_results.items():
            # If the property is single value per sample, then wrap the values in list in order to work on fixed
            # structure
            if not isinstance(values[0], list):
                values = [[x] for x in values]

            values_lengths_cumsum = np.cumsum(np.array([len(v) for v in values]))
            values_arr = np.hstack(values).astype(np.float)

            try:
                lower_limit, upper_limit = iqr_outliers_range(values_arr, self.iqr_percentiles, self.iqr_scale)
            except NotEnoughSamplesError:
                result[name] = 'Not enough non-null samples to calculate outliers.'
                continue

            # Get the indices of the outliers
            top_outliers = np.argwhere(values_arr > upper_limit).squeeze(axis=1)
            # Sort the indices of the outliers by the original values
            top_outliers = top_outliers[
                np.apply_along_axis(lambda i, sort_arr=values_arr: sort_arr[i], axis=0, arr=top_outliers).argsort()
            ]

            # Doing the same for bottom outliers
            bottom_outliers = np.argwhere(values_arr < lower_limit).squeeze(axis=1)
            # Sort the indices of the outliers by the original values
            bottom_outliers = bottom_outliers[
                np.apply_along_axis(lambda i, sort_arr=values_arr: sort_arr[i], axis=0, arr=bottom_outliers).argsort()
            ]

            # Take the indices to show images from the top and bottom
            show_indices = np.concatenate((bottom_outliers[:self.n_show_top], top_outliers[-self.n_show_top:]))

            # Calculate cumulative sum of the outliers lengths in order to find the correct index of the image
            for outlier_index in show_indices:
                sample_index = _sample_index_from_flatten_index(values_lengths_cumsum, outlier_index)
                value = values_arr[outlier_index].item()
                # To get the value index inside the properties list of a single sample we take the sum of values
                # and decrease the current outlier index. Then we get the value index from the end of the sample list.
                index_of_value_in_sample = (values_lengths_cumsum[sample_index] - outlier_index) * -1
                num_properties_in_sample = len(values[sample_index])

                if data.has_images:
                    image = self.draw_image(data, sample_index, index_of_value_in_sample, num_properties_in_sample)
                    image_thumbnail = prepare_thumbnail(
                        image=image,
                        size=(200, 200),
                        copy_image=False
                    )
                else:
                    image_thumbnail = '<p>Image unavailable</p>'
                images[name].append((value, image_thumbnail))

            # Calculate for all outliers the image index
            image_outliers = [_sample_index_from_flatten_index(values_lengths_cumsum, outlier_index) for
                              outlier_index in np.concatenate((bottom_outliers, top_outliers))]

            result[name] = {
                'indices': data.to_dataset_index(*image_outliers),
                # For the upper and lower limits doesn't show values that are smaller/larger than the actual values
                # we have in the data
                'lower_limit': max(lower_limit, min(values_arr)),
                'upper_limit': min(upper_limit, max(values_arr)),
            }

        # Create display
        display = []
        for property_name, info in result.items():
            # If info is string it means there was error
            if isinstance(info, str):
                html = NO_IMAGES_TEMPLATE.format(prop_name=property_name, message=info)
            elif len(info['indices']) == 0:
                html = NO_IMAGES_TEMPLATE.format(prop_name=property_name, message='No outliers found.')
            else:
                values_combine = ''.join([f'<p>{format_number(x[0])}</p>' for x in images[property_name]])
                images_combine = ''.join([x[1] for x in images[property_name]])

                html = HTML_TEMPLATE.format(
                    prop_name=property_name,
                    values=values_combine,
                    images=images_combine,
                    count=len(info['indices']),
                    n_of_images=len(images[property_name]),
                    lower_limit=format_number(info['lower_limit']),
                    upper_limit=format_number(info['upper_limit'])
                )

            display.append(html)

        return CheckResult(result, display=''.join(display))

    @abstractmethod
    def get_relevant_data(self, batch: Batch):
        """Get the data on which the check calculates outliers."""
        pass

    @abstractmethod
    def draw_image(self, data: VisionData, sample_index: int, index_of_value_in_sample: int,
                   num_properties_in_sample: int) -> np.ndarray:
        """Return an image to show as output of the display.

        Parameters
        ----------
        data : VisionData
            The vision data object used in the check.
        sample_index : int
            The batch index of the sample to draw the image for.
        index_of_value_in_sample : int
            Each sample property is list, then this is the index of the outlier in the sample property list.
        num_properties_in_sample
            The number of values in the sample's property list.
        """
        pass

    @abstractmethod
    def get_default_properties(self, data: VisionData):
        """Return default properties to run in the check."""
        pass


NO_IMAGES_TEMPLATE = """
<h3><b>Property "{prop_name}"</b></h3>
<div>{message}</div>
"""

HTML_TEMPLATE = """
<h3><b>Property "{prop_name}"</b></h3>
<div>
Total number of outliers: {count}
</div>
<div>
Non-outliers range: {lower_limit} to {upper_limit}
</div>
<h4>Samples</h4>
<div
    style="
        overflow-x: auto;
        display: grid;
        grid-template-rows: auto 1fr 1fr;
        grid-template-columns: auto repeat({n_of_images}, 1fr);
        grid-gap: 1.5rem;
        justify-items: center;
        align-items: center;
        padding: 2rem;
        width: max-content;">
    <h5>{prop_name}</h5>
    {values}
    <h5>Image</h5>
    {images}
</div>
"""


def _ensure_property_shape(property_values, data, prop_name):
    """Validate the result of the property."""
    if len(property_values) != len(data):
        raise DeepchecksProcessError(f'Properties are expected to return value per image but instead got'
                                     f' {len(property_values)} values for {len(data)} images for property '
                                     f'{prop_name}')

    # If the first item is list validate all items are list of numbers
    if isinstance(property_values[0], t.Sequence):
        if any((not isinstance(x, t.Sequence) for x in property_values)):
            raise DeepchecksProcessError(f'Property result is expected to be either all lists or all scalars but'
                                         f' got mix for property {prop_name}')
        if any((not _is_list_of_numbers(x) for x in property_values)):
            raise DeepchecksProcessError(f'For outliers, properties are expected to be only numeric types but'
                                         f' found non-numeric value for property {prop_name}')
    # If first value is not list, validate all items are numeric
    elif not _is_list_of_numbers(property_values):
        raise DeepchecksProcessError(f'For outliers, properties are expected to be only numeric types but'
                                     f' found non-numeric value for property {prop_name}')


def _is_list_of_numbers(l):
    return not any(i is not None and not isinstance(i, Number) for i in l)


def _sample_index_from_flatten_index(cumsum_lengths, flatten_index) -> int:
    # The cumulative sum lengths is holding the cumulative sum of properties per image, so the first index which value
    # is greater than the flatten index, is the image index.
    # for example if the sums lengths is [1, 6, 11, 13, 16, 20] and the flatten index = 6, it means this property
    # belong to the third image which is index = 2.
    return np.argwhere(cumsum_lengths > flatten_index)[0][0]
