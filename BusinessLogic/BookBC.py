import uuid
from DataModel.Books import Books
from BusinessLogic.AppHelper import ActiveSession
class BookBC:
    def __init__(self, SysId=None):
        self.SysId = SysId
        self.load_book_data()

    def load_book_data(self):
        try:
            if self.SysId is not None:
                self.book = ActiveSession.Session.query(Books).filter_by(SysId=self.SysId).first()
            else:
                print('SysId not provided, initialized empty book')
                self.book = Books()
        except Exception as e:
            print(f"Error loading book data: {str(e)}")
            self.book = None

    def create_book(self,new_book):
        try:
            self.book = Books(**new_book)
            self.book.SysId = str(uuid.uuid4())
            book_exists = ActiveSession.Session.query(Books).filter_by(bookID=self.book.bookID).first()
            if book_exists:
                raise ValueError('Book Already Exists!!')
            else:
                ActiveSession.Session.add(self.book)
                ActiveSession.Session.commit()
                new_book['message'] = 'Book created successfully ' + str(self.book.bookID)
                new_book['Code'] = 201
                return new_book
        except ValueError as ve:
            ActiveSession.Session.rollback()
            new_book['message'] = str(ve)
            new_book['Code'] = 500
            return new_book
        except Exception as e:
            ActiveSession.Session.rollback()
            new_book['message'] = str(e)
            new_book['Code'] = 500
            return new_book

    def get_books(self):
        try:
            print('called here')
            if self.SysId is None:
                return ActiveSession.Session.query(Books).all()
            else:
                if self.book:
                    return self.book
                else:
                    return {"error": "Book not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    def update_book(self, new_data):
        try:
           if self.book is not None:
                for key, value in new_data.items():
                    setattr(self.book, key, value)
                ActiveSession.Session.commit()
                return {"message": "Book updated successfully ","Code":201}
           else:
               return {"message": "Book not found",'Code':404}
        except Exception as e:
            ActiveSession.Session.rollback()
            return {"message": str(e),'Code':500}

    def delete_book(self):
        try:
            ActiveSession.Session.delete(self.book)
            ActiveSession.Session.commit()
            return {"message": "Book deleted successfully",'Code':201 }
        except Exception as e:
            ActiveSession.Session.rollback()
            return {"message": str(e),'Code':500}

