from generate_timeseries import gerar_timeseries
from plots import plotar_timeseries
import datetime

if __name__ == "__main__":
    start = datetime.datetime(2025, 1, 1, 0, 0, 0)
    end = datetime.datetime(2025, 1, 1, 1, 0, 0)
    seed = 42
    
    dados = gerar_timeseries(seed, start, end)
    plotar_timeseries(dados)