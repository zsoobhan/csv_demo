#!/usr/bin/env python3

import re


DAYS_MAP = {
    'mon': 'square',
    'tue': 'square',
    'wed': 'square',
    'thu': 'double',
    'fri': 'double',
}
DAYS = list(DAYS_MAP.keys())  # N.B. python3.6 dicts remember the order of keys
DAYS_RE = '|'.join(DAYS)

FUNCTION_MAP = {
    'square': lambda x: x ** 2,
    'double': lambda x: x * 2,
}


class CSVParserException(Exception):
    pass


class InvalidColumnException(CSVParserException):
    pass


class InvalidFunctionKeyException(CSVParserException):
    pass


def generate_function_value(
    function_key: str, value: int, function_map=FUNCTION_MAP
):
    """
    concatenates the description str with evaluated function

    example return:
        >>> 'DESCRIPTION 99'
    """

    try:
        function = function_map[function_key]
    except KeyError:
        raise InvalidFunctionKeyException(
            f'{function_key} not in {function_map.keys()}'
        )

    return function(value)  # evaluates function


def generate_description(description: str, final_value: int):
    """
    concatenates the description str with final_value

    example return:
        >>> 'DESCRIPTION 99'
    """

    return '{description} {final_value}'.format(
        description=description,
        final_value=final_value
    )


def get_valid_columns(label: str, days_re=DAYS_RE):
    '''
    checks if label is valid and returns list of valid day interval or
    column name
    '''

    if label == 'description':
        return [label]

    days = label.split('-')

    if len(days) > 2:
        raise InvalidColumnException(
            f'label ({label}) has multiple -, 1 expected'
        )

    for day in days:
        if not re.findall(days_re, day):
            raise InvalidColumnException(f'label ({label}) not in ({days_re})')

    return get_days_from_range(days)


def get_days_from_range(days: list, master_list=DAYS):
    '''
    returns a list of matching days from the master_list
    expects a list of 1 or 2 days in correct order.

    e.g.:
        >>> ['mon'] --> ['mon']
        >>> ['mon', 'wed'] --> ['mon', 'tue', 'wed']

    '''
    # TODO: refactor this

    if len(days) == 2:
        return master_list[
            master_list.index(days[0]): master_list.index(days[1]) + 1
        ]
    return [master_list[master_list.index(days[0])]]
