import uuid

import requests
from flask import Flask, jsonify, render_template, request
from BusinessLogic.BookBC import BookBC
from BusinessLogic.MemberBC import MemberBC
from BusinessLogic.TransactionBC import TransactionBC
from BusinessLogic.AppHelper import strip_json_keys
import pandas as pd
from DataModel.Books import Books

import os
app = Flask(__name__, template_folder='Views', static_url_path='/static/')

# region Index
@app.route("/")
def home():
    #print("Current Working Directory:", os.getcwd())
    return render_template('Forms/index.html')
# endregion

# region Book CRUD
@app.route("/Book")
def BookLising():
    #print(BookBC.get_books(self=None))
    print(BookBC(None).get_books())
    return render_template('Listings/Book.html', books = BookBC(SysId=None).get_books())
@app.route('/Book/Create')
def CreateBook():
    # Add your logic for creating a book here
    return render_template('Forms/Book.html', book = BookBC(None) , status = 'Create')
@app.route('/Book/Edit')
def EditBook():
    SysId = request.args.get('SysId')
    book = BookBC(SysId=SysId)

    return render_template('Forms/Book.html', book = book.get_books() , status = 'Edit')

@app.route('/SubmitBook', methods=['POST'])
def SubmitBook():
    if request.method == 'POST':
        if request.form.get('SysId') == 'None':
            book_bc = BookBC()
            return jsonify(book_bc.create_book(new_book=dict(request.form)))
        else:
            #print('Updating Valuesss',request.form.get('SysId'))
            book_bc = BookBC(SysId=request.form.get('SysId'))
            return jsonify(book_bc.update_book(new_data=dict(request.form)))

@app.route('/Book/Delete')
def DeleteBook():
    SysId = request.args.get('SysId')
    book = BookBC(SysId=SysId)
    return render_template('Forms/Book.html', book=book.get_books() , status = 'Delete')

@app.route('/Delete', methods=['POST'])
def Delete():
    if request.method == 'POST':
        if request.form.get('SysId') == 'None':
            return jsonify({"error":"No Book To Deelte"},500)
        else:
            book_bc = BookBC(SysId=request.form.get('SysId'))
            return jsonify(book_bc.delete_book())
# endregion

# region Book API
@app.route('/Book/Api')
def ApiBook():
    return render_template('Forms/BookAPI.html')


@app.route('/ApiCall', methods=['POST'])
def FecthApiData():
    api_url = request.form.get('ApiLink')
    try:
        response = requests.get(api_url)
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/SaveApi', methods=['POST'])
def SaveApi():
    try:
        data = request.get_json()
        print(data)
        # Extract the 'Table' and 'data' fields
        # table_name = data.get('Table')
        selected_data = data.get('data')
        final_data = []
        book_bc = BookBC()
        for d in selected_data:
            clean_data = strip_json_keys(d)
            final_data.append(book_bc.create_book(new_book=clean_data))
        for final in final_data:
            print(final['message'])
        return jsonify(final_data)
    except:
        return 'Api error'


# endregion

# region Member CRUD
@app.route('/Member')
def MemberLisitng():
    m = MemberBC(SysId=None).get_members()
    print(m)
    return render_template('Listings/Member.html',members = m)

@app.route('/Member/Create')
def CreateMember():
    # Add your logic for creating a book here
    return render_template('Forms/Member.html', member = MemberBC(None),status = 'Create')

@app.route('/Member/Edit')
def EditMember():
    SysId = request.args.get('SysId')
    member = MemberBC(SysId=SysId)
    return render_template('Forms/Member.html', member = member.get_members() , status = 'Edit')


@app.route('/SubmitMember', methods=['POST'])
def SubmitMember():
    if request.method == 'POST':
        if request.form.get('SysId') == 'None':
            member_bc = MemberBC()
            return jsonify(member_bc.create_member(new_data=dict(request.form)))
        else:
            #print('Updating Valuesss',request.form.get('SysId'))
            member_bc = MemberBC(SysId=request.form.get('SysId'))
            return jsonify(member_bc.update_member(new_data=dict(request.form)))

@app.route('/Member/Delete')
def DeleteMember():
    SysId = request.args.get('SysId')
    member = MemberBC(SysId=SysId)
    return render_template('Forms/Member.html', member=member.get_members() , status = 'Delete')

@app.route('/DeleteM', methods=['POST'])
def DeleteM():
    if request.method == 'POST':
        if request.form.get('SysId') == 'None':
            return jsonify({"error":"No Book To Delte"},500)
        else:
            member_bc = MemberBC(SysId=request.form.get('SysId'))
            return jsonify(member_bc.delete_member())
# endregion

# region Transaction CRUD
@app.route("/Transactions")
def TransactionLising():
    # print(BookBC.get_books(self=None))
    # print(TransactionBC(SysId=None).get_transactions())
    return render_template('Listings/Transaction.html', transactions = TransactionBC(SysId=None).get_transactions())
@app.route('/Transaction/Create')
def CreateTransaction():
    # Add your logic for creating a transaction here
    return render_template('Forms/Transaction.html', transaction = TransactionBC(None),books=BookBC(None).get_books(),members=MemberBC(None).get_members(),status = 'Create')
@app.route('/Transaction/Edit')
def EditTransaction():
    SysId = request.args.get('SysId')
    Transaction = TransactionBC(SysId=SysId)
    return render_template('Forms/Transaction.html', transaction = Transaction.get_transactions(),book=BookBC.get_books(None),member=MemberBC.get_members(None), status = 'Edit')

@app.route('/SubmitTransaction', methods=['POST'])
def SubmitTransaction():
    if request.method == 'POST':
        if request.form.get('SysId') == 'None':
            Transaction_bc = TransactionBC()
            return jsonify(Transaction_bc.create_transaction(new_transaction=dict(request.form)))
        else:
            #print('Updating Valuesss',request.form.get('SysId'))
            Transaction_bc = TransactionBC(SysId=request.form.get('SysId'))
            return jsonify(Transaction_bc.update_transaction(new_data=dict(request.form)))

@app.route('/Transaction/Delete')
def DeleteTransaction():
    SysId = request.args.get('SysId')
    Transaction = TransactionBC(SysId=SysId)
    return render_template('Forms/Transaction.html', transaction=Transaction.get_transactions() , status = 'Delete')

@app.route('/Delete', methods=['POST'])
def DeleteT():
    if request.method == 'POST':
        if request.form.get('SysId') == 'None':
            return jsonify({"error":"No Book To Deelte"},500)
        else:
            Transaction_bc = TransactionBC(SysId=request.form.get('SysId'))
            return jsonify(Transaction_bc.delete_transaction())
# endregion

if __name__ == "__main__":
    app.run(debug=True)