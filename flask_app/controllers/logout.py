from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template, redirect, request, session, flash

@app.route("/log_out")
def logout():
    # Retrieve the first name from the session
    first_name = session.get('first_name')
    last_name = session.get('last_name')
    email = session.get('email')
    gender = session.get('gender')
    birthday = session.get('birthday')
    race = session.get('race')
    usa = session.get('usa')

    if first_name and last_name and email and gender and birthday and race and usa:
        return render_template("logout.html", first_name=first_name, last_name=last_name, email=email, gender=gender, birthday=birthday, race=race, usa=usa)
    else:
        flash("First name not found in session.")
        return redirect('/')  # Redirect to login page upon failure

@app.route("/clear_session")
def clear_session():
    # Clear the session
    session.clear()
    flash("You have been successfully logged out.")
    return redirect('/')  # Redirect to the index route
