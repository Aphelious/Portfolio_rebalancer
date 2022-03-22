from env import *
import csv
from datetime import datetime
from models import Transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine(f'sqlite:///transactions.db', echo=False, future=True)
session = Session(engine)

# Steps for parsing and interpreting csv/any input:

# Check the file format/extension
# Check file contents?
# Determine Delimiter
# Determine line break: CR, LF, or CRLF
# Determine encoding
# Determine UTF character at start or not
# Open and read in contents
# Check if a header exists
# Check if missing data
# Handle rows of missing data
# Assign data type to column based on header info?
# Check if Column data matches header data type


# Read rows directly from cvs into kwarg:value pairs, then to the session to be instantiated and added to db using
# Sqlalchemy orm:

def transactions_from_csv(csv_filepath):
    with open(csv_filepath, 'r', newline='', encoding='utf-8-sig') as csvfile:
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
