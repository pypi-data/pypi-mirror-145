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
"""The dataset module containing the tabular Dataset class and its functions."""
# pylint: disable=inconsistent-quotes,protected-access
import typing as t
import logging
from functools import lru_cache

import numpy as np
import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype
from sklearn.model_selection import train_test_split

from deepchecks.utils.dataframes import select_from_dataframe
from deepchecks.utils.features import infer_numerical_features, is_categorical, infer_categorical_features
from deepchecks.utils.typing import Hashable
from deepchecks.core.errors import DeepchecksValueError, DatasetValidationError, DeepchecksNotSupportedError


__all__ = ['Dataset']


logger = logging.getLogger('deepchecks.dataset')
TDataset = t.TypeVar('TDataset', bound='Dataset')


class Dataset:
    """
    Dataset wraps pandas DataFrame together with ML related metadata.

    The Dataset class is containing additional data and methods intended for easily accessing
    metadata relevant for the training or validating of an ML models.

    Parameters
    ----------
    df : pd.DataFrame
        A pandas DataFrame containing data relevant for the training or validating of a ML models.
    label : t.Union[Hashable, pd.Series, pd.DataFrame, np.ndarray] , default: None
        label column provided either as a string with the name of an existing column in the DataFrame or a label
        object including the label data (pandas Series/DataFrame or a numpy array) that will be concatenated to the
        data in the DataFrame. in case of label data the following logic is applied to set the label name:
        - Series: takes the series name or 'target' if name is empty
        - DataFrame: expect single column in the dataframe and use its name
        - numpy: use 'target'
    features : t.Optional[t.Sequence[Hashable]] , default: None
        List of names for the feature columns in the DataFrame.
    cat_features : t.Optional[t.Sequence[Hashable]] , default: None
        List of names for the categorical features in the DataFrame. In order to disable categorical.
        features inference, pass cat_features=[]
    index_name : t.Optional[Hashable] , default: None
        Name of the index column in the dataframe. If set_index_from_dataframe_index is True and index_name
        is not None, index will be created from the dataframe index level with the given name. If index levels
        have no names, an int must be used to select the appropriate level by order.
    set_index_from_dataframe_index : bool , default: False
        If set to true, index will be created from the dataframe index instead of dataframe columns (default).
        If index_name is None, first level of the index will be used in case of a multilevel index.
    datetime_name : t.Optional[Hashable] , default: None
        Name of the datetime column in the dataframe. If set_datetime_from_dataframe_index is True and datetime_name
        is not None, date will be created from the dataframe index level with the given name. If index levels
        have no names, an int must be used to select the appropriate level by order.
    set_datetime_from_dataframe_index : bool , default: False
        If set to true, date will be created from the dataframe index instead of dataframe columns (default).
        If datetime_name is None, first level of the index will be used in case of a multilevel index.
    convert_datetime : bool , default: True
        If set to true, date will be converted to datetime using pandas.to_datetime.
    datetime_args : t.Optional[t.Dict] , default: None
        pandas.to_datetime args used for conversion of the datetime column.
        (look at https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html for more documentation)
    max_categorical_ratio : float , default: 0.01
        The max ratio of unique values in a column in order for it to be inferred as a
        categorical feature.
    max_categories : int , default: 30
        The maximum number of categories in a column in order for it to be inferred as a categorical
        feature.
    max_float_categories : int , default: 5
        The maximum number of categories in a float column in order for it to be inferred as a
        categorical feature.
    label_type : str , default: None
        Used to assume target model type if not found on model. Values ('classification_label', 'regression_label')
        If None then label type is inferred from label using is_categorical logic.
    """

    _features: t.List[Hashable]
    _label_name: t.Optional[Hashable]
    _index_name: t.Optional[Hashable]
    _set_index_from_dataframe_index: t.Optional[bool]
    _datetime_name: t.Optional[Hashable]
    _set_datetime_from_dataframe_index: t.Optional[bool]
    _datetime_column: t.Optional[pd.Series]
    _cat_features: t.List[Hashable]
    _data: pd.DataFrame
    _max_categorical_ratio: float
    _max_categories: int
    _label_type: t.Optional[str]

    def __init__(
            self,
            df: pd.DataFrame,
            label: t.Union[Hashable, pd.Series, pd.DataFrame, np.ndarray] = None,
            features: t.Optional[t.Sequence[Hashable]] = None,
            cat_features: t.Optional[t.Sequence[Hashable]] = None,
            index_name: t.Optional[Hashable] = None,
            set_index_from_dataframe_index: bool = False,
            datetime_name: t.Optional[Hashable] = None,
            set_datetime_from_dataframe_index: bool = False,
            convert_datetime: bool = True,
            datetime_args: t.Optional[t.Dict] = None,
            max_categorical_ratio: float = 0.01,
            max_categories: int = 30,
            max_float_categories: int = 5,
            label_type: str = None
    ):

        self._data = df.copy()

        # Validations
        if label is None:
            label_name = None
        elif isinstance(label, (pd.Series, pd.DataFrame, np.ndarray)):
            label_name = None
            if isinstance(label, pd.Series):
                # Set label name if exists
                if label.name is not None:
                    label_name = label.name
                    if label_name in self._data.columns:
                        raise DeepchecksValueError(f'Data has column with name "{label_name}", use pandas rename to'
                                                   f' change label name or remove the column from the dataframe')
            elif isinstance(label, pd.DataFrame):
                # Validate shape
                if label.shape[1] > 1:
                    raise DeepchecksValueError('Label must have a single column')
                # Set label name
                label_name = label.columns[0]
                label = label[label_name]
                if label_name in self._data.columns:
                    raise DeepchecksValueError(f'Data has column with name "{label_name}", change label column '
                                               f'or remove the column from the data dataframe')
            elif isinstance(label, np.ndarray):
                # Validate label shape
                if len(label.shape) > 2:
                    raise DeepchecksValueError('Label must be either column vector or row vector')
                elif len(label.shape) == 2:
                    if all(x != 1 for x in label.shape):
                        raise DeepchecksValueError('Label must be either column vector or row vector')
                    label = np.squeeze(label)

            # Validate length of label
            if label.shape[0] != self._data.shape[0]:
                raise DeepchecksValueError('Number of samples of label and data must be equal')

            # If no label found to set, then set default name
            if label_name is None:
                label_name = 'target'
                if label_name in self._data.columns:
                    raise DeepchecksValueError('Can\'t set default label name "target" since it already exists in '
                                               'the dataframe. use pandas name parameter to give the label a '
                                               'unique name')
            # Set label data in dataframe
            if isinstance(label, pd.Series):
                pd.testing.assert_index_equal(self._data.index, label.index)
                self._data[label_name] = label
            else:
                self._data[label_name] = np.array(label).reshape(-1, 1)
        elif isinstance(label, Hashable):
            label_name = label
            if label_name not in self._data.columns:
                raise DeepchecksValueError(f'label column {label_name} not found in dataset columns')
        else:
            raise DeepchecksValueError(f'Unsupported type for label: {type(label).__name__}')

        # Assert that the requested index can be found
        if not set_index_from_dataframe_index:
            if index_name is not None and index_name not in self._data.columns:
                error_message = f'Index column {index_name} not found in dataset columns.'
                if index_name == 'index':
                    error_message += ' If you attempted to use the dataframe index, set ' \
                                     'set_index_from_dataframe_index to True instead.'
                raise DeepchecksValueError(error_message)
        else:
            if index_name is not None:
                if isinstance(index_name, str):
                    if index_name not in self._data.index.names:
                        raise DeepchecksValueError(f'Index {index_name} not found in dataframe index level names.')
                elif isinstance(index_name, int):
                    if index_name > (len(self._data.index.names) - 1):
                        raise DeepchecksValueError(f'Dataframe index has less levels than {index_name + 1}.')
                else:
                    raise DeepchecksValueError(f'When set_index_from_dataframe_index is True index_name can be None,'
                                               f' int or str, but found {type(index_name)}')

        # Assert that the requested datetime can be found
        if not set_datetime_from_dataframe_index:
            if datetime_name is not None and datetime_name not in self._data.columns:
                error_message = f'Datetime column {datetime_name} not found in dataset columns.'
                if datetime_name == 'date':
                    error_message += ' If you attempted to use the dataframe index, ' \
                                     'set set_datetime_from_dataframe_index to True instead.'
                raise DeepchecksValueError(error_message)
        else:
            if datetime_name is not None:
                if isinstance(datetime_name, str):
                    if datetime_name not in self._data.index.names:
                        raise DeepchecksValueError(
                            f'Datetime {datetime_name} not found in dataframe index level names.'
                        )
                elif isinstance(datetime_name, int):
                    if datetime_name > (len(self._data.index.names) - 1):
                        raise DeepchecksValueError(f'Dataframe index has less levels than {datetime_name + 1}.')
                else:
                    raise DeepchecksValueError(f'When set_index_from_dataframe_index is True index_name can be None,'
                                               f' int or str, but found {type(index_name)}')
            self._datetime_column = self.get_datetime_column_from_index(datetime_name)

        if features is not None:
            difference = set(features) - set(self._data.columns)
            if len(difference) > 0:
                raise DeepchecksValueError('Features must be names of columns in dataframe. '
                                           f'Features {difference} have not been '
                                           'found in input dataframe.')
            self._features = list(features)
        else:
            self._features = [x for x in self._data.columns if x not in
                              {label_name,
                               index_name if not set_index_from_dataframe_index else None,
                               datetime_name if not set_datetime_from_dataframe_index else None}]

        self._label_name = label_name
        self._index_name = index_name
        self._set_index_from_dataframe_index = set_index_from_dataframe_index
        self._datetime_name = datetime_name
        self._set_datetime_from_dataframe_index = set_datetime_from_dataframe_index
        self._datetime_args = datetime_args or {}

        self._max_categorical_ratio = max_categorical_ratio
        self._max_categories = max_categories
        self._max_float_categories = max_float_categories

        if self._label_name in self.features:
            raise DeepchecksValueError(f'label column {self._label_name} can not be a feature column')

        if self._datetime_name in self.features:
            raise DeepchecksValueError(f'datetime column {self._datetime_name} can not be a feature column')

        if self._index_name in self.features:
            raise DeepchecksValueError(f'index column {self._index_name} can not be a feature column')

        if cat_features is not None:
            if set(cat_features).intersection(set(self._features)) != set(cat_features):
                raise DeepchecksValueError(f'Categorical features must be a subset of features. '
                                           f'Categorical features {set(cat_features) - set(self._features)} '
                                           f'have not been found in feature list.')
            self._cat_features = list(cat_features)
        else:
            self._cat_features = self._infer_categorical_features(
                self._data,
                max_categorical_ratio=max_categorical_ratio,
                max_categories=max_categories,
                max_float_categories=max_float_categories,
                columns=self._features
            )

        if ((self._datetime_name is not None) or self._set_datetime_from_dataframe_index) and convert_datetime:
            if self._set_datetime_from_dataframe_index:
                self._datetime_column = pd.to_datetime(self._datetime_column, **self._datetime_args)
            else:
                self._data[self._datetime_name] = pd.to_datetime(self._data[self._datetime_name], **self._datetime_args)

        if label_type:
            self._label_type = label_type
        elif self._label_name:
            self._label_type = self._infer_label_type(
                self.data[self._label_name],
                max_categorical_ratio=0.05,
                max_categories=max_categories,
                max_float_categories=max_float_categories
            )
        else:
            self._label_type = None

        unassigned_cols = [col for col in self._features if col not in self._cat_features]
        self._numerical_features = infer_numerical_features(self._data[unassigned_cols])

    @classmethod
    def from_numpy(
            cls: t.Type[TDataset],
            *args: np.ndarray,
            columns: t.Sequence[Hashable] = None,
            label_name: t.Hashable = None,
            **kwargs
    ) -> TDataset:
        """Create Dataset instance from numpy arrays.

        Parameters
        ----------
        *args: np.ndarray
            Numpy array of data columns, and second optional numpy array of labels.
        columns : t.Sequence[Hashable] , default: None
            names for the columns. If none provided, the names that will be automatically
            assigned to the columns will be: 1 - n (where n - number of columns)
        label_name : t.Hashable , default: None
            labels column name. If none is provided, the name 'target' will be used.
        **kwargs : Dict
            additional arguments that will be passed to the main Dataset constructor.
        Returns
        -------
        Dataset
            instance of the Dataset
        Raises
        ------
        DeepchecksValueError
            if receives zero or more than two numpy arrays.
            if columns (args[0]) is not two dimensional numpy array.
            if labels (args[1]) is not one dimensional numpy array.
            if features array or labels array is empty.

        Examples
        --------
        >>> import numpy
        >>> from deepchecks.tabular import Dataset

        >>> features = numpy.array([[0.25, 0.3, 0.3],
        ...                        [0.14, 0.75, 0.3],
        ...                        [0.23, 0.39, 0.1]])
        >>> labels = numpy.array([0.1, 0.1, 0.7])
        >>> dataset = Dataset.from_numpy(features, labels)

        Creating dataset only from features array.

        >>> dataset = Dataset.from_numpy(features)

        Passing additional arguments to the main Dataset constructor

        >>> dataset = Dataset.from_numpy(features, labels, max_categorical_ratio=0.5)

        Specifying features and label columns names.

        >>> dataset = Dataset.from_numpy(
        ...     features, labels,
        ...     columns=['sensor-1', 'sensor-2', 'sensor-3'],
        ...     label_name='labels'
        ... )

        """
        if len(args) == 0 or len(args) > 2:
            raise DeepchecksValueError(
                "'from_numpy' constructor expecting to receive two numpy arrays (or at least one)."
                "First array must contains the columns and second the labels."
            )

        columns_array = args[0]
        columns_error_message = (
            "'from_numpy' constructor expecting columns (args[0]) "
            "to be not empty two dimensional array."
        )

        if len(columns_array.shape) != 2:
            raise DeepchecksValueError(columns_error_message)

        if columns_array.shape[0] == 0 or columns_array.shape[1] == 0:
            raise DeepchecksValueError(columns_error_message)

        if columns is not None and len(columns) != columns_array.shape[1]:
            raise DeepchecksValueError(
                f'{columns_array.shape[1]} columns were provided '
                f'but only {len(columns)} name(s) for them`s.'
            )

        elif columns is None:
            columns = [str(index) for index in range(1, columns_array.shape[1] + 1)]

        if len(args) == 1:
            labels_array = None
        else:
            labels_array = args[1]
            if len(labels_array.shape) != 1 or labels_array.shape[0] == 0:
                raise DeepchecksValueError(
                    "'from_numpy' constructor expecting labels (args[1]) "
                    "to be not empty one dimensional array."
                )

            labels_array = pd.Series(labels_array)
            if label_name:
                labels_array = labels_array.rename(label_name)

        return cls(
            df=pd.DataFrame(data=columns_array, columns=columns),
            label=labels_array,
            **kwargs
        )

    @property
    def data(self) -> pd.DataFrame:
        """Return the data of dataset."""
        return self._data

    def copy(self: TDataset, new_data: pd.DataFrame) -> TDataset:
        """Create a copy of this Dataset with new data.

        Parameters
        ----------
        new_data (DataFrame): new data from which new dataset will be created

        Returns
        -------
        Dataset
            new dataset instance
        """
        # Filter out if columns were dropped
        features = [feat for feat in self._features if feat in new_data.columns]
        cat_features = [feat for feat in self.cat_features if feat in new_data.columns]
        label_name = self._label_name if self._label_name in new_data.columns else None
        index = self._index_name if self._index_name in new_data.columns else None
        date = self._datetime_name if self._datetime_name in new_data.columns else None

        cls = type(self)

        return cls(new_data, features=features, cat_features=cat_features, label=label_name,
                   index_name=index, set_index_from_dataframe_index=self._set_index_from_dataframe_index,
                   datetime_name=date, set_datetime_from_dataframe_index=self._set_datetime_from_dataframe_index,
                   convert_datetime=False, max_categorical_ratio=self._max_categorical_ratio,
                   max_categories=self._max_categories, label_type=self.label_type)

    def sample(self: TDataset, n_samples: int, replace: bool = False, random_state: t.Optional[int] = None,
               drop_na_label: bool = False) -> TDataset:
        """Create a copy of the dataset object, with the internal dataframe being a sample of the original dataframe.

        Parameters
        ----------
        n_samples : int
            Number of samples to draw.
        replace : bool, default: False
            Whether to sample with replacement.
        random_state : t.Optional[int] , default None
            Random state.
        drop_na_label : bool, default: False
            Whether to take sample only from rows with exiting label.
        Returns
        -------
        Dataset
            instance of the Dataset with sampled internal dataframe.
        """
        if drop_na_label and self.label_name:
            valid_idx = self.data[self.label_name].notna()
            data_to_sample = self.data[valid_idx]
        else:
            data_to_sample = self.data
        n_samples = min(n_samples, len(data_to_sample))
        return self.copy(data_to_sample.sample(n_samples, replace=replace, random_state=random_state))

    @property
    def n_samples(self) -> int:
        """Return number of samples in dataframe.

        Returns
        -------
        int
            Number of samples in dataframe
        """
        return self.data.shape[0]

    @property
    def label_type(self) -> t.Optional[str]:
        """Return the label type.

         Returns
        -------
        t.Optional[str]
            Label type
        """
        return self._label_type

    def train_test_split(self: TDataset,
                         train_size: t.Union[int, float, None] = None,
                         test_size: t.Union[int, float] = 0.25,
                         random_state: int = 42,
                         shuffle: bool = True,
                         stratify: t.Union[t.List, pd.Series, np.ndarray, bool] = False
                         ) -> t.Tuple[TDataset, TDataset]:
        """Split dataset into random train and test datasets.

        Parameters
        ----------
        train_size : t.Union[int, float, None] , default: None
            If float, should be between 0.0 and 1.0 and represent the proportion of the dataset to include in
            the train split. If int, represents the absolute number of train samples. If None, the value is
            automatically set to the complement of the test size.
        test_size : t.Union[int, float] , default: 0.25
            If float, should be between 0.0 and 1.0 and represent the proportion of the dataset to include in the
            test split. If int, represents the absolute number of test samples.
        random_state : int , default: 42
            The random state to use for shuffling.
        shuffle : bool , default: True
            Whether or not to shuffle the data before splitting.
        stratify : t.Union[t.List, pd.Series, np.ndarray, bool] , default: False
            If True, data is split in a stratified fashion, using the class labels. If array-like, data is split in
            a stratified fashion, using this as class labels.
        Returns
        -------
        Dataset
            Dataset containing train split data.
        Dataset
            Dataset containing test split data.
        """
        if isinstance(stratify, bool):
            stratify = self.label_col if stratify else None

        train_df, test_df = train_test_split(self._data,
                                             test_size=test_size,
                                             train_size=train_size,
                                             random_state=random_state,
                                             shuffle=shuffle,
                                             stratify=stratify)
        return self.copy(train_df), self.copy(test_df)

    @staticmethod
    def _infer_label_type(
            label_col: pd.Series,
            max_categorical_ratio: float,
            max_categories: int,
            max_float_categories: int
    ):
        if not is_numeric_dtype(label_col):
            return 'classification_label'
        elif is_categorical(label_col, max_categorical_ratio, max_categories, max_float_categories):
            return 'classification_label'
        else:
            return 'regression_label'

    @staticmethod
    def _infer_categorical_features(
            df: pd.DataFrame,
            max_categorical_ratio: float,
            max_categories: int,
            max_float_categories: int,
            columns: t.Optional[t.List[Hashable]] = None,
    ) -> t.List[Hashable]:
        """Infers which features are categorical by checking types and number of unique values.

         Parameters
        ----------
        df: pd.DataFrame
        max_categorical_ratio: float
        max_categories: int
        max_float_categories: int
        columns: t.Optional[t.List[Hashable]] , default: None
        Returns
        -------
        t.List[Hashable]
           Out of the list of feature names, returns list of categorical features
        """
        categorical_columns = infer_categorical_features(
            df,
            max_categorical_ratio=max_categorical_ratio,
            max_categories=max_categories,
            max_float_categories=max_float_categories,
            columns=columns
        )

        if len(categorical_columns) > 0:
            columns = list(map(str, categorical_columns))[:7]
            stringified_columns = ", ".join(columns)
            if len(categorical_columns) < 7:
                logger.warning(
                    'Automatically inferred these columns as categorical features: %s. \n',
                    stringified_columns
                )
            else:
                logger.warning(
                    'Some columns have been inferred as categorical features: '
                    '%s. \n and more... \n For the full list '
                    'of columns, use dataset.cat_features',
                    stringified_columns
                )

        return categorical_columns

    def is_categorical(self, col_name: Hashable) -> bool:
        """Check if uniques are few enough to count as categorical.

        Parameters
        ----------
        col_name : Hashable
            The name of the column in the dataframe

        Returns
        -------
        bool
            If is categorical according to input numbers

        """
        return is_categorical(
            t.cast(pd.Series, self._data[col_name]),
            max_categorical_ratio=self._max_categorical_ratio,
            max_categories=self._max_categories,
            max_float_categories=self._max_float_categories
        )

    @property
    def index_name(self) -> t.Optional[Hashable]:
        """If index column exists, return its name.

        Returns
        -------
        t.Optional[Hashable]
           index name
        """
        return self._index_name

    @property
    def index_col(self) -> t.Optional[pd.Series]:
        """Return index column. Index can be a named column or DataFrame index.

        Returns
        -------
        t.Optional[pd.Series]
           If index column exists, returns a pandas Series of the index column.
        """
        if self._set_index_from_dataframe_index is True:
            index_name = self.data.index.name or 'index'
            if self._index_name is None:
                return pd.Series(self.data.index.get_level_values(0), name=index_name,
                                 index=self.data.index)
            elif isinstance(self._index_name, (str, int)):
                return pd.Series(self.data.index.get_level_values(self._index_name), name=index_name,
                                 index=self.data.index)
            else:
                raise DeepchecksValueError(f'Don\'t know to handle index_name of type {type(self._index_name)}')
        elif self._index_name is not None:
            return self.data[self._index_name]
        else:  # No meaningful index to use: Index column not configured, and _set_index_from_dataframe_index is False
            return

    @property
    def datetime_name(self) -> t.Optional[Hashable]:
        """If datetime column exists, return its name.

        Returns
        -------
        t.Optional[Hashable]
           datetime name
        """
        return self._datetime_name

    def get_datetime_column_from_index(self, datetime_name):
        """Retrieve the datetime info from the index if _set_datetime_from_dataframe_index is True."""
        index_name = self.data.index.name or 'datetime'
        if datetime_name is None:
            return pd.Series(self.data.index.get_level_values(0), name=index_name,
                             index=self.data.index)
        elif isinstance(datetime_name, (str, int)):
            return pd.Series(self.data.index.get_level_values(datetime_name), name=index_name,
                             index=self.data.index)

    @property
    def datetime_col(self) -> t.Optional[pd.Series]:
        """Return datetime column if exists.

        Returns
        -------
        t.Optional[pd.Series]
            Series of the datetime column
        """
        if self._set_datetime_from_dataframe_index is True:
            return self._datetime_column
        elif self._datetime_name is not None:
            return self.data[self._datetime_name]
        else:  # No meaningful Datetime to use: Datetime column not configured, and _set_datetime_from_dataframe_index
            # is False
            return

    @property
    def label_name(self) -> t.Optional[Hashable]:
        """If label column exists, return its name.

        Returns
        -------
        t.Optional[Hashable]
           Label name
        """
        return self._label_name

    @property
    def features(self) -> t.List[Hashable]:
        """Return list of feature names.

        Returns
        -------
        t.List[Hashable]
           List of feature names.
        """
        return list(self._features)

    @property
    def features_columns(self) -> pd.DataFrame:
        """Return DataFrame containing only the features defined in the dataset, if features are empty raise error.

        Returns
        -------
        pd.DataFrame
        """
        self.assert_features()
        return self.data[self.features]

    @property
    def label_col(self) -> pd.Series:
        """Return Series of the label defined in the dataset, if label is not defined raise error.

        Returns
        -------
        pd.Series
        """
        self.assert_label()
        return self.data[self.label_name]

    @property
    def cat_features(self) -> t.List[Hashable]:
        """Return list of categorical feature names.

         Returns
        -------
        t.List[Hashable]
           List of categorical feature names.
        """
        return list(self._cat_features)

    @property
    def numerical_features(self) -> t.List[Hashable]:
        """Return list of numerical feature names.

         Returns
        -------
        t.List[Hashable]
           List of categorical feature names.
        """
        return list(self._numerical_features)

    @property
    @lru_cache(maxsize=128)
    def classes(self) -> t.Tuple[str, ...]:
        """Return the classes from label column in sorted list. if no label column defined, return empty list.

        Returns
        -------
        t.Tuple[str, ...]
            Sorted classes
        """
        if self.label_name is not None:
            return tuple(sorted(self.data[self.label_name].dropna().unique().tolist()))
        return tuple()

    @property
    def columns_info(self) -> t.Dict[Hashable, str]:
        """Return the role and logical type of each column.

        Returns
        -------
        t.Dict[Hashable, str]
           Directory of a column and its role
        """
        columns = {}
        for column in self.data.columns:
            if column == self._index_name:
                value = 'index'
            elif column == self._datetime_name:
                value = 'date'
            elif column == self._label_name:
                value = 'label'
            elif column in self._features:
                if column in self.cat_features:
                    value = 'categorical feature'
                elif column in self.numerical_features:
                    value = 'numerical feature'
                else:
                    value = 'other feature'
            else:
                value = 'other'
            columns[column] = value
        return columns

    def assert_label(self):
        """Check if label is defined and if not raise error.

        Raises
        ------
        DeepchecksNotSupportedError
        """
        if not self.label_name:
            raise DeepchecksNotSupportedError('There is no label defined to use. Did you pass a DataFrame '
                                              'instead of a Dataset?')

    def assert_features(self):
        """Check if features are defined (not empty) and if not raise error.

        Raises
        ------
        DeepchecksNotSupportedError
        """
        if not self.features:
            raise DeepchecksNotSupportedError('There are no features defined to use. Did you pass a DataFrame '
                                              'instead of a Dataset?')

    def assert_datetime(self):
        """Check if datetime is defined and if not raise error.

        Raises
        ------
        DeepchecksNotSupportedError
        """
        if not (self._set_datetime_from_dataframe_index or self._datetime_name):
            raise DatasetValidationError('There is no datetime defined to use. Did you pass a DataFrame instead '
                                         'of a Dataset?')

    def assert_index(self):
        """Check if index is defined and if not raise error.

        Raises
        ------
        DeepchecksNotSupportedError
        """
        if not (self._set_index_from_dataframe_index or self._index_name):
            raise DatasetValidationError('There is no index defined to use. Did you pass a DataFrame instead '
                                         'of a Dataset?')

    def select(
            self: TDataset,
            columns: t.Union[Hashable, t.List[Hashable], None] = None,
            ignore_columns: t.Union[Hashable, t.List[Hashable], None] = None,
            keep_label: bool = False
    ) -> TDataset:
        """Filter dataset columns by given params.

        Parameters
        ----------
        columns : Union[Hashable, List[Hashable], None]
            Column names to keep.
        ignore_columns : Union[Hashable, List[Hashable], None]
            Column names to drop.

        Returns
        -------
        TDataset
            horizontally filtered dataset

        Raises
        ------
        DeepchecksValueError
            In case one of columns given don't exists raise error
        """
        if keep_label and columns and self.label_name not in columns:
            columns.append(self.label_name)

        new_data = select_from_dataframe(self._data, columns, ignore_columns)
        if new_data.equals(self.data):
            return self
        else:
            return self.copy(new_data)

    @classmethod
    def ensure_not_empty_dataset(cls, obj: t.Any) -> 'Dataset':
        """Verify Dataset or transform to Dataset.

        Function verifies that provided value is a non-empty instance of Dataset,
        otherwise raises an exception, but if the 'cast' flag is set to True it will
        also try to transform provided value to the Dataset instance.

        Parameters
        ----------
        obj
            value to verify

        Raises
        ------
        DeepchecksValueError
            if the provided value is not a Dataset instance;
            if the provided value cannot be transformed into Dataset instance;
        DatasetValidationError
            if the provided value is empty Dataset instance;
        """
        if isinstance(obj, pd.DataFrame):
            obj = Dataset(obj, features=[], cat_features=[])
        elif not isinstance(obj, Dataset):
            raise DeepchecksValueError(
                f'non-empty instance of Dataset or DataFrame was expected, instead got {type(obj).__name__}'
            )
        if len(obj.data) == 0:
            raise DatasetValidationError('dataset cannot be empty')
        return obj

    @classmethod
    def datasets_share_features(cls, *datasets: 'Dataset') -> bool:
        """Verify that all provided datasets share same features.

        Parameters
        ----------
        datasets : List[Dataset]
            list of datasets to validate

        Returns
        -------
        bool
            True if all datasets share same features, otherwise False

        Raises
        ------
        AssertionError
            'datasets' parameter is not a list;
            'datasets' contains less than one dataset;
        """
        assert len(datasets) > 1, "'datasets' must contains at least two items"

        # TODO: should not we also check features dtypes?

        features_names = set(datasets[0].features)

        for ds in datasets[1:]:
            if features_names != set(ds.features):
                return False

        return True

    @classmethod
    def datasets_share_categorical_features(cls, *datasets: 'Dataset') -> bool:
        """Verify that all provided datasets share same categorical features.

        Parameters
        ----------
        datasets : List[Dataset]
            list of datasets to validate

        Returns
        -------
        bool
            True if all datasets share same categorical features, otherwise False

        Raises
        ------
        AssertionError
            'datasets' parameter is not a list;
            'datasets' contains less than one dataset;
        """
        assert len(datasets) > 1, "'datasets' must contains at least two items"

        # TODO: should not we also check features dtypes?

        first = set(datasets[0].cat_features)

        for ds in datasets[1:]:
            features = set(ds.cat_features)
            if first != features:
                return False

        return True

    @classmethod
    def datasets_share_label(cls, *datasets: 'Dataset') -> bool:
        """Verify that all provided datasets share same label column.

        Parameters
        ----------
        datasets : List[Dataset]
            list of datasets to validate

        Returns
        -------
        bool
            True if all datasets share same categorical features, otherwise False

        Raises
        ------
        AssertionError
            'datasets' parameter is not a list;
            'datasets' contains less than one dataset;
        """
        assert len(datasets) > 1, "'datasets' must contains at least two items"

        # TODO: should not we also check label dtypes?
        label_name = datasets[0].label_name

        for ds in datasets[1:]:
            if ds.label_name != label_name:
                return False

        return True

    @classmethod
    def datasets_share_index(cls, *datasets: 'Dataset') -> bool:
        """Verify that all provided datasets share same index column.

        Parameters
        ----------
        datasets : List[Dataset]
            list of datasets to validate

        Returns
        -------
        bool
            True if all datasets share same index column, otherwise False

        Raises
        ------
        AssertionError
            'datasets' parameter is not a list;
            'datasets' contains less than one dataset;
        """
        assert len(datasets) > 1, "'datasets' must contains at least two items"

        first_ds = datasets[0]

        for ds in datasets[1:]:
            if (ds._index_name != first_ds._index_name or
                    ds._set_index_from_dataframe_index != first_ds._set_index_from_dataframe_index):
                return False

        return True

    @classmethod
    def datasets_share_date(cls, *datasets: 'Dataset') -> bool:
        """Verify that all provided datasets share same date column.

        Parameters
        ----------
        datasets : List[Dataset]
            list of datasets to validate

        Returns
        -------
        bool
            True if all datasets share same date column, otherwise False

        Raises
        ------
        AssertionError
            'datasets' parameter is not a list;
            'datasets' contains less than one dataset;
        """
        assert len(datasets) > 1, "'datasets' must contains at least two items"

        first_ds = datasets[0]

        for ds in datasets[1:]:
            if (ds._datetime_name != first_ds._datetime_name or
                    ds._set_datetime_from_dataframe_index != first_ds._set_datetime_from_dataframe_index):
                return False

        return True

    def __len__(self) -> int:
        """Return number of samples in the member dataframe.

        Returns
        -------
        int

        """
        return self.n_samples
