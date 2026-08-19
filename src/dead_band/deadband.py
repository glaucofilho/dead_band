import warnings
from datetime import datetime
from typing import List, Optional, Sequence, Tuple, Union, cast

try:
    from .cython_modules.c_deadband import (  # type: ignore[import-not-found]
        apply_c_deadband,
    )

    CYTHON_AVAILABLE = True
except ImportError:  # pragma: no cover
    # The compiled extension is missing. That happens only when the package
    # was built from source on a platform with no published wheel and no
    # compiler. The pure-Python implementation below produces identical
    # results, so degrade to it rather than failing the import outright.
    apply_c_deadband = None  # type: ignore[assignment]
    CYTHON_AVAILABLE = False
    warnings.warn(
        "dead_band: the compiled extension is unavailable, falling back "
        "to the pure-Python implementation, which is substantially slower. "
        "Reinstall from a wheel to get the accelerated path.",
        RuntimeWarning,
        stacklevel=2,
    )

# A point is (value, timestamp) or (value, timestamp, quality).
PointNoQuality = Tuple[float, datetime]
PointWithQuality = Tuple[float, datetime, Optional[int]]
DataPoint = Union[PointNoQuality, PointWithQuality]


def apply_deadband(
    series: Sequence[DataPoint],
    deadband_value: float,
    max_time_interval: float,
    min_time_interval: float = 0,
    time_unit: str = "s",
    deadband_type: str = "abs",
    save_on_quality_change: bool = True,
    use_cython: bool = True,
) -> List[DataPoint]:
    """
    Applies a deadband filter to a time series, considering value variation, time intervals (in selectable units), and optional quality changes.

    Args:
        series (list): List of tuples (value: float, timestamp: datetime.datetime, quality: Optional[int]). Quality can be omitted (value, timestamp) or included (value, timestamp, quality).
        deadband_value (float): Deadband threshold (absolute value or percentage, depending on deadband_type).
        max_time_interval (float): Maximum time interval (unit defined by time_unit) to force saving a new point.
        min_time_interval (float): Minimum time interval (unit defined by time_unit) to allow saving a new point even with small variation. Default is 0.
        time_unit (str): Unit for time intervals: 's' (seconds), 'ms' (milliseconds), or 'us' (microseconds). Default is 's'.
        deadband_type (str): 'abs' for absolute deadband or 'percent' for percentage-based deadband. Default is 'abs'.
        save_on_quality_change (bool): If True, saves a point whenever the quality changes compared to the last saved point. Only used when quality is provided in the series. Default is True.
        use_cython (bool): If True, uses the Cython implementation for performance, when it is available. Falls back to the pure-Python implementation if the compiled extension is missing; check dead_band.CYTHON_AVAILABLE to tell which path is active. Default is True.

    Returns:
        list: New list of tuples with the same structure as input (with or without quality) after applying the deadband filter.
    """  # noqa: E501
    if use_cython and CYTHON_AVAILABLE:
        return apply_c_deadband(
            series,
            deadband_value,
            max_time_interval,
            min_time_interval,
            time_unit,
            deadband_type,
            save_on_quality_change,
        )

    if not series:
        return []

    # Convert time units once
    if time_unit == "s":
        multiplier = 1_000_000
    elif time_unit == "ms":
        multiplier = 1_000
    elif time_unit == "us":
        multiplier = 1
    else:
        raise ValueError("time_unit must be 's', 'ms', or 'us'")

    min_time_interval_us = min_time_interval * multiplier
    max_time_interval_us = max_time_interval * multiplier

    if deadband_type == "abs":

        def calc_variation(current, last):
            return abs(current - last)

    elif deadband_type == "percent":

        def calc_variation(current, last):
            return (
                abs(current - last) / abs(last) * 100
                if last != 0
                else abs(current)
            )

    else:
        raise ValueError("deadband_type must be 'abs' or 'percent'")

    has_quality = len(series[0]) == 3

    if not has_quality:
        # `has_quality` is the runtime witness for these casts: every point in
        # the series has the same arity as the first one.
        plain = cast(Sequence[PointNoQuality], series)
        filtered_series: List[DataPoint] = [plain[0]]
        last_value, last_timestamp = plain[0]

        for point in plain[1:]:
            value, timestamp = point
            time_delta_us = (
                timestamp - last_timestamp
            ).total_seconds() * 1_000_000

            if time_delta_us >= min_time_interval_us:
                variation = calc_variation(value, last_value)
                if (
                    variation > deadband_value
                    or time_delta_us >= max_time_interval_us
                ):
                    filtered_series.append(point)
                    last_value, last_timestamp = value, timestamp
        return filtered_series

    with_quality = cast(Sequence[PointWithQuality], series)
    filtered_series = [with_quality[0]]
    last_value, last_timestamp, last_quality = with_quality[0]

    for qpoint in with_quality[1:]:
        value, timestamp, quality = qpoint
        time_delta_us = (
            timestamp - last_timestamp
        ).total_seconds() * 1_000_000

        if time_delta_us < min_time_interval_us:
            continue

        if save_on_quality_change and quality != last_quality:
            filtered_series.append(qpoint)
            last_value, last_timestamp, last_quality = (
                value,
                timestamp,
                quality,
            )
            continue

        variation = calc_variation(value, last_value)
        if variation > deadband_value or time_delta_us >= max_time_interval_us:
            filtered_series.append(qpoint)
            last_value, last_timestamp, last_quality = (
                value,
                timestamp,
                quality,
            )

    return filtered_series
