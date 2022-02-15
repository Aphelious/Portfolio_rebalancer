import csv
from datetime import datetime


# Create objects from csv:

def transactions_from_csv(csv_filepath):
    '''When supplied a csv filepath, read csv file using csv.DictReader to automatically pair column names with
    comma-separated values. Column names must be identical to Transaction class attributes/SQLalchemy-mapped columns
    in models.py ie: account, trade_date, settlement_date, trans_type, investment_name, category, ticker, shares,
    share_price, amount, principal_amount. This function also creates date objects from the csv values where applicable.'''

    with open(csv_filepath, newline='', mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for i in row:
                try:
                    data = row.get(i)
                    date = datetime.strptime(data, '%Y-%m-%d')
                    row.update({i: date})
                except:
                    continue
            transaction = Transaction(**row)
            session.add(transaction)
        session.commit()