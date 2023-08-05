# ----------------------------------------------------------------------------
# Copyright (C) 2021 Deepchecks (https://www.deepchecks.com)
#
# This file is part of Deepchecks.
# Deepchecks is distributed under the terms of the GNU Affero General
# Public License (version 3 or later).
# You should have received a copy of the GNU Affero General Public License
# along with Deepchecks.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------------
#
"""Module of segment performance check."""
import math
import typing as t
from collections import defaultdict, Counter

import numpy as np
import pandas as pd
import torch
from ignite.metrics import Metric
import plotly.express as px

from deepchecks import ConditionResult
from deepchecks.core import DatasetKind, CheckResult
from deepchecks.core.condition import ConditionCategory
from deepchecks.utils import plot
from deepchecks.utils.strings import format_number, format_percent
from deepchecks.vision import SingleDatasetCheck, Context, Batch
from deepchecks.vision.utils.image_properties import default_image_properties, validate_properties
from deepchecks.vision.metrics_utils import get_scorers_list, metric_results_to_df


__all__ = ['ImageSegmentPerformance']


class ImageSegmentPerformance(SingleDatasetCheck):
    """Segment the data by various properties of the image, and compare the performance of the segments.

    Parameters
    ----------
    image_properties : List[Dict[str, Any]], default: None
        List of properties. Replaces the default deepchecks properties.
        Each property is dictionary with keys 'name' (str), 'method' (Callable) and 'output_type' (str),
        representing attributes of said method. 'output_type' must be one of 'continuous'/'discrete'
    alternative_metrics : Dict[str, Metric], default: None
        A dictionary of metrics, where the key is the metric name and the value is an ignite.Metric object whose score
        should be used. If None are given, use the default metrics.
    number_of_bins: int, default : 5
        Maximum number of bins to segment a single property into.
    number_of_samples_to_infer_bins : int, default : 1000
        Minimum number of samples to use to infer the bounds of the segments' bins
    """

    def __init__(
        self,
        image_properties: t.List[t.Dict[str, t.Any]] = None,
        alternative_metrics: t.Optional[t.Dict[str, Metric]] = None,
        number_of_bins: int = 5,
        number_of_samples_to_infer_bins: int = 1000,
        **kwargs
    ):
        super().__init__(**kwargs)
        if image_properties:
            validate_properties(image_properties)
            self.image_properties = image_properties
        else:
            self.image_properties = default_image_properties

        self.alternative_metrics = alternative_metrics
        self.number_of_bins = number_of_bins
        self.number_of_samples_to_infer_bins = number_of_samples_to_infer_bins
        self._state = None

    def initialize_run(self, context: Context, dataset_kind: DatasetKind):
        """Initialize run before starting updating on batches."""
        # First we will aggregate samples up to defined amount (number_of_samples_to_infer_bins), when we reach
        # the amount we will define the bins and populate them
        self._state = {'samples_for_binning': [], 'bins': None}

    def update(self, context: Context, batch: Batch, dataset_kind: DatasetKind):
        """Update the bins by the image properties."""
        dataset = context.get_data_by_kind(dataset_kind)
        images = batch.images
        predictions = batch.predictions
        labels = batch.labels

        samples_for_bin: t.List = self._state['samples_for_binning']
        bins = self._state['bins']

        # Initialize a list of all properties per image sample
        batch_properties = [{} for _ in range(len(images))]
        for single_property in self.image_properties:
            for index, image_result in enumerate(single_property['method'](images)):
                batch_properties[index][single_property['name']] = image_result

        batch_data = zip(labels, predictions, batch_properties)
        # If we already defined bins, add the current data to them
        if bins is not None:
            _divide_to_bins(bins, list(batch_data))
        else:
            # Add the current data to the samples list
            samples_for_bin.extend(batch_data)
            # Check if enough data to infer bins
            if len(samples_for_bin) >= self.number_of_samples_to_infer_bins:
                # Create the bins and metrics, and divide all cached data into the bins
                self._state['bins'] = self._create_bins_and_metrics(samples_for_bin, dataset)
                # Remove the samples cache which are no longer needed (free the memory)
                del samples_for_bin

    def compute(self, context: Context, dataset_kind: DatasetKind) -> CheckResult:
        """Calculate segment performance based on image properties.

        Returns
        -------
        CheckResult
            value: dictionary containing performance for each property segments
            display: plots of results
        """
        dataset = context.get_data_by_kind(dataset_kind)
        # In case there are fewer samples than 'number_of_samples_to_infer_bins' then bins were not calculated
        if self._state['bins'] is None:
            # Create the bins and metrics
            bins = self._create_bins_and_metrics(self._state['samples_for_binning'], dataset)
        else:
            bins = self._state['bins']

        # bins are in format:
        # {property_name: [{start: val, stop: val, count: x, metrics: {name: metric...}}, ...], ...}
        display_data = []
        result_value = defaultdict(list)

        for property_name, prop_bins in bins.items():
            # Calculate scale for the numbers formatting in the display of range
            bins_scale = max([_get_range_scale(b['start'], b['stop']) for b in prop_bins])
            for single_bin in prop_bins:
                # If we have a low number of unique values for a property, the first bin (-inf, x) might be empty so
                # check the count, and if empty filter out the bin
                if single_bin['count'] == 0:
                    continue

                display_range = _range_string(single_bin['start'], single_bin['stop'], bins_scale)
                bin_data = {
                    'Range': display_range,
                    'Number of samples': single_bin['count'],
                    'Property': f'{property_name}'
                }
                # Update the metrics and range in the single bin from the metrics objects to metric mean results,
                # in order to return the bins object as the check result value
                single_bin['metrics'] = _calculate_metrics(single_bin['metrics'], dataset)
                single_bin['display_range'] = display_range
                # For the plotly display need row per metric in the dataframe
                for metric, val in single_bin['metrics'].items():
                    display_data.append({'Metric': metric, 'Value': val, **bin_data})
                # Save for result
                result_value[property_name].append(single_bin)

        display_df = pd.DataFrame(display_data)

        fig = px.bar(
            display_df,
            x='Range',
            y='Value',
            color='Metric',
            color_discrete_sequence=plot.metric_colors,
            barmode='group',
            facet_col='Property',
            facet_row='Metric',
            facet_col_spacing=0.05,
            facet_row_spacing=0.05,
            hover_data=['Number of samples']
        )

        bar_width = 0.2
        (fig.update_xaxes(title=None, type='category', matches=None)
            .update_yaxes(title=None)
            .for_each_annotation(lambda a: a.update(text=a.text.split('=')[-1]))
            .for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
            .update_traces(width=bar_width)
         )

        return CheckResult(value=dict(result_value), display=fig)

    def _create_bins_and_metrics(self, batch_data: t.List[t.Tuple], dataset):
        """Return dict of bins for each property in format \
        {property_name: [{start: val, stop: val, count: x, metrics: {name: metric...}}, ...], ...}."""
        # For X bins we need to have (X - 1) quantile bounds (open bounds from left and right)
        quantiles = np.linspace(1 / self.number_of_bins, 1, self.number_of_bins - 1, endpoint=False)
        # Calculate for each property the quantile values
        batch_properties = [b[2] for b in batch_data]
        df = pd.DataFrame(batch_properties)
        bins = {}
        for prop in df.columns:
            # Filter nan values
            property_col = df[~df[prop].isnull()][prop]
            # If all values of the property are nan, then doesn't display it
            # TODO: how to handle if only some of the values are nan?
            if len(property_col) == 0:
                continue
            # Get quantiles without duplicates
            quantile_values = list(set(df[prop].quantile(quantiles).tolist()))
            bins[prop] = [{'start': start, 'stop': stop, 'count': 0,
                          'metrics': get_scorers_list(dataset, self.alternative_metrics)}
                          for start, stop in _create_open_bins_ranges(quantile_values)]

        # Divide the data into the bins
        _divide_to_bins(bins, batch_data)
        return bins

    def add_condition_score_from_mean_ratio_not_less_than(self, ratio=0.8):
        """Calculate for each property & metric the mean score and compares ratio between the lowest segment score and\
        the mean score.

        Parameters
        ----------
        ratio : float, default : 0.8
           Threshold of minimal ratio allowed between the lowest segment score of a property and the mean score.
        """
        def condition(result):
            failed_props = {}
            for prop_name, prop_bins in result.items():
                # prop bins is a list of:
                # [{count: int, start: float, stop: float, display_range: str, metrics: {name_1: float,...}}, ...]
                total_score = Counter()
                for b in prop_bins:
                    total_score.update(b['metrics'])
                mean_scores = {metric: score / len(prop_bins) for metric, score in total_score.items()}

                # Take the lowest score for each metric
                min_scores = []
                for metric in mean_scores:
                    min_metric_bin = sorted(prop_bins, key=lambda b, m=metric: b['metrics'][m])[0]
                    if mean_scores[metric] == 0:
                        if min_metric_bin['metrics'][metric] == 0:
                            min_ratio = 0
                        else:
                            min_ratio = np.inf if min_metric_bin['metrics'][metric] > 0 else -np.inf
                    else:
                        min_ratio = min_metric_bin['metrics'][metric] / mean_scores[metric]
                    # Only if below threshold add to list
                    if min_ratio < ratio:
                        min_scores.append({'Range': min_metric_bin['display_range'],
                                           'Metric': metric,
                                           'Ratio': round(min_ratio, 2)})
                # Take the lowest ratio between the failed metrics
                if min_scores:
                    absolutely_min_bin = sorted(min_scores, key=lambda b: b['Ratio'])[0]
                    failed_props[prop_name] = absolutely_min_bin

            if not failed_props:
                return ConditionResult(ConditionCategory.PASS)
            else:
                props = ', '.join(sorted([f'{p}: {m}' for p, m in failed_props.items()]))
                msg = f'Properties with failed segments: {props}'
                return ConditionResult(ConditionCategory.FAIL, details=msg)

        name = f'No segment with ratio between score to mean less than {format_percent(ratio)}'
        return self.add_condition(name, condition)


