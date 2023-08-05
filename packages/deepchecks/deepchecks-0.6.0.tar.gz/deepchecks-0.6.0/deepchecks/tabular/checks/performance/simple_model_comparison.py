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
"""Module containing simple comparison check."""
from collections import defaultdict
from typing import Callable, Dict, Hashable, List

import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.dummy import DummyRegressor, DummyClassifier
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

from deepchecks.core import CheckResult, ConditionResult
from deepchecks.core.condition import ConditionCategory
from deepchecks.core.errors import DeepchecksValueError
from deepchecks.tabular import Context, TrainTestCheck, Dataset
from deepchecks.utils.distribution.preprocessing import ScaledNumerics
from deepchecks.utils.strings import format_percent
from deepchecks.utils.metrics import ModelType, get_gain
from deepchecks.utils.simple_models import RandomModel


__all__ = ['SimpleModelComparison']


class SimpleModelComparison(TrainTestCheck):
    """Compare given model score to simple model score (according to given model type).

    Parameters
    ----------
    simple_model_type : str , default: constant
        Type of the simple model ['random', 'constant', 'tree'].
        + random - select one of the labels by random.
        + constant - in regression is mean value, in classification the most common value.
        + tree - runs a simple decision tree.
    alternative_scorers : Dict[str, Callable], default None
        An optional dictionary of scorer title to scorer functions/names. If none given, using default scorers.
        For description about scorers see Notes below.
    max_gain : float , default: 50
        the maximum value for the gain value, limits from both sides [-max_gain, max_gain]
    max_depth : int , default: 3
        the max depth of the tree (used only if simple model type is tree).
    random_state : int , default: 42
        the random state (used only if simple model type is tree or random).

    Notes
    -----
    Scorers are a convention of sklearn to evaluate a model.
    `See scorers documentation <https://scikit-learn.org/stable/modules/model_evaluation.html#scoring>`_
    A scorer is a function which accepts (model, X, y_true) and returns a float result which is the score.
    For every scorer higher scores are better than lower scores.

    You can create a scorer out of existing sklearn metrics:

    .. code-block:: python

        from sklearn.metrics import roc_auc_score, make_scorer

        training_labels = [1, 2, 3]
        auc_scorer = make_scorer(roc_auc_score, labels=training_labels, multi_class='ovr')
        # Note that the labels parameter is required for multi-class classification in metrics like roc_auc_score or
        # log_loss that use the predict_proba function of the model, in case that not all labels are present in the test
        # set.

    Or you can implement your own:

    .. code-block:: python

        from sklearn.metrics import make_scorer


        def my_mse(y_true, y_pred):
            return (y_true - y_pred) ** 2


        # Mark greater_is_better=False, since scorers always suppose to return
        # value to maximize.
        my_mse_scorer = make_scorer(my_mse, greater_is_better=False)
    """

    def __init__(
        self,
        simple_model_type: str = 'constant',
        alternative_scorers: Dict[str, Callable] = None,
        max_gain: float = 50,
        max_depth: int = 3,
        random_state: int = 42,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.simple_model_type = simple_model_type
        self.user_scorers = alternative_scorers
        self.max_gain = max_gain
        self.max_depth = max_depth
        self.random_state = random_state

    def run_logic(self, context: Context) -> CheckResult:
        """Run check.

        Returns
        -------
        CheckResult
            value is a Dict of: given_model_score, simple_model_score, ratio <br>
            ratio is given model / simple model (if the scorer returns negative values we divide 1 by it) <br>
            if ratio is infinite max_ratio is returned

        Raises
        ------
        DeepchecksValueError
            If the object is not a Dataset instance.
        """
        train_dataset = context.train
        test_dataset = context.test
        test_label = test_dataset.label_col
        task_type = context.task_type
        model = context.model

        # If user defined scorers used them, else use a single scorer
        if self.user_scorers:
            scorers = context.get_scorers(self.user_scorers, class_avg=False)
        else:
            scorers = [context.get_single_scorer(class_avg=False)]

        simple_model = self._create_simple_model(train_dataset, task_type)

        models = [
            (f'{type(model).__name__} model', 'Origin', model),
            (f'Simple model - {self.simple_model_type}', 'Simple', simple_model)
        ]

        # Multiclass have different return type from the scorer, list of score per class instead of single score
        if task_type in [ModelType.MULTICLASS, ModelType.BINARY]:
            n_samples = test_label.groupby(test_label).count()
            classes = test_dataset.classes

            results_array = []
            # Dict in format { Scorer : Dict { Class : Dict { Origin/Simple : score } } }
            results_dict = {}
            for scorer in scorers:
                model_dict = defaultdict(dict)
                for model_name, model_type, model_instance in models:
                    for class_score, class_value in zip(scorer(model_instance, test_dataset), classes):
                        model_dict[class_value][model_type] = class_score
                        results_array.append([model_name,
                                              model_type,
                                              class_score,
                                              scorer.name,
                                              class_value,
                                              n_samples[class_value]
                                              ])
                results_dict[scorer.name] = model_dict

            results_df = pd.DataFrame(
                results_array,
                columns=['Model', 'Type', 'Value', 'Metric', 'Class', 'Number of samples']
            )

            # Plot the metrics in a graph, grouping by the model and class
            fig = (
                px.histogram(
                    results_df,
                    x=['Class', 'Model'],
                    y='Value',
                    color='Model',
                    barmode='group',
                    facet_col='Metric',
                    facet_col_spacing=0.05,
                    hover_data=['Number of samples'])
                .update_xaxes(title=None, tickprefix='Class ', tickangle=60, type='category')
                .update_yaxes(title=None, matches=None)
                .for_each_annotation(lambda a: a.update(text=a.text.split('=')[-1]))
                .for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
            )

        else:
            classes = None

            results_array = []
            # Dict in format { Scorer : Dict { Origin/Simple : score } }
            results_dict = {}
            for scorer in scorers:
                model_dict = defaultdict(dict)
                for model_name, model_type, model_instance in models:
                    score = scorer(model_instance, test_dataset)
                    model_dict[model_type] = score
                    results_array.append([model_name,
                                          model_type,
                                          score,
                                          scorer.name,
                                          test_label.count()
                                          ])
                results_dict[scorer.name] = model_dict

            results_df = pd.DataFrame(
                results_array,
                columns=['Model', 'Type', 'Value', 'Metric', 'Number of samples']
            )

            # Plot the metrics in a graph, grouping by the model
            fig = (
                px.histogram(
                    results_df,
                    x='Model',
                    y='Value',
                    color='Model',
                    barmode='group',
                    facet_col='Metric',
                    facet_col_spacing=0.05,
                    hover_data=['Number of samples'])
                .update_xaxes(title=None)
                .update_yaxes(title=None, matches=None)
                .for_each_annotation(lambda a: a.update(text=a.text.split('=')[-1]))
                .for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
            )

        # For each scorer calculate perfect score in order to calculate later the ratio in conditions
        scorers_perfect = {scorer.name: scorer.score_perfect(test_dataset) for scorer in scorers}

        return CheckResult({'scores': results_dict,
                            'type': task_type,
                            'scorers_perfect': scorers_perfect,
                            'classes': classes
                            }, display=fig)

    def _create_simple_model(self, train_ds: Dataset, task_type: ModelType):
        """Create a simple model of given type (random/constant/tree) to the given dataset.

        Parameters
        ----------
        train_ds : Dataset
            The training dataset object.
        task_type : ModelType
            the model type.

        Returns
        -------
        object
            Classifier Object

        Raises
        ------
        NotImplementedError
            If the simple_model_type is not supported
        """
        np.random.seed(self.random_state)

        if self.simple_model_type == 'random':
            simple_model = RandomModel()

        elif self.simple_model_type == 'constant':
            if task_type == ModelType.REGRESSION:
                simple_model = DummyRegressor(strategy='mean')
            elif task_type in {ModelType.BINARY, ModelType.MULTICLASS}:
                simple_model = DummyClassifier(strategy='most_frequent')
            else:
                raise DeepchecksValueError(f'Unknown task type - {task_type}')
        elif self.simple_model_type == 'tree':
            if task_type == ModelType.REGRESSION:
                clf = DecisionTreeRegressor(
                    max_depth=self.max_depth,
                    random_state=self.random_state
                )
            elif task_type in {ModelType.BINARY, ModelType.MULTICLASS}:
                clf = DecisionTreeClassifier(
                    max_depth=self.max_depth,
                    random_state=self.random_state,
                    class_weight='balanced'
                )
            else:
                raise DeepchecksValueError(f'Unknown task type - {task_type}')

            simple_model = Pipeline([('scaler', ScaledNumerics(train_ds.cat_features, max_num_categories=10)),
                                     ('tree-model', clf)])
        else:
            raise DeepchecksValueError(
                f'Unknown model type - {self.simple_model_type}, expected to be one of '
                f"['random', 'constant', 'tree'] "
                f"but instead got {self.simple_model_type}"  # pylint: disable=inconsistent-quotes
            )

        simple_model.fit(train_ds.data[train_ds.features], train_ds.data[train_ds.label_name])
        return simple_model

    def add_condition_gain_not_less_than(self,
                                         min_allowed_gain: float = 0.1,
                                         classes: List[Hashable] = None,
                                         average: bool = False):
        """Add condition - require minimum allowed gain between the model and the simple model.

        Parameters
        ----------
        min_allowed_gain : float , default: 0.1
            Minimum allowed gain between the model and the simple model -
            gain is: difference in performance / (perfect score - simple score)
        classes : List[Hashable] , default: None
            Used in classification models to limit condition only to given classes.
        average : bool , default: False
            Used in classification models to flag if to run condition on average of classes, or on
            each class individually
        """
        name = f'Model performance gain over simple model is not less than {format_percent(min_allowed_gain)}'
        if classes:
            name = name + f' for classes {str(classes)}'
        return self.add_condition(name,
                                  condition,
                                  include_classes=classes,
                                  min_allowed_gain=min_allowed_gain,
                                  max_gain=self.max_gain,
                                  average=average)


def condition(result: Dict, include_classes=None, average=False, max_gain=None, min_allowed_gain=0) -> ConditionResult:
    scores = result['scores']
    task_type = result['type']
    scorers_perfect = result['scorers_perfect']

    fails = {}
    if task_type in [ModelType.MULTICLASS, ModelType.BINARY] and not average:
        for metric, classes_scores in scores.items():
            failed_classes = {}
            for clas, models_scores in classes_scores.items():
                # Skip if class is not in class list
                if include_classes is not None and clas not in include_classes:
                    continue

                # If origin model is perfect, skip the gain calculation
                if models_scores['Origin'] == scorers_perfect[metric]:
                    continue

                gain = get_gain(models_scores['Simple'],
                                models_scores['Origin'],
                                scorers_perfect[metric],
                                max_gain)
                if gain < min_allowed_gain:
                    failed_classes[clas] = format_percent(gain)
            if failed_classes:
                fails[metric] = failed_classes
    else:
        if task_type in [ModelType.MULTICLASS, ModelType.BINARY]:
            scores = average_scores(scores, include_classes)
        for metric, models_scores in scores.items():
            # If origin model is perfect, skip the gain calculation
            if models_scores['Origin'] == scorers_perfect[metric]:
                continue
            gain = get_gain(models_scores['Simple'],
                            models_scores['Origin'],
                            scorers_perfect[metric],
                            max_gain)
            if gain < min_allowed_gain:
                fails[metric] = format_percent(gain)

    if fails:
        msg = f'Found metrics with gain below threshold: {fails}'
        return ConditionResult(ConditionCategory.FAIL, msg)
    else:
        return ConditionResult(ConditionCategory.PASS)


def average_scores(scores, include_classes):
    result = {}
    for metric, classes_scores in scores.items():
        origin_score = 0
        simple_score = 0
        total = 0
        for clas, models_scores in classes_scores.items():
            # Skip if class is not in class list
            if include_classes is not None and clas not in include_classes:
                continue
            origin_score += models_scores['Origin']
            simple_score += models_scores['Simple']
            total += 1

        result[metric] = {
            'Origin': origin_score / total,
            'Simple': simple_score / total
         }
    return result
