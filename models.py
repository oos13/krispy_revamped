from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey
from . import db

#customer table
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100))
    #cc_info = db.Column(db.String(100))
    account = db.relationship("Account", backref='user', lazy=True, uselist=False)#creates a 1-to-1 relationship between user and account
    blacklisted = db.Column(db.Boolean, default=False, nullable=False)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_email = db.Column(db.String(100), db.ForeignKey(User.email), nullable=False )
    dish1 = db.Column(db.String(50))
    dish2 = db.Column(db.String(50))
    dish3 = db.Column(db.String(50))
    cc_info = db.Column(db.String(100))
    vip_status = db.Column(db.Boolean, default=False, nullable=False)
    balance = db.Column(db.Float, default=0.0, nullable=False)
    money_spent = db.Column(db.Float, default=0.0, nullable=False)
    num_orders = db.Column(db.Integer, default=0, nullable=False)
    warnings = db.Column(db.Integer, default=0, nullable=False)

class Employee(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    position = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    salary = db.Column(db.Integer, default=1000)
    compliments = db.Column(db.Integer, default=0)#a negative value would represent the complaints, positive value for compliments (bc they cancel eachother out)
    avg_rating = db.Column(db.Float, default=0)
    demotion = db.Column(db.Integer, default=0)#negative

class Manager(UserMixin, db.Model):
    manager_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

class Menu(db.Model):
    item = db.Column(db.String(64), primary_key=True, nullable=False)
    item_type = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    special_item = db.Column(db.Boolean, default=False, nullable=False)
    times_ordered = db.Column(db.Integer, default = 0, nullable=False)
    chef_made = db.Column(db.String(64))

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    item = db.Column(db.String(500), nullable=False) #should this and price be foreign keys? (ie. db.ForeignKey('Menu.item'))
    price = db.Column(db.Float, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    date = db.Column(db.DateTime)
    delivery = db.Column(db.Boolean, nullable=False)
    food_rating = db.Column(db.Integer, default=3, nullable=False)


class Deliveries(db.Model):
    delivery_no = db.Column(db.Integer, primary_key=True, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(Order.order_id), unique=True)
    delivery_person = db.Column(db.Integer, db.ForeignKey(Employee.id), nullable=True )
    delivery_rating = db.Column(db.Integer, default=3)
    fee = db.Column(db.Integer)


    
    
    
