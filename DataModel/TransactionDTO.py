class TransactionDTO:
    def __init__(self, transaction, member_id, member, book_id, code, book):
        self.transaction = transaction
        self.member_id = member_id
        self.member = member
        self.book_id = book_id
        self.code = code
        self.book = book
