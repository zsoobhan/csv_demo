#!/usr/bin/env python3

import glob
import os
import pandas

import utils


class CSVParser:
    """
    CSVParser will parse all of the files matching the glob '*.csv'
    located in `self.directory` when `self.parse()` is run.

    ::params::
    :directory: the relative location of the directory containing the csv files
                defaults to './csv_files/'
    """

    directory = None

    # internal
    _clean_data = {}
    _data = {}

    def __init__(self, directory: str=''):
        """
        Sets the directory value
        """
        if not self.directory:
            self.directory = './csv_files/'

    def parse(self):
        """
        Parses the csv files in self.directory, populates self._data  and
        returns self._data

        example of data generated:

        >>> { 'filepath':
        >>>     [
        >>>         {
        >>>             'day': value of day (mon, tue, wed, thu, fri),
        >>>             'description': verbose description ,
        >>>             'value': value,
        >>>             'square'|'double': mathematical evaluation of `value`
        >>>         }, ...
        >>>     ]
        >>> }

        """
        for filepath in glob.glob(os.path.join(self.directory, '*.csv')):
            self._get_clean_data(filepath)

        for filepath, matrix in self._clean_data.items():
            matrix_data = []

            #  generate a dict for each column with the exception of
            #  the 'description'
            for header in matrix.drop('description', axis=1).axes[1]:
                value = matrix[header][0]
                function_key = utils.DAYS_MAP[header]  # e.g. 'square'
                function_value = utils.generate_function_value(
                    function_key,
                    value
                )
                description = matrix['description'][0]

                matrix_data.append(
                    {
                        'day': header,
                        'description': utils.generate_description(
                            description, value
                        ),
                        function_key: function_value,
                        'value': value,
                    }
                )
            # append generated dictionaries to instance
            self._data[filepath] = matrix_data
        return self._data

    def _get_clean_data(self, filepath):
        """
        Get's data from csv files and transforms ranges into individual columns
        and updates self._clean_data with the resulting matrices
        """
        data = pandas.read_csv(filepath)
        print(f'Parsing {filepath}')

        for column in data.axes[1]:
            try:
                # split day ranges (e.g. 'mon-tue') into individual
                # columns (['mon', ''tue'])
                for valid_column in utils.get_valid_columns(column):
                    data[valid_column] = data[column]  # copy data

                # if it was a range, drop the original column
                if column != valid_column:
                    data = data.drop(column, axis=1)

            except utils.InvalidColumnException:
                data = data.drop(column, axis=1)

        self._clean_data[filepath] = data

    def __repr__(self):
        return (
            f'CSVParser: parsed={self._data.keys() if self._data else None}'
        )
