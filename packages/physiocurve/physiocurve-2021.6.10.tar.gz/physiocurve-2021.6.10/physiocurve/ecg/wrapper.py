from functools import cached_property

from ecgdetectors import Detectors
from physiocurve.common import estimate_samplerate

try:
    import pandas as pd

    HASPANDAS = True
except ImportError:
    HASPANDAS = False


def ifpandas(func):
    def wrapper_ifpandas():
        if HASPANDAS:
            func()
        else:
            pass

    return wrapper_ifpandas


class Ecg:
    def __init__(self, values, samplerate, index=None):
        self._index = index
        self._rwaves = None
        self._values = values
        self._samplerate = samplerate
        self._detectors = Detectors(samplerate)

    @classmethod
    def from_pandas(cls, series, samplerate=None):
        if samplerate is None:
            samplerate = estimate_samplerate(series)
        return cls(series.to_numpy(), samplerate, series.index.to_numpy())

    @property
    def samplerate(self):
        return self._samplerate

    @cached_property
    def argrwave(self):
        return self._detectors.christov_detector(self._values)

    @property
    def idxrwave(self):
        return self._index[self.argrwave] if self._index else self.argrwave

    @ifpandas
    def rwaves(self):
        values = self._values[self.argrwave]
        idx = self.index[self.argrwave]
        return pd.Series(values, index=idx)
