# Author: Carlos Xavier Hernandez <cxh@stanford.edu>
# Contributors:
# Copyright (c) 2016, Stanford University and the Authors
# All rights reserved.

from __future__ import print_function, division, absolute_import

from sklearn import preprocessing
from sklearn.preprocessing import _data
from sklearn.preprocessing import _label
from sklearn.preprocessing import _function_transformer
import sklearn.impute

from .base import (MultiSequencePreprocessingMixin,
                   MultiSequenceOnlinePreprocessingMixin)
from .timeseries import Butterworth, EWMA, DoubleEWMA

__all__ = ['Binarizer', 'Butterworth', 'DoubleEWMA', 'EWMA', 'Imputer',
           'KernelCenterer', 'LabelBinarizer', 'MultiLabelBinarizer',
           'Normalizer', 'PolynomialFeatures']


class Binarizer(MultiSequencePreprocessingMixin, _data.Binarizer):
    __doc__ = _data.Binarizer.__doc__

# Older versions of sklearn might not have this
if hasattr(_function_transformer, 'FunctionTransformer'):
    __all__.append('FunctionTransformer')

    class FunctionTransformer(MultiSequencePreprocessingMixin,
                              _function_transformer.FunctionTransformer):
        __doc__ = _function_transformer.FunctionTransformer.__doc__


#class Imputer(MultiSequencePreprocessingMixin, sklearn.impute):
    #__doc__ = sklearn.impute.__doc__


class KernelCenterer(MultiSequencePreprocessingMixin,
                     _data.KernelCenterer):
    __doc__ = _data.KernelCenterer.__doc__


class LabelBinarizer(MultiSequencePreprocessingMixin,
                     _label.LabelBinarizer):
    __doc__ = _label.LabelBinarizer.__doc__


class MultiLabelBinarizer(MultiSequencePreprocessingMixin,
                          _label.MultiLabelBinarizer):
    __doc__ = _label.MultiLabelBinarizer.__doc__

# Older versions of sklearn might not have this
if hasattr(_data.MinMaxScaler, 'partial_fit'):
    __all__.append('MinMaxScaler')

    class MinMaxScaler(MultiSequenceOnlinePreprocessingMixin,
                       _data.MinMaxScaler):
        __doc__ = _data.MinMaxScaler.__doc__

# Older versions of sklearn might not have this
if hasattr(_data, 'MaxAbsScaler'):
    __all__.append('MaxAbsScaler')

    class MaxAbsScaler(MultiSequenceOnlinePreprocessingMixin,
                       _data.MaxAbsScaler):
        __doc__ = _data.MaxAbsScaler.__doc__


class Normalizer(MultiSequencePreprocessingMixin, _data.Normalizer):
    __doc__ = _data.Normalizer.__doc__

# Older versions of sklearn might not have this
if hasattr(_data, 'RobustScaler'):
    __all__.append('RobustScaler')

    class RobustScaler(MultiSequencePreprocessingMixin,
                       _data.RobustScaler):
        __doc__ = _data.RobustScaler.__doc__

# Older versions of sklearn might not have this
if hasattr(_data.StandardScaler, 'partial_fit'):
    __all__.append('StandardScaler')

    class StandardScaler(MultiSequenceOnlinePreprocessingMixin,
                         _data.StandardScaler):
        __doc__ = _data.StandardScaler.__doc__


class PolynomialFeatures(MultiSequencePreprocessingMixin,
                         _data.PolynomialFeatures):
    __doc__ = _data.PolynomialFeatures.__doc__
