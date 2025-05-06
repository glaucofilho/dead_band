from src.dead_band import slow_deadband, fast_deadband
from resources import generate_timeseries
import datetime
import time

start = datetime.datetime(2020, 1, 1, 0, 0, 0)
end = datetime.datetime(2020, 12, 31, 23, 59, 59, 999)
seed = 42
dead_band_value = 10
max_time_invertal = 30

def try_slow_deadband():
    data = generate_timeseries(seed, start, end)
    ts_i = time.time()
    filtered_data = slow_deadband(data, dead_band_value, max_time_invertal)
    ts_f = time.time()
    duration = ts_f - ts_i
    print(f"{duration:.4f} seconds to filter data")

    data = generate_timeseries(seed, start, end, generate_quality=False)
    ts_i = time.time()
    filtered_data = slow_deadband(data, dead_band_value, max_time_invertal)
    ts_f = time.time()
    duration = ts_f - ts_i
    print(f"{duration:.4f} seconds to filter data without quality")
    return duration

def try_fast_deadband():
    data = generate_timeseries(seed, start, end)
    ts_i = time.time()
    filtered_data = fast_deadband(data, dead_band_value, max_time_invertal)
    ts_f = time.time()
    duration = ts_f - ts_i
    print(f"{duration:.4f} seconds to filter data")

    data = generate_timeseries(seed, start, end, generate_quality=False)
    ts_i = time.time()
    filtered_data = fast_deadband(data, dead_band_value, max_time_invertal)
    ts_f = time.time()
    duration = ts_f - ts_i
    print(f"{duration:.4f} seconds to filter data without quality")
    return duration


if __name__ == "__main__":
    print("Testing slow deadband")
    slow = try_slow_deadband()
    print("=" * 60)
    print("Testing fast deadband")
    fast = try_fast_deadband()
    print("=" * 60)
    percent = ((slow - fast) / slow )* 100
    print(f"Fast deadband is {percent:.2f}% faster than slow deadband")