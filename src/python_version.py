def apply_deadband(
    series,
    deadband_value,
    max_time_interval,
    min_time_interval=0,
    time_unit="s",
    deadband_type="abs",
    save_on_quality_change=True,
):
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

    Returns:
        list: New list of tuples with the same structure as input (with or without quality) after applying the deadband filter.
    """  # noqa: E501
    if not series:
        return []

    if time_unit == "s":
        multiplier = 1_000_000
    elif time_unit == "ms":
        multiplier = 1_000
    elif time_unit == "us":
        multiplier = 1
    else:
        raise ValueError("time_unit must be 's', 'ms', or 'us'")

    if deadband_type not in ["abs", "percent"]:
        raise ValueError("deadband_type must be 'abs' or 'percent'")

    min_time_interval_us = min_time_interval * multiplier
    max_time_interval_us = max_time_interval * multiplier

    has_quality = len(series[0]) == 3

    filtered_series = [series[0]]
    if has_quality:
        last_value, last_timestamp, last_quality = series[0]
    else:
        last_value, last_timestamp = series[0]
        last_quality = None

    for point in series[1:]:
        if has_quality:
            value, timestamp, quality = point
        else:
            value, timestamp = point
            quality = None

        time_delta_us = (
            timestamp - last_timestamp
        ).total_seconds() * 1_000_000

        if deadband_type == "abs":
            variation = abs(value - last_value)
        else:
            if last_value == 0:
                variation = abs(value)
            else:
                variation = abs(value - last_value) / abs(last_value) * 100

        should_save = False

        if time_delta_us < min_time_interval_us:
            should_save = False
        elif (
            has_quality and save_on_quality_change and quality != last_quality
        ):
            should_save = True
        elif variation > deadband_value:
            should_save = True
        elif time_delta_us >= max_time_interval_us:
            should_save = True

        if should_save:
            filtered_series.append(point)
            last_value = value
            last_timestamp = timestamp
            if has_quality:
                last_quality = quality

    return filtered_series
