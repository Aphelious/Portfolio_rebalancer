import yfinance as yf

'''Portfolio Rebalancer

Module level documentation

This Module is written for the purpose of retrieving current stock price data, arranging it into current positions
and composing a portfolio based on those positions. General statistics are generated computing the returns of the various
positions in absolute and relative terms. Then an analysis is done to compare the current portfolio allocations to an
ideal or pre-scribed allocation. The script then outputs directions for buys/sells to bring the portfolio
back into balance. The implementation consists of three classes: Portfolio, Position, and Transaction. Portfolio objects are
composed of Position objects. Position objects are composed of Transaction objects Most methods, such as Buys and Sells,
Calculate Total Return, etc. belong to Positions. The methods of rebalancing are methods of the Portfolio class and
mostly they simply call the appropriate subclasses' methods to the extent they are needed. All dates and times are in
the form of aware datetime objects to preserve accuracy of prices in market that often fluctuate by the minute. This
also makes it easier to pass those attributes to other library's methods, specifically the yFinance library, of which
this module makes heavy use.

This script requires the yFinance and Datetime libraries

'''


def get_latest_price(ticker):
    data = yf.Ticker(ticker)
    latest_price = data.history(period='2d')
    return round(latest_price['Close'][0], 2)


class Portfolio:
    '''This class represents an entire Portfolio of assets. It is composed of Position objects and contains only those
     methods that act on multiple Position objects. Multiple Portfolio objects can be saved to the database for comparison
     purposes using some global functions defined elsewhere. Every time a Portfolio object is instantiated the database
     is checked for a record of the same name. If found, a 'branch' of that object is created as a separate entity and
     both are updated with current information. This allows for comparison between different versions of the same
     portfolio.

    Methods:

    list_positions()
        calls each Position object's get_info() and position_return() methods and prints.

    current_allocation()
        Prints a dictionary where investment Categories are the keys and the values are the percentage that category
        makes up of the total portfolio value.
     '''


    def __init__(self, positions):
        self.positions = positions  # This is a list of Position objects composed of lists of Transaction objects.
        self.total_postiions = len(self.positions)
        self.total_return = 0
        for position in self.positions:
            self.total_return += position.position_return()


    def list_positions(self):
        '''Prints Position info and return info by calling get_info() and position_return() on all position objects
         in the portfolio. '''

        for position in self.positions:
            print(position.get_info())
            print(position.postition_return())
            print()

    def current_allocation(self) -> dict:
        '''Groups all Positions by Investment Category, totals each category amount and inserts the values into a
        dictionary. A total amount is calculated from the summing the dictionary values which is then used to calculate
        each category's percentage of the total. Returns a dict type.'''

        allocation_dict = {}
        for position in self.positions:
            if position.status == 'Open':
                if position.category in allocation_dict:
                    allocation_dict[position.category] += position.total_amount
                else:
                    allocation_dict[position.category] = position.total_amount
        total_value = sum(allocation_dict.values())
        for category in allocation_dict:
            allocation_dict[category] = round(allocation_dict[category]/total_value, 2)
        for key, value in allocation_dict.items():
            print(f'{key}:{value * 100}%')
        return allocation_dict  # Right now the main output is printing text to the screen. Once a GUI is establshed,
                                # these return types will be updated


    def __str__(self):
        return f'This Portfolio consists of {self.total_postiions} posititons.\n' \
               f'The total return of the Portfolio to date is: ${round(self.total_return, 2)}\n'


class Position:
    '''This class combines all transaction events of a particular stock in a list. These events include Buys, Sells,
    and Dividend Reinvestments. Each transaction has a return on investment associated with it. The ROI is calculated
    by comparing buy price to the sell price and any dividends incurred during the holding period. If there is no sell
    event recorded, the current price is used. The ROIs of all transactions are weight-averaged to make up the total
    Position return, but each transaction ROI can be accessed using the 'list_transaction_retuns()' method.

    Methods:

    method: get_info
        Calculate the total number of transactions currently making up the position, display the name and ticker symbol
        of the position.
    '''


    def __init__(self, transactions):
        self.transactions = transactions  # This is a list of transaction objects queried from the database
        self.total_transactions = len(self.transactions)
        self.ticker = self.transactions[0].ticker
        self.name = self.transactions[0].investment_name
        self.category = self.transactions[0].category
        self.total_shares = 0
        self.total_amount = 0
        self.status = 'Closed'
        self.latest_price = get_latest_price(self.ticker)
        for transaction in self.transactions:
            self.total_shares += transaction.shares
            self.total_amount += transaction.principal_amount
        if self.total_shares > 0:
            self.status = 'Open'


    def get_info(self):
        '''Return basic information about the investment position: Investment name, Ticker, Category, Total number
        of transactions, and Status(Open or Closed).'''

        return f'Investment name: {self.name}\n' \
               f'Ticker: {self.ticker}\n' \
               f'Category: {self.category}\n' \
               f'Total number of transactions: {self.total_transactions}\n' \
               f'Position status: {self.status}'


    def position_return(self):
        if self.status == 'Open':
            position_return = round((self.total_shares * self.latest_price) - abs(self.total_amount), 2)
            return position_return
        else:
            return round(abs(self.total_amount), 2)


    def list_transactions_returns(self):
        returns = {}
        for transaction in self.transactions:
            if transaction.trans_type != 'Sell':
                buy_price = transaction.share_price
                buy_shares = transaction.shares
                buy_amount = buy_price * buy_shares
                current_value = buy_shares * self.latest_price
                transaction_return = round((current_value - buy_amount), 2)
                returns.update({transaction.id: transaction_return})
        return returns