import uuid

from DataModel.BaseDM import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from DataModel.Books import Books
from DataModel.Members import Members
from DataModel.Transactions import Transactions
from uuid import uuid4
import json

class ActiveSession:
    engine = create_engine('mssql+pyodbc://' + 'LAPTOP-LC07V53A/LibrarySys?' + 'driver=SQL+Server+Native+Client+11.0')
    Session = sessionmaker(bind=engine)
    Session = Session()
    Base.metadata.create_all(engine)

def strip_json_keys(obj):
    if isinstance(obj, dict):
        return {key.strip(): strip_json_keys(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [strip_json_keys(element) for element in obj]
    else:
        return obj

def RunTestClass():
    books =[]
    with open('../Test.Json','r') as Test_data:
            data = json.load(Test_data)
    data = strip_json_keys(data)
    for book in data['message']:
        book = Books(**book)
        book.SysId = str(uuid.uuid4())
        books.append(book)
    return books
#test_books = RunTestClass()

