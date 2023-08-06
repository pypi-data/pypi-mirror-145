# from binance import Client
# import pandas as pd 


def getminutedata( symbol, interval='1m', lookback="300" ):

    from binance import Client
    import pandas as pd 
    
    frame = pd.DataFrame( client.get_historical_klines( symbol , interval, lookback + " min ago UTC") )
    
    frame = frame.iloc[ : , : 6]
    frame.columns = ['Time', 'Open', 'High', 'Lows', 'Close', 'Volume']
    
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime( frame.index, unit='ms' )
    
    frame = frame.astype( float )
    return frame

    






# ---------------------------------------------
def fib(n):   # return Fibonacci series up to n
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a+b
    return result


# -------------------------------------------



if __name__ == '__main__':
    pass
