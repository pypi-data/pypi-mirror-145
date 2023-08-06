from functools import cached_property

import numpy as np
from physiocurve.common import estimate_samplerate
from physiocurve.pressure import foot, incycle

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


class Pressure:
    def __init__(self, values, samplerate, index=None):
        self._index = index
        self._values = values
        self._samplerate = samplerate

    @classmethod
    def from_pandas(cls, series, samplerate=None):
        if samplerate is None:
            samplerate = estimate_samplerate(series)
        return cls(series.to_numpy(), samplerate, series.index.to_numpy())

    @property
    def samplerate(self):
        return self._samplerate

    @cached_property
    def argfeet(self):
        return foot.findPressureFeet(self._values, self._samplerate)

    @property
    def idxfeet(self):
        return self._index[self.argfeet] if self._index is not None else self.argfeet

    @ifpandas
    def feet(self):
        values = self._values[self.argfeet]
        idx = self.index[self.argfeet]
        return pd.Series(values, index=idx)

    @cached_property
    def _argdiasys(self):
        return incycle.find_dia_sys(self._values, self._samplerate, self.argfeet)

    @property
    def argdia(self):
        dia, _ = self._argdiasys
        return dia

    @property
    def idxdia(self):
        return self._index[self.argdia] if self._index is not None else self.argdia

    @ifpandas
    def diastolics(self):
        values = self._values[self.argdia]
        idx = self.index[self.argdia]
        return pd.Series(values, index=idx)

    @property
    def argsys(self):
        _, sys = self._argdiasys
        return sys

    @property
    def idxsys(self):
        return self._index[self.argsys] if self._index is not None else self.argsys

    @ifpandas
    def systolics(self):
        values = self._values[self.argsys]
        idx = self.index[self.argsys]
        return pd.Series(values, index=idx)

    @cached_property
    def argdic(self):
        return incycle.find_dicrotics(self._values, *self._argdiasys)

    @property
    def idxdic(self):
        return self._index[self.argdic] if self._index is not None else self.argdic

    @ifpandas
    def diastolics(self):
        values = self._values[self.argdic]
        idx = self.index[self.argdic]
        return pd.Series(values, index=idx)

    @cached_property
    def means(self):
        return incycle.calc_means(self._values, self.argdia)

    @cached_property
    def heartrate(self):
        return foot.calc_heartrate(self.argfeet, self._samplerate)

    @cached_property
    def sqi(self):
        return incycle.calc_quality_index(
            self._values,
            self.argdia,
            self.argsys,
            self.means,
            self.heartrate,
            self._samplerate,
        )

    @cached_property
    def nra(self):
        values = self._values
        idxok = self.argdic.astype(bool)
        dics = values[self.argdic[idxok]]

        # Remove invalid dicrotic samples from all arrays
        sysidx = np.zeros(self.argsys.shape[0], dtype=bool)
        sysidx[: idxok.shape[0]] = idxok
        syss = values[self.argsys[sysidx]]

        diaidx = np.zeros(self.argdia.shape[0], dtype=bool)
        diaidx[: idxok.shape[0]] = idxok
        dias = values[self.argdia[diaidx]]
        return (dics - dias) / (syss - dias)
