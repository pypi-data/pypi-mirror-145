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
"""Package for tabular functionality."""
from .dataset import Dataset
from .context import Context
from .suite import Suite
from .base_checks import (
    SingleDatasetCheck,
    TrainTestCheck,
    ModelOnlyCheck,
    ModelComparisonCheck,
)
from .model_base import (
    ModelComparisonContext,
    ModelComparisonSuite
)

__all__ = [
    "Dataset",
    "Context",
    "SingleDatasetCheck",
    "TrainTestCheck",
    "ModelOnlyCheck",
    "Suite",
    "ModelComparisonContext",
    "ModelComparisonCheck",
    "ModelComparisonSuite",
]
