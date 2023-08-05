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
"""Module containing all data distribution checks."""
from .train_test_feature_drift import TrainTestFeatureDrift
from .whole_dataset_drift import WholeDatasetDrift
from .train_test_label_drift import TrainTestLabelDrift
from .train_test_prediction_drift import TrainTestPredictionDrift


__all__ = [
    'TrainTestFeatureDrift',
    'WholeDatasetDrift',
    'TrainTestLabelDrift',
    'TrainTestPredictionDrift'
]
