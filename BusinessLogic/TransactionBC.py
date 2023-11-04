import uuid
from datetime import date

from DataModel.Books import Books
from DataModel.Members import Members
from DataModel.Transactions import Transactions
from DataModel.TransactionDTO import TransactionDTO
from BusinessLogic.AppHelper import ActiveSession


class TransactionBC:
    def __init__(self, SysId=None):
        self.SysId = SysId
        self.load_transaction()

    def load_transaction(self):
        try:
            if self.SysId is not None:
                self.transaction = ActiveSession.Session.query(Transactions).filter_by(SysId=self.SysId).first()
            else:
                print('SysId not provided, initialized empty transaction')
                self.transaction = Transactions()
        except Exception as e:
            print(f"Error loading transaction data: {str(e)}")
            self.transaction = None

    def create_transaction(self, new_transaction):
        try:
            self.transaction = Transactions(**new_transaction)
            traction_exists = ActiveSession.Session.query(Transactions).filter_by(Book_id=self.transaction.Book_id).first()
            if traction_exists:
                raise ValueError('book already rented Out to x!!')
            else:
                self.transaction.SysId = str(uuid.uuid4())
                self.transaction.created_date = date.today()
                ActiveSession.Session.add(self.transaction)
                ActiveSession.Session.commit()
                new_transaction['message'] = 'Transaction created successfully'
                new_transaction['Member'] = str(self.transaction.Member_id)
                new_transaction['transaction'] = str(self.transaction.SysId)
                new_transaction['Code'] = 201
                return new_transaction
        except Exception as e:
            ActiveSession.Session.rollback()
            new_transaction['message'] = str(e)
            new_transaction['Code'] = 500
            return new_transaction

    def get_transactions(self):
        try:
            print('called here')
            if self.SysId is None:
                results = ActiveSession.Session.query(Transactions).all()
                return results
            else:
                if self.transaction:
                    return self.transaction
                else:
                    return {"error": "transaction not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    def update_transaction(self, new_data):
        try:
            if self.transaction is not None:
                for key, value in new_data.items():
                    setattr(self.transaction, key, value)
                ActiveSession.Session.commit()
                return {"message": "transaction updated successfully ", "Code": 201}
            else:
                return {"message": "transaction not found", 'Code': 404}
        except Exception as e:
            ActiveSession.Session.rollback()
            return {"message": str(e), 'Code': 500}

    def delete_transaction(self):
        try:
            ActiveSession.Session.delete(self.transaction)
            ActiveSession.Session.commit()
            return {"message": "transaction deleted successfully", 'Code': 201}
        except Exception as e:
            ActiveSession.Session.rollback()
            return {"message": str(e), 'Code': 500}
