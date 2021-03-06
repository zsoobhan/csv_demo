import pytest

from .. import utils


class TestGlobals(object):
    """
    Reduce the possibility of bad config value
    """

    def test_function_map_config(self):
        # quick and dirty check, not failsafe!
        assert set(utils.FUNCTION_MAP.keys()) == set(['square', 'double'])

    def test_days_config(self):
        assert utils.DAYS == ['mon', 'tue', 'wed', 'thu', 'fri']
        assert utils.DAYS_RE == 'mon|tue|wed|thu|fri'
        assert utils.DAYS_MAP == {
            'mon': 'square',
            'tue': 'square',
            'wed': 'square',
            'thu': 'double',
            'fri': 'double',
        }


class TestGenerateFunctionValue(object):
    function_map = {
        'cube': lambda x: x**3,
        'quad': lambda x: x**4,
    }

    def test_custom_function_map(self):
        result = utils.generate_function_value(
            'cube',
            3,
            function_map=self.function_map
        )
        assert result == 27

    def test_default_function_map(self):
        result = utils.generate_function_value(
            'double',
            3,
        )
        assert result == 6

    def test_correct_exception_raised(self):
        with pytest.raises(utils.InvalidFunctionKeyException) as exc:
            utils.generate_function_value(
                'invalid',
                3,
                function_map=self.function_map
            )
        assert str(exc.value) == "invalid not in dict_keys(['cube', 'quad'])"


class TestGenerateDescription(object):

    def test_custom_function_map(self):
        result = utils.generate_description(
            'foo bar',
            3,
        )
        assert result == 'foo bar 3'


class TestGetValidColumns(object):
    regex_pattern = 'foo|bar'

    def test_valid_description(self):
        assert utils.get_valid_columns('description') == ['description']

    def test_valid_default_pattern(self):
        assert utils.get_valid_columns('wed') == ['wed']

    def test_invalid_value(self):
        with pytest.raises(utils.InvalidColumnException) as exc:
            utils.get_valid_columns('baz', days_re=self.regex_pattern)
        assert str(exc.value) == 'label (baz) not in (foo|bar)'

    def test_invalid_range_not_in_regex(self):
        with pytest.raises(utils.InvalidColumnException) as exc:
            utils.get_valid_columns('foo-baz', days_re=self.regex_pattern)
        assert str(exc.value) == 'label (foo-baz) not in (foo|bar)'

    def test_invalid_range_too_many_dashes(self):
        with pytest.raises(utils.InvalidColumnException) as exc:
            utils.get_valid_columns('foo-baz-', days_re=self.regex_pattern)
        assert str(exc.value) == 'label (foo-baz-) has multiple -, 1 expected'


class TestGetDays(object):
    master_list = ['alpha', 'beta', 'gamma']

    def test_valid_custom_master_list(self):
        assert utils.get_days_from_range(
            ['beta'], master_list=self.master_list
        ) == ['beta']

    def test_valid_custom_master_list_range(self):
        assert utils.get_days_from_range(
            ['alpha', 'gamma'], master_list=self.master_list
        ) == ['alpha', 'beta', 'gamma']

    def test_valid_custom_default_list(self):
        assert utils.get_days_from_range(['mon']) == ['mon']

    def test_valid_range_default_list(self):
        assert utils.get_days_from_range(['tue', 'thu']) == [
            'tue', 'wed', 'thu'
        ]
