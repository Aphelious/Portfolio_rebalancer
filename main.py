from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, declarative_base
from models import Transaction
from classes import Position, Portfolio



engine = create_engine(f'sqlite:///transactions.db', echo=False, future=True)
Base = declarative_base()

# def get_current_price(ticker):
    # # Strategy that I know works:
    # data = yf.Ticker(self.ticker)
    # latest_price = data.history(period='1d')
    # self.current_price = round(latest_price['Close'][0], 2)

    # # Strategy for Mutual funds:
    # data = yf.Ticker(self.ticker)
    # latest_price = data.history(period='2d')
    # self.current_price = round(latest_price['Close'][0], 2)

    # # Different implementation:
    # data = yf.Ticker(ticker)
    # latest_price = data.history()
    # last_quote = latest_price.tail(1)['Close'].iloc[0]
    # return last_quote

# Create a function to compose Positions

def get_latest_price():
    data = yf.Ticker(ticker)
    latest_price = data.history(period='2d')
    return round(latest_price['Close'][0], 2)

tickers = []

with Session(engine) as session:
    result = session.execute(select(Transaction.ticker).group_by(Transaction.ticker))
    for row in result:
        tickers.append(row[0])

positions = []
with Session(engine) as session:
    for item in tickers:
        result = session.execute(select(Transaction).where(Transaction.ticker == item).order_by(Transaction.settlement_date))
        transactions = []
        for row in result:
            transactions.append(row[0])
        position = Position(transactions)
        positions.append(position)


portfolio = Portfolio(positions)
print(portfolio)
print(portfolio.total_return)

