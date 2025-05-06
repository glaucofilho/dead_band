from pytest import raises

from dead_band import fast_deadband, slow_deadband

from .payloads import input_1, input_2, output_1, output_2, output_3, output_4


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
    assert slow_deadband(input_2, 10, 30) == output_4


def test_fast_deadband():
    assert fast_deadband(input_1, 10, 30) == output_1
    assert fast_deadband([], 10, 30) == []
    with raises(Exception):
        fast_deadband(input_1, 10, 30, time_unit="invalid")
    with raises(Exception):
        fast_deadband(input_1, 10, 30, deadband_type="invalid")
    assert fast_deadband(input_1, 10, 30, deadband_type="percent") == output_2
    assert fast_deadband(input_1, 10, 30, 5) == output_3
    assert fast_deadband(input_1, 10, 30000, time_unit="ms") == output_1
    assert fast_deadband(input_1, 10, 30000000, time_unit="us") == output_1
    assert fast_deadband(input_2, 10, 30) == output_4
