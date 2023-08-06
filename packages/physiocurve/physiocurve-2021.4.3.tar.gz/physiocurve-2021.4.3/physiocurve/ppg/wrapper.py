from physiocurve.pressure import Pressure


class PPG(Pressure):
    def __init__(self, values, samplerate, index=None):
        super().__init__(values, samplerate, index)

    def sqi(self):
        raise NotImplementedError
