from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = '12345'
CORS(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['book_management']
UsersCollection = db['users']
BooksCollection = db['books']

def SerializeDoc(doc):
    if doc and '_id' in doc:
        doc['_id'] = str(doc['_id'])
    return doc

def SerializeDocs(docs):
    return [SerializeDoc(doc) for doc in docs]


def CheckLogin():
    return 'user' in session

@app.route('/login')
def LoginPage():
    if CheckLogin():
        return redirect(url_for('DashboardPage'))
    return render_template('login.html')

@app.route('/register')
def RegisterPage():
    if CheckLogin():
        return redirect(url_for('DashboardPage'))
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)