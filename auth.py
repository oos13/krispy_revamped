from tabnanny import check
from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Employee, User, Account
from flask_login import login_required, login_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    #login code
    #pull info from form
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    #query database, find user by email if exists save to variable 'user'
    user = User.query.filter_by(email=email).first()
    # employee = Employee.query.filter_by(email=email).first()
    #check if user exists, if not print login error message and redirect to login
    if not user or not check_password_hash(user.password, password) : 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    #if we get here we know user entered correct credentials

    login_user(user, remember=remember)
    
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    address = request.form.get('address')
    cc_info = request.form.get('cc_info')#this will go into new_account = Account(...)
    deposit = request.form.get('deposit')


    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('email adress already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, address=address, password=generate_password_hash(password, method='sha256'))
    new_account = Account(balance=deposit, cc_info=cc_info, user_email=email)

    # add the new user to the database
    db.session.add(new_user)
    db.session.add(new_account)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/employee')
def employee():
    return render_template('employee.html')


@auth.route('/employee', methods=['POST'])
def employee_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    position = request.form.get('position')
   

    employee = Employee.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if employee: # if a user is found, we want to redirect back to signup page so user can try again
        flash('email adress already exists')
        return redirect(url_for('auth.employee'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_employee = Employee(email=email, name=name, position=position, password=generate_password_hash(password, method='sha256'))
    ###new_account = Account(...)

    # add the new user to the database
    db.session.add(new_employee)
    ###db.session.add(new_account)
    db.session.commit()

    return redirect(url_for('auth.employee_login'))


@auth.route('/employee_login')
def employee_login():
    return render_template('employee_login.html')

@auth.route('/employee_login', methods=['POST'])
def employee_login_post():
    #login code
    #pull info from form
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    #query database, find user by email if exists save to variable 'user'
    employee = Employee.query.filter_by(email=email).first()
    # employee = Employee.query.filter_by(email=email).first()
    #check if user exists, if not print login error message and redirect to login
    if not employee or not check_password_hash(employee.password, password) : 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.employee_login'))
    #if we get here we know user entered correct credentials

    login_user(employee, remember=remember)
    
    return redirect(url_for('main.employee_profile'))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

