import pandas as pd


def findPressureFeet(curve):
    series = curve.series
    samplerate = curve.samplerate

    fstderiv = series.diff().shift(-1)
    sndderiv = fstderiv.diff().shift(-1)

    # Remove deceleration peaks
    sndderiv = sndderiv * (fstderiv > 0)

    def performWindowing(sumcoef=4, quantcoef=3):
        # Find pulse rising edge
        winsum = int(samplerate / sumcoef)
        winquant = int(samplerate * quantcoef)
        sndderivsq = sndderiv ** 2
        integral = sndderivsq.rolling(window=winsum, center=True).sum()
        thres = integral.rolling(window=winquant).quantile(0.7)
        thres = thres.fillna(method='backfill')
        risings = (integral > thres).astype(int)
        risingvar = risings.diff()
        (risingStarts,) = (risingvar > 0).nonzero()
        (risingStops,) = (risingvar < 0).nonzero()
        return (risingStarts, risingStops)

    found = False
    for quantcoef in [3, 2, 1]:
        # Try again with smaller window if we find nothing
        risingStarts, risingStops = performWindowing(quantcoef=quantcoef)
        try:
            risingStops = risingStops[risingStops > risingStarts[0]]
            found = True
            break
        except IndexError:
            continue

    # Last resort: find one foot on the whole series
    if not found:
        risingStarts = [0]
        risingStops = [len(sndderiv) - 1]

    def locateMaxima():
        for start, stop in zip(risingStarts, risingStops):
            idxstart = sndderiv.index[start]
            idxstop = sndderiv.index[stop]
            try:
                maximum = sndderiv.loc[idxstart:idxstop].idxmax()
            except ValueError:
                continue
            else:
                yield maximum

    cycleStarts = pd.Index(list(locateMaxima()))
    return cycleStarts
