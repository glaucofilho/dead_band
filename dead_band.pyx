import pandas as pd
import numpy as np

def compress_dataframe_cython(df, last_valid_value=-99999999, last_valid_timestamp=0, last_valid_quality=-1, dead_band=0.000001, min_time=0, max_time=3600):
    cdef int i
    cdef float diff
    cdef double[:] values
    cdef list compressed_data = []
    cdef long long[:] timestamps
    cdef long long[:] qualities

    min_time = 1000*min_time
    max_time = 1000*max_time

    values = df['Value'].to_numpy()
    qualities = df['Quality'].to_numpy()
    df["Timestamp"] = df["Timestamp"].apply(lambda x: int(x.timestamp() * 1000))
    timestamps = df["Timestamp"].to_numpy()

    for i in range(len(values)):
        if i == 0:
            compressed_data.append([timestamps[i], values[i], qualities[i]])
            last_valid_value = values[i]
            last_valid_timestamp = timestamps[i]
            last_valid_quality = qualities[i]
        else:
            diff = values[i] - last_valid_value
            diff_time = timestamps[i] - last_valid_timestamp
            diff_quality = qualities[i] - last_valid_quality

            if abs(diff_time) > max_time or abs(diff) > dead_band or diff_quality != 0:
                if abs(diff_time) > min_time:
                    compressed_data.append([timestamps[i], values[i], qualities[i]])
                    last_valid_value = values[i]
                    last_valid_timestamp = timestamps[i]
                    last_valid_quality = qualities[i]
    return compressed_data
