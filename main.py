from flask import Blueprint, render_template
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    return render_template('profile.html')

@main.route('/cart')
def cart():
    return render_template('cart.html')


@main.route('/claim')
def claim():
    return render_template('claim.html')


@main.route('/update')
def update():
    return render_template('update.html')


@main.route('/employee_profile')
def employee_profile():
    return render_template('employee_profile.html')

