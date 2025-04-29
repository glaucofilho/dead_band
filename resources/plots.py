import matplotlib.pyplot as plt

def plotar_timeseries(series, file_name='grafico'):
    """
    Plota a série temporal de valores gerados.
    
    Args:
        series (list): Lista de tuplas (valor: float, timestamp: datetime.datetime)
    """
    valores = [item[0] for item in series]
    tempos = [item[1] for item in series]

    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(tempos, valores, label="Valor", marker='o')

    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Valor")
    ax.set_title("Série Temporal Gerada")
    ax.legend()
    ax.grid(True)
    fig.autofmt_xdate()
    plt.savefig(f'./resources/png/{file_name}.png')
