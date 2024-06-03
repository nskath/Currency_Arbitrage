import numpy as np
import yfinance as yf

def get_exchange_rates(currencies):
    exchange_rates = np.full((len(currencies), len(currencies)), np.inf)
    
    for i, c1 in enumerate(currencies):
        for j, c2 in enumerate(currencies):
            if i == j:
                exchange_rates[i][j] = 1
            else:
                ticker = f"{c1}{c2}=X"
                data = yf.download(ticker, period="1d", interval="1m")
                if not data.empty:
                    rate = data['Close'].iloc[-1]
                    exchange_rates[i][j] = rate
                else:
                    print(f"No exchange rate data available for {c1} to {c2}, skipping.")
    
    return exchange_rates, currencies

def floyd_warshall(graph):
    n = len(graph)
    dist = np.copy(graph)
    next_node = np.full((n, n), -1, dtype=int)
    
    for i in range(n):
        for j in range(n):
            if i != j and graph[i][j] != np.inf:
                next_node[i][j] = j
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]
    
    return dist, next_node

def reconstruct_path(next_node, start, exchange_rates):
    path = [start]
    conversion_path = [1]
    next_index = next_node[start][start]
    current_value = 1
    
    while next_index != -1 and next_index != start:
        current_value *= exchange_rates[path[-1]][next_index]
        conversion_path.append(current_value)
        path.append(next_index)
        next_index = next_node[next_index][start]
    
    current_value *= exchange_rates[path[-1]][start]
    path.append(start)
    conversion_path.append(current_value)
    
    return path, conversion_path

def detect_arbitrage(rates, currencies):
    log_rates = -np.log(rates)
    dist, next_node = floyd_warshall(log_rates)
    
    n = len(dist)
    
    for i in range(n):
        if dist[i][i] < 0:
            path, conversion_path = reconstruct_path(next_node, i, rates)
            print("Arbitrage opportunity detected:")
            for p, c in zip(path, conversion_path):
                print(f"{currencies[p]} ({c})", end=" -> ")
            print(f"{currencies[path[0]]} ({conversion_path[-1]})")
            return True
    
    return False

# currency pairs to check
currencies = ['USD', 'EUR', 'JPY', 'GBP', 'INR', 'AUD', 'CAD', 'CHF', 'CNY', 'SEK']

try:
    exchange_rates, currencies = get_exchange_rates(currencies)
    arbitrage_exists = detect_arbitrage(exchange_rates, currencies)
    if not arbitrage_exists:
        print("No arbitrage opportunity found.")
except Exception as e:
    print(f"An error occurred: {e}")
