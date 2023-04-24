from flask import Blueprint,render_template,redirect, url_for,flash, request
from werkzeug.security import generate_password_hash
from project.models import User
from project import db
from flask_login import login_user, login_required, logout_user
from threading import Thread


routes = Blueprint('routes', __name__)


@routes.route('/login')
def login():
    return render_template('login.html')

@routes.route('/signup')
def signup():
    return render_template('signup.html')

@routes.route('/signup', methods=['GET','POST'])
def signup_post():
    if "post":
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        confirm_password = request.form.get('password')
        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        if password!=confirm_password:
            flash('Password does not match')
            return redirect(url_for('routes.signup'))
        
        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('routes.signup'))
 
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, first_name=firstname,last_name=lastname, password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('routes.login'))
    else:
        return render_template('signup.html')

 
@routes.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    print('SE project')
    user = User.query.filter_by(email=email).first()
    login_user(user, remember=remember)
    return redirect(url_for('netflixUtility.viewNetflix'))   

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))