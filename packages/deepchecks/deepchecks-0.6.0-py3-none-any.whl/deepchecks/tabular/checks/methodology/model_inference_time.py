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
"""The model inference time check module."""
import typing as t
import timeit

import numpy as np

from deepchecks.core.condition import ConditionCategory
from deepchecks.tabular import Context, SingleDatasetCheck
from deepchecks.core import CheckResult, ConditionResult
from deepchecks.core.errors import DeepchecksValueError
from deepchecks.utils.strings import format_number


__all__ = ['ModelInferenceTime']


MI = t.TypeVar('MI', bound='ModelInferenceTime')


class ModelInferenceTime(SingleDatasetCheck):
    """Measure model average inference time (in seconds) per sample.

    Parameters
    ----------
    n_samples : int , default: 1000
        number of samples to use for inference, but if actual
        dataset is smaller then all samples will be used
    """

    def __init__(self, n_samples: int = 1000, **kwargs):
        super().__init__(**kwargs)
        self.n_samples = n_samples
        if n_samples == 0 or n_samples < 0:
            raise DeepchecksValueError('n_samples cannot be le than 0!')

    def run_logic(self, context: Context, dataset_type: str = 'train') -> CheckResult:
        """Run check.

        Returns
        -------
        CheckResult
            value is of the type 'float' .

        Raises
        ------
        DeepchecksValueError
            If the test dataset is not a 'Dataset' instance with a label or
            if 'model' is not a scikit-learn-compatible fitted estimator instance.
        """
        if dataset_type == 'train':
            dataset = context.train
        else:
            dataset = context.test

        model = context.model
        df = dataset.features_columns

        prediction_method = model.predict  # type: ignore

        n_samples = len(df) if len(df) < self.n_samples else self.n_samples
        df = df.sample(n=n_samples, random_state=np.random.randint(n_samples))

        result = timeit.timeit(
            'predict(*args)',
            globals={'predict': prediction_method, 'args': (df,)},
            number=1
        )

        result = result / n_samples

        return CheckResult(value=result, display=(
            'Average model inference time for one sample (in seconds): '
            f'{format_number(result, floating_point=8)}'
        ))

    def add_condition_inference_time_is_not_greater_than(self: MI, value: float = 0.001) -> MI:
        """Add condition - checking that the average model inference time (in seconds) per sample is not greater than X.

        Parameters
        ----------
        value : float , default: 0.001
            condition threshold.
        Returns
        -------
        MI
        """
        def condition(avarage_time: float) -> ConditionResult:
            if avarage_time >= value:
                return ConditionResult(ConditionCategory.FAIL, details=(
                    'Found average inference time (in seconds) above threshold: '
                    f'{format_number(avarage_time, floating_point=8)}'
                ))
            else:
                return ConditionResult(ConditionCategory.PASS)

        return self.add_condition(condition_func=condition, name=(
            'Average model inference time for one sample is not '
            f'greater than {format_number(value, floating_point=8)}'
        ))
