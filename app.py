from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import json
import jwt
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

@app.route('/')
def Home():
    return redirect(url_for('LoginPage'))

@app.route('/login')
def LoginPage():
    if CheckLogin():
        return redirect(url_for('DashboardPage'))
    return render_template('login.html')

@app.route('/dashboard')
def DashboardPage():
    if not CheckLogin():
        return redirect(url_for('LoginPage'))
    return render_template('dashboard.html')


@app.route('/register')
def RegisterPage():
    if CheckLogin():
        return redirect(url_for('DashboardPage'))
    return render_template('register.html')


@app.route('/api/auth/register', methods=['POST'])
def ApiRegister():
    data = request.get_json()
    
    ExistingUser = UsersCollection.find_one({'email': data['email']})
    if ExistingUser:
        return jsonify({'success': False, 'detail': 'Username already exists'})
    
    NewUser = {
        'password': data['password'],
        'name': data['fullname'],
        'email': data['email'],
        'role': data['role'],
        'created_at': datetime.now()
    }
    
    UsersCollection.insert_one(NewUser)
    return jsonify({'success': True, 'message': 'User created successfully'})


@app.route('/api/auth/login', methods=['POST'])
def ApiLogin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = UsersCollection.find_one({'email': email, 'password': password})
    
    print(user,email)
    if user:
        session['user'] = {
            'role': user['role'],
            'name': user['name']
        }
        
        payload = {"email": email}
        return jsonify({
            'success': True,
            'user': {
                'token':jwt.encode(payload,"123456"),
                'role': user['role'],
                'name': user['name']
            }
        })
    
    return jsonify({'success': False, 'detail': 'Invalid username or password'})



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)