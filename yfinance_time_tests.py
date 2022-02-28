import yfinance as yf
import time



def get_latest_price_1day(ticker):
    # Strategy that I know works for stocks and ETFs:
    start = time.time()
    data = yf.Ticker(ticker)
    price_history = data.history(period='1d', rounding=True)
    latest_price = price_history['Close'][0]
    print(f'One-day History Strategy: {latest_price}')
    end = time.time()
    print(f'Time to run One-Day History Strategy: {end - start}')


def get_latest_price_2day(ticker):
    # Strategy for Mutual funds (2 days):
    start = time.time()
    data = yf.Ticker(ticker)
    price_history = data.history(period='2d', rounding=True)
    latest_price = round(price_history['Close'][0], 2)
    print(f'Two-day History Strategy: {latest_price}')
    end = time.time()
    print(f'Time to run Two-Day History Strategy: {end - start}')

def get_latest_price_tail(ticker):
    # Different implementation (Fastest, but inaccurate):
    start = time.time()
    data = yf.Ticker(ticker)
    price_history = data.history(rounding=True)
    latest_price = price_history.tail(10)['Close'].iloc[0]
    print(f'Tail Strategy: {latest_price}')
    end = time.time()
    print(f'Time to run Tail Strategy: {end - start}')

def get_latest_price_market_price(ticker):
    # Yet another implementation (very slow):
    start = time.time()
    data = yf.Ticker(ticker)
    latest_price = data.info['regularMarketPrice']
    print(f'Market Price Strategy: {latest_price}')
    end = time.time()
    print(f'Time to run Market Price Strategy: {end - start}')


def get_current_price(ticker):
    print(f'Fetching latest price for ticker: {ticker}')
    try:
        get_latest_price_1day(ticker)
    except:
        print(f'One-day strategy did not work')

    get_latest_price_2day(ticker)
    get_latest_price_tail(ticker)
    get_latest_price_market_price(ticker)

get_current_price('VFFVX')

