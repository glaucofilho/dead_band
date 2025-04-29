import matplotlib.pyplot as plt

def plot_timeseries(series, file_name='plot'):
    """
    Plots the generated time series of values.
    
    Args:
        series (list): List of tuples (value: float, timestamp: datetime.datetime)
    """
    values = [item[0] for item in series]
    times = [item[1] for item in series]

    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(times, values, label="Value", marker='o')

    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Value")
    ax.set_title("Generated Time Series")
    ax.legend()
    ax.grid(True)
    fig.autofmt_xdate()
    plt.savefig(f'./resources/png/{file_name}.png')
