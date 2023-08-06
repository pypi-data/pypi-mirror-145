import itertools

import numpy as np
import pandas as pd

from graphysio.algorithms.filters import savgol


def findPressureFull(curve):
    series = curve.series
    samplerate = curve.samplerate

    fstderivraw = series.diff().iloc[1:]
    sndderivraw = fstderivraw.diff().iloc[1:]
    # Smoothen the derivatives
    fstderiv, _ = savgol(fstderivraw, samplerate, (0.16, 2))
    sndderiv, _ = savgol(sndderivraw, samplerate, (0.16, 2))

    cycles = []
    starts, durations = curve.getCycleIndices()
    for start, duration in zip(starts, durations):
        stop = start + duration
        diastop = start - duration
        dia = findPOI(series, [start, diastop], 'min', windowsize=0.05, forcesign=False)
        sbp = findPOI(series, [start, stop], 'max', windowsize=0.05)
        peridic = findPOI(sndderiv, [sbp, stop], 'max', windowsize=0.15)
        dic = findHorizontal(fstderiv, peridic)
        cycle = (dia, sbp, dic)
        cycles.append(cycle)

    indices = [pd.Index(idx, dtype=np.int64) for idx in zip(*cycles)]
    return indices


# Utility function for point placing


def isbetter(new, ref, kind, forcesign):
    if kind == 'max':
        condition = new > ref
        if forcesign:
            condition = condition or (new < 0)
    elif kind == 'min':
        condition = new < ref
        if forcesign:
            condition = condition or (new > 0)
    else:
        raise ValueError(kind)
    return condition


def genWindows(soi, interval, windowspan):
    begin, end = interval
    ltr = end > begin
    windowspan *= 1e9  # s to ns
    if begin is None or end is None:
        return
    if ltr:
        direction = 1
    else:
        direction = -1
    for n in itertools.count():
        start = begin + direction * n * windowspan
        stop = start + direction * windowspan

        # Stop condition if we exceed end
        if ltr:
            if stop >= end:
                stop = end
        else:
            if stop <= end:
                stop = end
            start, stop = (stop, start)

        window = soi.loc[start:stop]
        if len(window) < 1:
            return
        yield window.index.values


def findPOI(soi, interval, kind, windowsize, forcesign=True):
    if kind not in ['min', 'max']:
        raise ValueError(kind)
    argkind = 'idx' + kind

    goodwindow = []
    previous = -np.inf if kind == 'max' else np.inf
    for window in genWindows(soi, interval, windowsize):
        zoi = soi.loc[window]
        new = getattr(zoi, kind)()
        if isbetter(new, previous, kind, forcesign):
            goodwindow = window
        else:
            break
        previous = new
    finalzoi = soi.loc[goodwindow]
    try:
        retidx = getattr(finalzoi, argkind)()
    except ValueError:
        # No POI found
        retidx = None
    return retidx


def findHorizontal(soi, loc):
    if loc is None:
        return None
    step = 8000000  # 8 ms (from ns)
    end = loc + 10 * step
    zoi = soi.loc[loc:end]
    horidx = zoi.abs().idxmin()
    return horidx
