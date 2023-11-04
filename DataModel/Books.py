from sqlalchemy import Column, Integer, String, Float, Date
from DataModel.BaseDM import BaseDM
class Books(BaseDM):
    __tablename__ = "Books"
    bookID = Column(Integer,unique=True)
    title = Column(String)
    authors = Column(String)
    average_rating = Column(Float)
    isbn = Column(String)
    isbn13 = Column(String)
    language_code = Column(String)
    num_pages = Column(Integer)
    ratings_count = Column(Integer)
    text_reviews_count = Column(Integer)
    publication_date = Column(Date)
    publisher = Column(String)
