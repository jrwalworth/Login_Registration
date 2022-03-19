from app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db='user_login_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.dob = data['dob']
        self.pc_or_mac = data['pc_or_mac']
        self.fav_animal = data['fav_animal']
        self.created_at = data['created_at']
        self.updated_at = data['iupdated_at']
        
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
    def insert(cls, data):
        query = "INSERT INTO user ( first_name, last_name, email, password, \
            dob, pc_or_mac, fav_animal, created_at, updated_at) VALUES \
            (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(dob)s,\
            %(pc_or_mac)s, %(fav_animal)s,NOW(), NOW() );"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE user SET first_name=%(first_name)s, last_name=%(last_name)s,\
            email=%(email)s, password=%(password)s, dob=%(dob)s, pc_or_mac=%(pc_or_mac)s,\
            fav_animale=%(fav_animal)s, updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM user WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    #Validations
    @staticmethod
    def validation(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash('First name must be at least two characters.')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('last name must be at least two characters.')
            is_valid = False
        #Add additional validation conditions for remaining fields
        return is_valid
        