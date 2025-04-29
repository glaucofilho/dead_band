from pytest import raises

from src import slow_deadband

from .payloads import input_1, output_1


def test_slow_deadband():
    assert slow_deadband(input_1, 10, 30) == output_1
    assert slow_deadband([], 10, 30) == []
    with raises(Exception):
        slow_deadband(input_1, 10, 30, time_unit="invalid")
    with raises(Exception):
        slow_deadband(input_1, 10, 30, deadband_type="invalid")
