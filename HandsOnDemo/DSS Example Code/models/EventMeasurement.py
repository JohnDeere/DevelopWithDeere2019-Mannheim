import json


class EventMeasurement(object):
    def __init__(self, d):
        if type(d) is str:
            d = json.loads(d)

        self.from_dict(d)

    def from_dict(self, d):
        self.__dict__ = {}
        for key, value in d.items():
            if type(value) is dict:
                value = EventMeasurement(value)
            self.__dict__[key] = value

    value = ""
    unitId = ""
