from sqlalchemy import Column,String,Float,Boolean, Date, ForeignKey
from DataModel.BaseDM import BaseDM
from DataModel.Books import Books
from DataModel.Members import Members
from sqlalchemy.orm import relationship , backref
class Transactions(BaseDM):
    __tablename__ = 'Transactions'
    Member_id = Column(String(36),ForeignKey(Members.SysId),nullable=False)
    Book_id  = Column(String(36),ForeignKey(Books.SysId),nullable=False)
    created_date = Column(Date,nullable=False)
    issue_date = Column(Date)
    return_date = Column(Date)
    is_returned = Column(Boolean, default=False)
    charges = Column(Float)
    Member = relationship(Members, backref=backref("Transactions"))
    Book = relationship(Books,backref=backref("Transactions"))