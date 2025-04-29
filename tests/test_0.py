from pytest import raises

from src import slow_deadband

from .payloads import input_1, output_1, output_2, output_3


def test_slow_deadband():
    assert slow_deadband(input_1, 10, 30) == output_1
    assert slow_deadband([], 10, 30) == []
    with raises(Exception):
        slow_deadband(input_1, 10, 30, time_unit="invalid")
    with raises(Exception):
        slow_deadband(input_1, 10, 30, deadband_type="invalid")
    assert slow_deadband(input_1, 10, 30, deadband_type="percent") == output_2
    assert slow_deadband(input_1, 10, 30, 5) == output_3
    assert slow_deadband(input_1, 10, 30000, time_unit="ms") == output_1
    assert slow_deadband(input_1, 10, 30000000, time_unit="us") == output_1
