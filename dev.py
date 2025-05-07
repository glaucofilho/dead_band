from dead_band import apply_deadband
from resources import generate_timeseries
import datetime
import time
import csv

start = datetime.datetime(2020, 1, 1, 0, 0, 0)
end = datetime.datetime(2020, 12, 31, 23, 59, 59, 999)
seed = 42
dead_band_value = 10
max_time_invertal = 30

def generate_csv_file(filename, data):
    with open(f"{filename}.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["value", "timestamp", "quality"])
        for row in data:
            formatted_row = list(row)
            formatted_row[1] = formatted_row[1].isoformat()
            writer.writerow(formatted_row)

def try_slow_deadband():
    data = generate_timeseries(seed, start, end)
    ts_i = time.time()
    filtered_data = apply_deadband(data, dead_band_value, max_time_invertal, use_cython=False)
    ts_f = time.time()
    duration = ts_f - ts_i
    print(f"{duration:.4f} seconds to filter data")

    data = generate_timeseries(seed, start, end, generate_quality=False)
    ts_i = time.time()
    filtered_data = apply_deadband(data, dead_band_value, max_time_invertal, use_cython=False)
    ts_f = time.time()
    duration = ts_f - ts_i
    print(f"{duration:.4f} seconds to filter data without quality")
    return duration

def try_fast_deadband():
    data = generate_timeseries(seed, start, end)
    ts_i = time.time()
    filtered_data = apply_deadband(data, dead_band_value, max_time_invertal)
    ts_f = time.time()
    generate_csv_file("filtered_data", filtered_data)
    generate_csv_file("data", data)
    duration = ts_f - ts_i
    print(f"{duration:.4f} seconds to filter data")

    data = generate_timeseries(seed, start, end, generate_quality=False)
    ts_i = time.time()
    filtered_data = apply_deadband(data, dead_band_value, max_time_invertal)
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