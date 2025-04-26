import random
import datetime

def gerar_timeseries(seed, start_time, end_time, start_value=0, start_quality=0):
    """
    Gera uma série temporal simulando leituras de sensores com variação contínua.
    
    A série gerada é determinística baseada na seed fornecida. Os valores simulam
    leituras que flutuam levemente ao redor do valor anterior (sensor com ruído natural),
    com intervalos de tempo aleatórios entre 100ms e 15s.
    
    Args:
        seed (int): Seed para o gerador de números aleatórios.
        start_time (datetime.datetime): Timestamp inicial da série.
        end_time (datetime.datetime): Timestamp final da série.
        start_value (float, opcional): Valor inicial da série. Default é 0.
        start_quality (int, opcional): Qualidade inicial da série (0 ou 1). Default é 0.
        
    Returns:
        list: Lista de tuplas (valor: float, timestamp: datetime.datetime, qualidade: int)
    """
    random.seed(seed)
    
    series = []
    current_time = start_time
    valor = start_value
    qualidade = start_quality
    series.append((valor, current_time, qualidade))
    
    while current_time <= end_time:
        valor = valor + random.uniform(-10, 10)
        qualidade = random.choice([0, 1])
        intervalo = random.randint(100, 15000) / 1000
        current_time += datetime.timedelta(seconds=intervalo)
        series.append((valor, current_time, qualidade))
    
    return series

if __name__ == "__main__":
    start = datetime.datetime(2025, 1, 1, 0, 0, 0)
    end = datetime.datetime(2025, 1, 1, 1, 0, 0)
    seed = 42
    
    dados = gerar_timeseries(seed, start, end)
    for d in dados:
        print(d)