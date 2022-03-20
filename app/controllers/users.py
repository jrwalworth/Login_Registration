from flask import render_template, redirect, request, session, flash
from app.models.user import User
from app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

#index
@app.route('/')
def index():
    return render_template('index.html')

#index
@app.route('/register', methods=['POST'])
def register():
    isValid = User.validate_registration(request.form)
    if not isValid:
        return redirect('/')
    newUser = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        #hash password
        'password' : bcrypt.generate_password_hash(request.form['password']),
        'dob' : request.form['dob'],
        'fav_animal' : request.form['fav_animal'],
        'subscribe' : request.form['subscribe'],
    
    }
    id = User.insert(newUser)
    if not id:
        flash('Something went wrong.')
        return redirect('/')
    session['user_id'] = id
    return redirect('/welcome/')


#
@app.route('/login', methods=['POST'])
def login():
    data = {
        'email' : request.form['email']
    }
    user = User.getEmail(data)
    if not user:
        flash('That email is not in our database. Please register.')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Wrong password.')
    session['user_id'] = user.id
    return redirect('/welcome/')

#
@app.route('/logout')
def logout():
    pass

#
@app.route('/welcome/')
def welcome_page():
    return render_template('welcome.html')