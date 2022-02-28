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


class Portfolio:
    '''This class represents an entire Portfolio of assets. It is composed of Position objects and contains only those
     methods that act on multiple Position objects. Multiple Portfolio objects can be saved to the database for comparison
     purposes using some global functions defined elsewhere. Every time a Portfolio object is instantiated the database
     is checked for a record of the same name. If found, a 'branch' of that object is created as a separate entity and
     both are updated with current information. This allows for comparison between different versions of the same
     portfolio.

    Methods

    total return:
        calls each Position object's calculate_position_return() method and outputs a formatted list

     '''

    def __init__(self, positions):
        self.positions = positions

    def total_return(self):
        # TODO: write total return of Portfolio function
        pass

    def compare_allocations(self):
        # TODO: write compare allocations function
        pass


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
        self.transactions = transactions  # This is a list of transaction objects, queried from the database
        self.total_transactions = len(self.transactions)
        self.ticker = self.transactions[0].ticker
        self.name = self.transactions[0].investment_name
        self.category = self.transactions[0].category
        self.total_shares = 0
        self.total_amount = 0
        self.status = 'Closed'
        data = yf.Ticker(self.ticker)
        latest_price = data.history(period='2d')
        self.current_price = round(latest_price['Close'][0], 2)
        for transaction in self.transactions:
            self.total_shares += transaction.shares
            self.total_amount += transaction.principal_amount
        if self.total_shares > 0:
            self.status = 'Open'



    def get_info(self):
        '''Return basic information about the investment position: Investment name, Ticker, Category, Total number
        of transactions, and Status(Open or Closed).'''

        return f'Investment name: {self.name}\nTicker: {self.ticker}\nCategory: {self.category}\n' \
               f'Total number of transactions: {self.total_transactions}\n' \
               f'Position status: {self.status}'


    def postition_return(self):
        position_return = round((self.total_shares * self.current_price)-self.total_amount, 2)
        return f'Total position return: ${position_return}'

    def list_transactions_returns(self):
        returns = {}
        for transaction in self.transactions:
            if transaction.trans_type != 'Sell':
                buy_price = transaction.share_price
                buy_shares = transaction.shares
                buy_amount = buy_price * buy_shares
                current_value = buy_shares * self.current_price
                transaction_return = round((current_value - buy_amount), 2)
                returns.update({transaction.id: transaction_return})
        return returns