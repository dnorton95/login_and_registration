from flask_app import app
from flask import redirect, render_template, request, session
from flask_app.models.registration import registration_class
from flask_app.controllers import logout
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import bcrypt

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Establish a database connection
    db = connectToMySQL("user_schema")

    # Query the database to find the user
    query = "SELECT * FROM users WHERE email=%(email)s"
    data = {
        'email': email,
    }
    users = db.query_db(query, data)

    if users:  # Check if any users are found
        user = users[0]  # Retrieve the first user
        # Verify the hashed password
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['email'] = email
            session['first_name'] = user['first_name']
            session['last_name'] = user['last_name']
            session['email'] = user['email']
            session['gender'] = user['gender']
            session['birthday'] = user['birthday']
            session['race'] = user['race']
            session['usa'] = user['usa']
            return redirect('/log_out')
        else:
            flash("Login failed. Please check your email and password.")
            return redirect('/')  # Redirect to login page upon failed login