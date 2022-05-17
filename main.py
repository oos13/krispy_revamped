
from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from flask_login import login_required, current_user, logout_user
from . import db
from .models import Employee, User, Account, Menu, Order, Claim
from sqlalchemy import func
from datetime import datetime, date




main = Blueprint('main', __name__)

@main.route('/')
def index():
    items = Menu.query.filter(Menu.special_item == False)
    
    return render_template('index.html', items=items)

@main.route('/', methods=['POST','GET'])
@login_required
def purchase():
    #find account of current user
    user_account = db.session.query(Account).filter_by(user_email=current_user.email).first()
    items = Menu.query.filter(Menu.special_item == False)
    if user_account.vip_status == True:
        items = Menu.query.filter()
    
    #create an order to be entered into the order table
    order_items = ""
    price = 0
    order_date = datetime.now()
    
    for things in items:
        current_app.logger.info(things.item)

        quantity = request.form.get(things.item)
        current_app.logger.info(quantity)
        for i in range(int(quantity)):
            order_items = order_items + things.item + ","
            price = price + things.price
    

    #apply discount if VIP
    if user_account.vip_status is True:
        price = price*0.95
    #this order will be submitted to the db after validation
    new_order = Order(item=order_items, price=price, customer_id=current_user.id, date=order_date, delivery=True)
    
    #update account accordingly
    #check if there is enoguh money in account
    if user_account.balance < price:
        user_account.warnings = user_account.warnings + 1
        db.session.commit()
        #user played himself, now they are blacklisted
        if user_account.warnings == 3:
            current_user.blacklisted = True
            db.session.commit()
            logout_user()
        return redirect(url_for('.index'))  
    #user has enough money, update their account   
    else:
        user_account.balance = user_account.balance - price
        user_account.num_orders = user_account.num_orders + 1
        user_account.money_spent = user_account.money_spent + price
        db.session.commit()
        #check if user should retain vip status
        if user_account.vip_status is True and user_account.warnings == 2:
            flash("vip status lost")
            user_account.vip_status = False
            user_account.warnings = 0
            db.session.commit()

    #update the menu table to reflect the number of times an item has been ordered
    
    for things in items:        
        quantity = request.form.get(things.item)
        current_app.logger.info(quantity)
        menu_item = db.session.query(Menu).filter_by(item=things.item).first()
        menu_item.times_ordered = menu_item.times_ordered + int(quantity)
        db.session.commit()  

    db.session.add(new_order)
    db.session.commit() 

    flash('Thanks you! Your order has been submitted')       

    return redirect(url_for('.index'))



@main.route('/profile')
@login_required
def profile():
    user = Account.query.filter_by(user_email=current_user.email).first()
    #logic to return 3 most ordered dishes
    res = Menu.query.order_by(Menu.times_ordered.desc()).limit(3).all()
    item1 = res[0]
    item2 = res[1]
    item3 = res[2]

    return render_template('profile.html', balance=user.balance, item1=item1.item, item2=item2.item, item3=item3.item, vip=user.vip_status, warnings=user.warnings)

@main.route('/cart')
@login_required
def cart():
    return render_template('cart.html')


@main.route('/claim')
@login_required
def claim():
    claim_date = date.today()
    return render_template('claim.html', claim_date=claim_date)

@main.route('/claim', methods=['POST'])
def submit_claim():
    name = current_user.name
    email = current_user.email
    issue = "Complaint"
    subject = request.form.get('subject')

    new_claim = Claim(name=name, email=email, category=issue, comment=subject)
    db.session.add(new_claim)
    db.session.commit()
    return redirect(url_for('main.profile'))


@main.route('/compliment')
@login_required
def compliment():
    claim_date = date.today()
    return render_template('compliment.html', claim_date=claim_date)

@main.route('/compliment', methods=['POST'])
def submit_compliment():
    name = current_user.name
    email = current_user.email
    issue = "Compliment"
    subject = request.form.get('subject')

    new_claim = Claim(name=name, email=email, category=issue, comment=subject)
    db.session.add(new_claim)
    db.session.commit()
    return redirect(url_for('main.profile'))




@main.route('/update')
@login_required
def update():
    return render_template('update.html')


@main.route('/employee_profile')
@login_required
def employee_profile():
    return render_template('employee_profile.html')

@main.route('/manager_profile')
@login_required
def manager_profile():
    employees = Employee.query.filter().all()
    menu_items = Menu.query.filter().all()
    claims = Claim.query.filter().all()
    return render_template('manager_profile.html', employees=employees, menu_items=menu_items, claims=claims)

@main.route('/pickup')
@login_required
def pickup():
    return render_template('pickup.html')

@main.route('/delivery')
@login_required
def delivery():
    return render_template('delivery.html')

@main.route('/menu')
def menu():
    items = Menu.query.filter(Menu.special_item == False)

    return render_template('menu.html', items=items)


@main.route('/edit_menu')
def edit_menu():
    return render_template('edit_menu.html')

@main.route('/edit_menu', methods=['POST'])
def change_menu():
    item = request.form.get('dish')
    Menu.query.filter_by(Menu.item == item).delete()
    db.session.commit()

@main.route('/add_menu')
def add_menu():
    return render_template('add_menu.html')

@main.route('/add_menu', methods=['POST'])
@login_required
def add_to_menu():
    name = request.form.get('item')
    type = request.form.get('item_type')
    price = request.form.get('price')
    price = float(price)
    chef = request.form.get('chef')
    is_special = request.form.get('special')
    if is_special == "True":
        is_special = True
    else:
        is_special = False
    

    new_item = Menu(item=name, item_type=type, price=price, special=is_special, chef_made=chef)
    db.session.add(new_item)
    db.session.commit()

    return redirect(url_for('main.employee_profile'))
