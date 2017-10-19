#!/usr/bin/env python3


class CSVParser:
    """
    CSVParser will parse all of the files matching the glob '*.csv'
    located in `self.directory` when `self.parse()` is run.

    n.b. `__init__` will only accept keyword arguments

    params::
    :directory: the relative location of the directory containing the csv files

    """

    directory = None
    parsed_values = None

    def __init__(self, **kwargs):
        """
        Sets the expected attributes on the instance if passed to init.
        """
        expected_attributes = ['directory']

        for attr in expected_attributes:
            setattr(self, attr, kwargs.get(attr))

    def parse(self):
        """
        Parses the files in self.directory and returns values in a dictionary

        returns:
        >>> {
        >>>     'day': value of day (mon, tue, wed, thu, fri),
        >>>     'description': verbose description ,
        >>>     'value': value,
        >>>     'square'|'double': mathematical evaluation pertaining to `value`
        >>> }

        """
        pass

    def output(self):
        """
        Prints the contents of self.parsed_values to the screen

        """
