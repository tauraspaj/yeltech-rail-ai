from common import utils


def test_parse_datetime_string():
    assert utils.calculate_time_ahead('2023-03-25', 5) == ('2023-03-25',
                                                           '2023-03-30')
