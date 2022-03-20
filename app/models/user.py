from app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

#min 8 characters, at least one letter and one number.
PW_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')

class User:
    db='user_login_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.dob = data['dob']
        # self.pc_or_mac = data['pc_or_mac']
        self.fav_animal = data['fav_animal']
        self.agree = data['agree']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM user;"
        results = connectToMySQL(cls.db).query_db(query)
        users=[]
        for u in results:
            users.append( cls(u) )
        return users
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM user WHERE id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM user WHERE email=%(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def insert(cls, data):
        query = "INSERT INTO user ( first_name, last_name, email, password, \
            dob,  fav_animal, agree, created_at, updated_at) VALUES \
            (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(dob)s,\
            %(fav_animal)s, %(agree)s,NOW(), NOW() );"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE user SET first_name=%(first_name)s, last_name=%(last_name)s,\
            email=%(email)s, password=%(password)s, dob=%(dob)s, fav_animal=%(fav_animal)s, \
            agree=%(agree)s,updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM user WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    #Validations
    @staticmethod
    def validate_registration(user):
        is_valid = True
        query = 'SELECT * FROM user WHERE email=%(email)s;'
        results = connectToMySQL(User.db).query_db(query, user)
        #validate email
        if len(user['email']) < 1:
            is_valid = False
            flash('You must add an email address.')
        elif not EMAIL_REGEX.match(user['email']):
            is_valid = False
            flash('Invalid email format.')
        if len(results) >= 1:
            is_valid = False
            flash('This email is already being used.')
        #validate names
        if len(user['first_name']) < 2:
            flash('First name must be at least two characters.')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last name must be at least two characters.')
            is_valid = False
        #validate password
        if not PW_REGEX.match(user['password']):
            is_valid = False
            flash("Password must be at least 8 characters and contain at least one letter and one number.")
        #confirm password
        if user['password'] != user['confirm']:
            is_valid = False
            flash('Passwords must match.')
        #validate dob
        if user['dob'] == '':
            is_valid = False
            flash('Date of birth is required.')
        if (user['dob']) == None:
            is_valid = False
            flash("You haven't been born yet. Please check your date of birth.")
        #validation pc_or_mac - must select one
        # if user['pc_or_mac'].checked:
        #     is_valid = False
        #     flash('You must select pc or mac.')
        #fav_animal
        if len(user['fav_animal']) < 1 or user['fav_animal'] == 'Choose an animal':
            is_valid = False
            flash('You must select an animal.')
        print(user['agree'])
        if user['agree'] != "1":
            is_valid = False
            flash('You must agree to the Privacy Policy.')
        return is_valid
        
    def fullName(self):
        return f'{self.first_name} {self.last_name}'