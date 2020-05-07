from datetime import time, timedelta

from django.db.models import IntegerField
from math import floor


class AbilityValue:
    def __init__(self, value):
        self._value = value

    @property
    def real_value(self):
        return self._value

    @real_value.setter
    def real_value(self, value):
        self._value = value

    @property
    def modifier(self):
        return floor((self._value - 10) / 2)

    def __len__(self):
        return 2

    def __getitem__(self, item):
        if item == "real_value":
            return self.real_value
        elif item == "modifier":
            return self.modifier
        else:
            raise KeyError(item)

    def __iter__(self):
        return ["real_value", "modifier"].__iter__()


class AbilityValueField(IntegerField):
    def to_python(self, value):
        if isinstance(value, AbilityValue):
            return value

        if value is None:
            return value

        return AbilityValue(value)

    def get_prep_value(self, value):
        return value.real_value


class Duration:
    def __init__(self, value):
        self._value = value

    @property
    def rounds(self):
        return self._value

    @rounds.setter
    def rounds(self, value):
        self._value = value

    @property
    def time(self):
        s = (6 * self._value) % 60
        m = (6 * self._value) // 60
        h = (6 * self._value) // 3600
        return timedelta(seconds=s, minutes=m, hours=h)

    @time.setter
    def time(self, value):
        if value.second % 6 != 0:
            raise ValueError("Time value must be the multiply of 6 seconds!")
        self._value = value.seconds / 6 + value.minutes * 10 + value.hours * 600


class DurationField(IntegerField):
    def to_python(self, value):
        if isinstance(value, Duration):
            return value

        if value is None:
            return value

        return Duration(value)

    def get_prep_value(self, value):
        return value.rounds
