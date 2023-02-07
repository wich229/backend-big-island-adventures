from app import db
from app.models.tour import Tour
from app.models.booking import Booking
from app.models.customer import Customer
from flask import Blueprint, jsonify, abort, make_response, request

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")



# POST /add customer
# @customers_bp.route("/register", methods=["POST"])



# POST /get customer or # GET customers/<customer_id>
# @customers_bp.route("/login", methods=["POST"])



# POST /logout
# @app.route("/logout", methods=["POST"])