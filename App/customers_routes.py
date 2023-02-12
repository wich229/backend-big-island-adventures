from app import db
from app.models.tour import Tour
from app.models.booking import Booking
from app.models.customer import Customer
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")
from .main_routes import main_bp
@customers_bp.route('/login')
def login():
	return render_template('login.html')

@customers_bp.route('/login', methods=['POST'])
def login_post():
	email = request.form.get('email')
	password = request.form.get('password')
	remember = True if request.form.get('remember') else False

	customer = Customer.query.filter_by(email=email).first()

	# check if the customer actually exists
	# take the customer-supplied password, hash it, and compare it to the hashed password in the database
	if not customer or not check_password_hash(customer.password, password):
		flash('Please check your login details and try again.')
		return redirect(url_for('customers_bp.login')) # if the customer doesn't exist or password is wrong, reload the page

	# if the above check passes, then we know the customer has the right credentials
	login_user(customer, remember=remember)
	return redirect(url_for('main_bp.profile'))


@customers_bp.route('/signup')
def signup():
	return render_template('signup.html')


@customers_bp.route('/signup', methods=['POST'])
def signup_post():
	email = request.form.get('email')
	name = request.form.get('name')
	phone = request.form.get('phone')
	password = request.form.get('password')

	customer = Customer.query.filter_by(email=email).first() # if this returns a customer, then the email already exists in database

	if customer: # if a customer is found, we want to redirect back to signup page so customer can try again
		flash('Email address already exists')
		return redirect(url_for('customers_bp.signup'))

	# create a new customer with the form data. Hash the password so the plaintext version isn't saved.
	new_customer = Customer(email=email, name=name,phone=phone, password=generate_password_hash(password, method='sha256'))

	# add the new customer to the database
	db.session.add(new_customer)
	db.session.commit()

	return redirect(url_for('customers_bp.login'))


@customers_bp.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main_bp.index'))