def _divide_to_bins(bins, batch_data: t.List[t.Tuple]):
    """Iterate the data and enter it into the appropriate bins."""
    for property_name, bins_values in bins.items():
        for label, prediction, properties in batch_data:
            _add_to_fitting_bin(bins_values, properties[property_name], label, prediction)


def _create_open_bins_ranges(quantiles):
    """Return quantiles with start and stop as list of tuples [(-Inf, x1),(x1,x2),(x2, Inf)]."""
    quantiles = sorted(quantiles)
    return zip(([-np.Inf] + quantiles), (quantiles + [np.Inf]))


def _add_to_fitting_bin(bins: t.List[t.Dict], property_value, label, prediction):
    """Find the fitting bin from the list of bins for a given value. Then increase the count and the prediction and \
    label to the metrics objects."""
    if property_value is None:
        return
    for single_bin in bins:
        if single_bin['start'] <= property_value < single_bin['stop']:
            single_bin['count'] += 1
            for metric in single_bin['metrics'].values():
                # Since this is a single prediction and label need to wrap in tensor
                metric.update((torch.unsqueeze(prediction, 0), torch.unsqueeze(label, 0)))
            return


def _range_string(start, stop, precision):
    start = '[' + format_number(start, precision) if not np.isinf(start) else '(-inf'
    stop = format_number(stop, precision) if not np.isinf(stop) else 'inf'
    return f'{start}, {stop})'


def _calculate_metrics(metrics, dataset):
    metrics_df = metric_results_to_df(
        {k: m.compute() for k, m in metrics.items()}, dataset
    )
    metrics_df = metrics_df[['Metric', 'Value']].groupby(['Metric']).median()
    return metrics_df.to_dict()['Value']


def _get_range_scale(start, stop):
    if np.isinf(start) or np.isinf(stop):
        return 2
    number = stop - start
    # Get the scale of number. if between 0 and 1, gets the number of zeros digits right to decimal point (up to
    # non-zero digit)
    scale = -int(math.log10(number))
    # If the number is larger than 1, -scale will be negative, so we will get 2. if the number is smaller than 0.001
    # then -scale will be 2 or larger (add 1 to set larger precision than the scale)
    return max(2, scale + 1)
