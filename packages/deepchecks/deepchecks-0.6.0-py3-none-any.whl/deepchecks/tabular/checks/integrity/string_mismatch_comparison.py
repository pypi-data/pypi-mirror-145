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
"""String mismatch functions."""
from collections import defaultdict
from typing import Union, List

import pandas as pd

from deepchecks.core import CheckResult, ConditionResult, ConditionCategory
from deepchecks.tabular import Context, TrainTestCheck
from deepchecks.utils.dataframes import select_from_dataframe
from deepchecks.utils.features import N_TOP_MESSAGE, column_importance_sorter_df
from deepchecks.utils.typing import Hashable
from deepchecks.utils.strings import (
    get_base_form_to_variants_dict,
    is_string_column,
    format_percent,
)


__all__ = ['StringMismatchComparison']


class StringMismatchComparison(TrainTestCheck):
    """Detect different variants of string categories between the same categorical column in two datasets.

    This check compares the same categorical column within a dataset and baseline and checks whether there are
    variants of similar strings that exists only in dataset and not in baseline.
    Specifically, we define similarity between strings if they are equal when ignoring case and non-letter
    characters.
    Example:
    We have a train dataset with similar strings 'string' and 'St. Ring', which have different meanings.
    Our tested dataset has the strings 'string', 'St. Ring' and a new phrase, 'st.  ring'.
    Here, we have a new variant of the above strings, and would like to be acknowledged, as this is obviously a
    different version of 'St. Ring'.

    Parameters
    ----------
    columns : Union[Hashable, List[Hashable]] , default: None
        Columns to check, if none are given checks all columns except ignored ones.
    ignore_columns : Union[Hashable, List[Hashable]] , default: None
        Columns to ignore, if none given checks based on columns variable
    n_top_columns : int , optional
        amount of columns to show ordered by feature importance (date, index, label are first)
    """

    def __init__(
        self,
        columns: Union[Hashable, List[Hashable], None] = None,
        ignore_columns: Union[Hashable, List[Hashable], None] = None,
        n_top_columns: int = 10,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.columns = columns
        self.ignore_columns = ignore_columns
        self.n_top_columns = n_top_columns

    def run_logic(self, context: Context) -> CheckResult:
        """Run check.

        Returns
        -------
        CheckResult
            with value of type dict that contains detected different variants of string
        """
        # Validate parameters
        df = context.test.data
        df = select_from_dataframe(df, self.columns, self.ignore_columns)
        baseline_df = context.train.data

        display_mismatches = []
        result_dict = defaultdict(dict)

        # Get shared columns
        columns = set(df.columns).intersection(baseline_df.columns)

        for column_name in columns:
            tested_column: pd.Series = df[column_name]
            baseline_column: pd.Series = baseline_df[column_name]
            # If one of the columns isn't string type, continue
            if not is_string_column(tested_column) or not is_string_column(baseline_column):
                continue

            tested_baseforms = get_base_form_to_variants_dict(tested_column.unique())
            baseline_baseforms = get_base_form_to_variants_dict(baseline_column.unique())

            common_baseforms = set(tested_baseforms.keys()).intersection(baseline_baseforms.keys())
            for baseform in common_baseforms:
                tested_values = tested_baseforms[baseform]
                baseline_values = baseline_baseforms[baseform]
                # If at least one unique value in tested dataset, add the column to results
                if len(tested_values - baseline_values) > 0:
                    # Calculate all values to be shown
                    variants_only_in_dataset = list(tested_values - baseline_values)
                    variants_only_in_baseline = list(baseline_values - tested_values)
                    common_variants = list(tested_values & baseline_values)
                    percent_variants_only_in_dataset = _percentage_in_series(tested_column, variants_only_in_dataset)
                    percent_variants_in_baseline = _percentage_in_series(baseline_column, variants_only_in_baseline)

                    display_mismatches.append([column_name, baseform, common_variants,
                                               variants_only_in_dataset, percent_variants_only_in_dataset[1],
                                               variants_only_in_baseline, percent_variants_in_baseline[1]])
                    result_dict[column_name][baseform] = {
                        'commons': common_variants, 'variants_only_in_test': variants_only_in_dataset,
                        'variants_only_in_train': variants_only_in_baseline,
                        'percent_variants_only_in_test': percent_variants_only_in_dataset[0],
                        'percent_variants_in_train': percent_variants_in_baseline[0]
                    }

        # Create result dataframe
        if display_mismatches:
            df_graph = pd.DataFrame(display_mismatches,
                                    columns=['Column name', 'Base form', 'Common variants', 'Variants only in test',
                                             '% Unique variants out of all dataset samples (count)',
                                             'Variants only in train',
                                             '% Unique variants out of all baseline samples (count)'])
            df_graph = df_graph.set_index(['Column name', 'Base form'])

            df_graph = column_importance_sorter_df(
                df_graph,
                context.test,
                context.features_importance,
                self.n_top_columns,
                col='Column name'
            )
            # For display transpose the dataframe
            display = [N_TOP_MESSAGE % self.n_top_columns, df_graph.T]
        else:
            display = None

        return CheckResult(result_dict, display=display)

    def add_condition_no_new_variants(self):
        """Add condition - no new variants allowed in test data."""
        name = 'No new variants allowed in test data'
        return self.add_condition(name, _condition_percent_limit, ratio=0)

    def add_condition_ratio_new_variants_not_greater_than(self, ratio: float):
        """Add condition - no new variants allowed above given percentage in test data.

        Parameters
        ----------
        ratio : float
            Max percentage of new variants in test data allowed.
        """
        name = f'Ratio of new variants in test data is not greater than {format_percent(ratio)}'
        return self.add_condition(name, _condition_percent_limit, ratio=ratio)


def _condition_percent_limit(result, ratio: float):
    not_passing_columns = {}
    for col, baseforms in result.items():
        sum_percent = 0
        for info in baseforms.values():
            sum_percent += info['percent_variants_only_in_test']
        if sum_percent > ratio:
            not_passing_columns[col] = format_percent(sum_percent)

    if not_passing_columns:
        details = f'Found columns with ratio of variants above threshold: {not_passing_columns}'
        return ConditionResult(ConditionCategory.FAIL, details)
    return ConditionResult(ConditionCategory.PASS)


def _percentage_in_series(series, values):
    count = sum(series.isin(values))
    percent = count / series.size
    return percent, f'{format_percent(percent)} ({count})'
