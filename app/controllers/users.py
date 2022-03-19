from flask import render_template, redirect, request, session
from app.models.user import User
from app import app

#index
@app.route('/')
def index():
    return render_template('index.html')