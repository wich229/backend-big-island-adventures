from app import db
from app.models.tour import Tour
from app.models.booking import Booking
from app.models.customer import Customer
from flask import Blueprint, jsonify, abort, make_response, request

bookings_bp = Blueprint("bookings_bp", __name__, url_prefix="/bookings")