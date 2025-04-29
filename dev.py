
from resources import generate_timeseries, plot_timeseries
from src import slow_deadband
import datetime

if __name__ == "__main__":
    start = datetime.datetime(2025, 1, 1, 0, 0, 0)
    end = datetime.datetime(2025, 1, 1, 1, 0, 0)
    seed = 42
    
    dados = generate_timeseries(seed, start, end)
    dados_comprimidos = slow_deadband(dados, deadband_value=10, max_time_interval=30)
    print(len(dados))
    print(len(dados_comprimidos))
    plot_timeseries(dados)
    plot_timeseries(dados_comprimidos,"grafico_comprimido")