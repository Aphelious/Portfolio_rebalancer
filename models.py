from sqlalchemy import Column, Integer, String, Float, Date, create_engine
from sqlalchemy.orm import declarative_base, reconstructor, Session
import yfinance as yf


engine = create_engine(f'sqlite:///transactions.db', echo=True, future=True)
Base = declarative_base()


# Set up SQLAlchemy Mapping for the Transaction class:

class Transaction(Base):
    '''Models distinct purchase, sell, or dividend re-invesment events of a particular stock or etf. This is the most
    fine-grained data that the program works with. This class is used to create objects directly from well-formatted
    csv files commonly output by investment brokerage APIs. By first modeling the individual transactions a portfolio
    has made the program can incorporate the full timeline of investment decisions into the current state of the
    portfolio. This affords the user more data and a greater set of features to determine performance.

    For example, if one buys 10 shares of XYZ on Monday and 10 shares of XYZ on Tuesday it is rational to consider those
    independent positions due to the fact that the price was likely different. Even it the price was exactly the same,
    modeling a portfolio this way allows us to capture the different purchase events in the datetimes, which is useful
    information to store.

    Attributes
    ------------
    account : int
        the account number that the investment is held in

    trade_date : datetime object
        a naive datetime object of the transaction initiation date and time, buy or sell, of the stock

    settlement_date : datetime object
        a naive datetime object of the transaction fulfillment date and time, buy or sell, of the stock

    trans_type : str
        the type of transaction, eg) 'Buy', 'Sell', 'Dividend Reinvestment'

    investment_name : str
        the name of the fund, etf, or name of the company

    category : str
        the sector or asset class that the investment is a part of, eg) 'Small-cap value', 'Large-cap Tech'

    ticker : str
        the stock ticker symbol of the company, mutual fund, etf, or other publicly traded investment vehicle

    shares : float
        the number of shares purchased or sold

    share_price : float
        the price at which the transaction was executed

    amount : float
        the total cost of the transaction as a multiple of shares times price/share

    principal_amount : float
        the total cost of the transaction as a multiple of shares times price/share, preserves sign (+ or -) of the
        transaction, indicating whether it was a buy or sell. This is mostly a duplicate of 'amount' but it might be
        useful for methods to keep it in this form

    Methods
    ---------

    get_latest_price()
        uses yfinance to fetch the price of the ticker at a specific date
    '''

    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, unique=True)
    account = Column(Integer)
    trade_date = Column(Date)
    settlement_date = Column(Date)
    trans_type = Column(String)
    investment_name = Column(String)
    category = Column(String)
    ticker = Column(String)
    shares = Column(Float)
    share_price = Column(Float)
    amount = Column(Float)
    principal_amount = Column(Float)

    def __str__(self):
        return f'{self.id}, {self.settlement_date}, {self.trans_type}, {self.investment_name}, {self.category},' \
               f' {self.ticker}, {self.shares}, {self.share_price}, {self.amount}, {self.principal_amount}'

    def __add__(self, other):
        if type(other) != Transaction:
            raise TypeError
        else:
            try:
                new_amount = self.amount + other.amount
                new_current_value = self.current_value + other.current_value
                new_profit = self.profit + other.profit
                return (new_amount, new_current_value, new_profit)
            except:
                raise ValueError

    def get_average_price(self):
        data = yf.Ticker(self.ticker)
        latest_price = data.history(period='1d')
        low = latest_price['Low'][0]
        high = latest_price['High'][0]
        average = (low + high) / 2
        return round(average, 2)

    def get_latest_price(self):
        data = yf.Ticker(self.ticker)
        latest_price = data.history(period='2d')
        return round(latest_price['Close'][0], 2)

    # @reconstructor
    # def init_on_load(self):
    #     '''Add two instance-level attributes to the Transaction object upon recreation from the database. Attribute
    #     values will be set upon instantiation of the Portfolio object.'''
    #     self.value_now = None
    #     self.return_ = None
