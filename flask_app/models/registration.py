from flask_app.config.mysqlconnection import connectToMySQL
from pprint import pprint
from flask import flash, session
import re

class registration_class:
    DB = "user_schema"

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.birthday = data['birthday']
        self.gender = data['gender']
        self.race = data['race']
        self.usa = data['usa']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def register(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, password, birthday, gender, race, usa)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(birthday)s, %(gender)s, %(race)s, %(usa)s)
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result  # Return the result of the query execution

    @classmethod
    def get_user_by_id(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(id)s"
        data = {'id': user_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            return cls(result[0])  # Return the first book found
        else:
            return None

    @staticmethod
    def validate_registration(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash('First name must be at least 2 characters')
            is_valid = False

        if len(data['last_name']) < 2:
            flash('Last name must be at least 2 characters')
            is_valid = False

        if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
            flash('Invalid email format.')
            is_valid = False
        else:
            db = connectToMySQL("user_schema")
            query = "SELECT * FROM users WHERE email = %(email)s"
            result = db.query_db(query, {'email': data['email']})
            if result:
                flash('Email already exists.')
                is_valid = False

        if len(data['password']) < 8:
            flash('Password must be at least 8 character')
            is_valid = False
        if not re.search(r"\d", data['password']):
            flash('Password must contain at least one number.')
            is_valid = False
        if not re.search(r"[A-Z]", data['password']):
            flash('Password must contain at least one uppercase letter.')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Password and password confirmation must match.')
            is_valid = False
            
        return is_valid
