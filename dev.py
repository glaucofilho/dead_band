from src import slow_deadband
from resources import generate_timeseries
import datetime
import time


if __name__ == "__main__":
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 31, 23, 59, 59, 999)
    seed = 42

    ts_i = time.time()
    data = generate_timeseries(seed, start, end)
    ts_f = time.time()
    duration = ts_f - ts_i
    print(f"{duration:.4f} seconds to generate the time series")

    ts_i = time.time()
    filtered_data = slow_deadband(data, 10, 30)
    ts_f = time.time()
    duration = ts_f - ts_i
    print(f"{duration:.4f} seconds to filter data")

    ts_i = time.time()
    data = generate_timeseries(seed, start, end, generate_quality=False)
    ts_f = time.time()
    duration = ts_f - ts_i
    print(
        f"{duration:.4f} seconds to generate the time series without quality"
    )

    ts_i = time.time()
    filtered_data = slow_deadband(data, 10, 30)
    ts_f = time.time()
    duration = ts_f - ts_i
    print(f"{duration:.4f} seconds to filter data without quality")
