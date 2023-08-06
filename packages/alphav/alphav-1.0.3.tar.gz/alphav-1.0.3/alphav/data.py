import pandas as pd
from abc import ABC


class Data:

    def __init__(self, function: str, data: dict, default='annual'):
        """
        data portion received from api function
        :param function: function for api
        :param data: raw data
        :param default: selection between annual and quarterly, to be put to main data
        """
        self._function = function
        self._raw = data

        self._main = None  # the main data piece of which we currently work on
        self._annual = None  # annual data if supported
        self._quarterly = None  # quarterly data if supported
        self._default = default  # when both annual and yearly provided - one of which is main

        # data functions that support yearly and quarterly data
        if function in [
            'INCOME_STATEMENT',
            'BALANCE_SHEET',
            'CASH_FLOW',
            'EARNINGS'
        ]:
            suffix = 'Earnings' if function == 'EARNINGS' else 'Reports'
            self._quarterly = pd.DataFrame(self._raw[f'quarterly{suffix}'])
            self._annual = pd.DataFrame(self._raw[f'annual{suffix}'])
            self.set_main(self._default)
        else:
            try:
                self._main = pd.DataFrame(self._raw)
            except ValueError:
                self._main = self._raw

    def __str__(self):
        return f'{self.name}\n' \
               f'{self.main}'

    def set_main(self, default):
        """
        set main to be annual or quarterly data
        :param default: 'annual' | 'quarterly'
        """
        assert self._annual is not None or self._quarterly is not None
        self._main = self._annual if default == 'annual' else self._quarterly

    @property
    def default(self):
        """
        :return: currently selected main data
        """
        return self._default

    @property
    def name(self):
        """
        :return: beautified name for this function
        """
        return self.function.lower().replace('_', ' ').title()

    @property
    def function(self) -> str:
        """
        :return: function section of the api
        """
        return self._function

    @property
    def raw(self):
        """
        :return: raw data provided by api
        """
        return self._raw

    @property
    def quarterly(self):
        """
        :return: quarterly data portion if exists
        """
        return self._quarterly

    @property
    def annual(self):
        """
        :return: annual data portion if exists
        """
        return self._annual

    @property
    def main(self):
        """
        :return: main data portion, annual / quarterly if exists and selected
        """
        return self._main


class PullDataDescriptor(ABC):

    def __init__(self, function=None):
        self._function = function

    def __set_name__(self, owner, name: str):
        self.private_name = '_' + name
        self.name = name
        self.owner = owner

    def __get__(self, obj, objtype=None):
        try:
            value = getattr(obj, self.private_name)
        except AttributeError:
            function = self._function if self._function is not None else self.name.upper()
            data = obj.req(function)
            setattr(obj, self.private_name, Data(function, data))
            value = getattr(obj, self.private_name)
        return value
