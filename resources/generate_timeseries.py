import random
import datetime


def generate_timeseries(
    seed,
    start_time,
    end_time,
    start_value=0,
    start_quality=1,
    bad_quality_weight=0.1,
    generate_quality=True,
):
    """
    Generates a time series simulating sensor readings with continuous variation.

    The generated series is deterministic based on the provided seed. The values simulate
    readings that fluctuate slightly around the previous value (sensor with natural noise),
    with random time intervals between 100ms and 15s.

    Args:
        seed (int): Seed for the random number generator.
        start_time (datetime.datetime): Initial timestamp of the series.
        end_time (datetime.datetime): Final timestamp of the series.
        start_value (float, optional): Initial value of the series. Default is 0.
        start_quality (int, optional): Initial quality of the series (0 or 1). Default is 1.
        bad_quality_weight (float, optional): Probability of bad qualities. Value between 0 and 1. Default is 0.1.
        generate_quality (bool, optional): If True, generates quality values. Default is True.

    Returns:
        list: List of tuples (value: float, timestamp: datetime.datetime, quality: int)
    """  # noqa: E501
    random.seed(seed)

    series = []
    current_time = start_time
    value = start_value
    quality = start_quality
    if generate_quality:
        series.append((value, current_time, quality))
    else:
        series.append((value, current_time))

    while current_time <= end_time:
        value = value + random.uniform(-10, 10)
        quality = 1 if random.random() >= bad_quality_weight else 0
        interval = random.randint(100, 15000) / 1000
        current_time += datetime.timedelta(seconds=interval)
        if generate_quality:
            series.append((value, current_time, quality))
        else:
            series.append((value, current_time))
    return series


if __name__ == "__main__":
    start = datetime.datetime(2025, 1, 1, 0, 0, 0)
    end = datetime.datetime(2025, 1, 1, 1, 0, 0)
    seed = 42

    data = generate_timeseries(seed, start, end)
    for d in data:
        print(d)
