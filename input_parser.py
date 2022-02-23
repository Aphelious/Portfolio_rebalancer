from env import *
import csv
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine(db_file)
session = Session(engine)

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
