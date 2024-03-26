from flask_app import app
from flask import redirect, render_template, request
from flask_app.models.registration import registration_class
from flask import flash
from datetime import datetime
import bcrypt

@app.route("/register", methods=["POST"])
def register():
    form_data = request.form.to_dict()
    birthday = datetime.strptime(form_data['birthday'], '%Y-%m-%d')
    formatted_birthday = birthday.strftime('%m-%d-%Y')
    # Capitalize first name and last name
    form_data['first_name'] = form_data['first_name'].capitalize()
    form_data['last_name'] = form_data['last_name'].capitalize()

   
    # Compare passwords before hashing
    if form_data['password'] != form_data['confirm_password']:
        flash("Passwords do not match.")
        return redirect('/')  # Redirect to the correct route
        
    if not registration_class.validate_registration(form_data):
        return redirect('/')  # Redirect to the correct route
    
    # Hash the password
    hashed_password = bcrypt.hashpw(form_data['password'].encode(), bcrypt.gensalt())
    form_data['password'] = hashed_password.decode('utf-8')
    
    registration_class.register(form_data)
    return redirect("/success")  # Redirect to the correct route


@app.route("/success", methods=["GET", "POST"])
def success():
    return render_template("success.html")

