from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Employee, User, Account, Menu
from sqlalchemy import func

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/', methods=['POST','PUT'])
@login_required
def purchase():
    hamburger = request.form.get('hamburger')
    crispy = request.form.get('crisp chicken sandwich')
    fish = request.form.get('fish burger')
    pizza = request.form.get('pizza')
    mac = request.form.get('buffalo wings')
    wings = request.form.get('Mac n Cheese')
    print(hamburger)
    # fries = request.form.get('Hamburger')
    # cheesefries = request.form.get('Hamburger')
    # coleslaw = request.form.get('Hamburger')
    # garlic_bread = request.form.get('Hamburger')
    # biscuits = request.form.get('Hamburger')
    # veggies = request.form.get('Hamburger')
    # mozzarella = request.form.get('Hamburger')
    # caesar = request.form.get('Hamburger')
    if int(hamburger) > 0:
        menu_item = db.session.query(Menu).filter_by(item='Hamburger').first()
        menu_item.times_ordered = menu_item.times_ordered + 1
        db.session.commit()
            

    return redirect(url_for('main.profile'))



@main.route('/profile')
@login_required
def profile():
    user = Account.query.filter_by(user_email=current_user.email).first()
    #logic to return 3 most ordered dishes
    res = Menu.query.order_by(Menu.times_ordered.desc()).limit(3).all()
    item1 = res[0]
    item2 = res[1]
    item3 = res[2]
    return render_template('profile.html', balance=user.balance, item1=item1.item, item2=item2.item, item3=item3.item)

@main.route('/cart')
@login_required
def cart():
    return render_template('cart.html')


@main.route('/claim')
@login_required
def claim():
    return render_template('claim.html')


@main.route('/update')
@login_required
def update():
    return render_template('update.html')


@main.route('/employee_profile')
@login_required
def employee_profile():
    return render_template('employee_profile.html')


