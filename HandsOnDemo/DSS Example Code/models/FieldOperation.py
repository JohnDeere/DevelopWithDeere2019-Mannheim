import json


class FieldOperation(object):
    def __init__(self, d):
        if type(d) is str:
            d = json.loads(d)

        self.from_dict(d)

    def from_dict(self, d):
        self.__dict__ = {}
        for key, value in d.items():
            if type(value) is dict:
                value = FieldOperation(value)
            self.__dict__[key] = value

    fieldOperationType = ""
    adaptMachineType = ""
    cropSeason = ""
    startDate = ""
    endDate = ""
    links = ""
