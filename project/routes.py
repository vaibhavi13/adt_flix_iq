from flask import Blueprint,render_template,redirect, url_for,flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from project.models import User, Role
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
        print(email)
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        confirm_password = request.form.get('password')
        role = request.form.get('roles')
        print(role)
        role = Role.query.filter_by(rolename=role).first()
        print(role.id)
        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        if password!=confirm_password:
            flash('Password does not match')
            return redirect(url_for('routes.signup'))
        
        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('routes.signup'))
 
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, first_name=firstname,last_name=lastname, password=generate_password_hash(password, method='sha256'),role_id=role.id)



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
    # role = request.form.get('roles')
    remember = True if request.form.get('remember') else False
    print('SE project')
    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    # if not user or not check_password_hash(user.password, password):
    #     flash('Please check your login details and try again.')
    #     return redirect(url_for('routes.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)

    print(user.role_id)
    role = Role.query.filter_by(id=user.role_id).first()
    if role.rolename == 'Patient':
         url = 'patientUtility.patient'
    else:
         url = 'main.profile'   
    
    print(email)

    return redirect(url_for(url))   

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))