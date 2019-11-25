import json
from models.EventMeasurement import EventMeasurement


class FieldOpMeasurement(object):
    def __init__(self, d):
        if type(d) is str:
            d = json.loads(d)

        self.from_dict(d)

    def from_dict(self, d):
        self.__dict__ = {}
        for key, value in d.items():
            k = 'yield_' if key == 'yield' else key
            if type(value) is dict:
                value = FieldOpMeasurement(value)
            self.__dict__[k] = value

    measurementName = ""
    measurementCategory = ""
    area: EventMeasurement
    yield_: EventMeasurement
    averageYield: EventMeasurement
    averageMoisture: EventMeasurement
    totalMaterial: EventMeasurement
    averageMaterial: EventMeasurement
    averageSpeed: EventMeasurement
