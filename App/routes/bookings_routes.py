from app import db
from app.models.tour import Tour
from app.models.booking import Booking
from app.models.customer import Customer
from datetime import date
from flask import Blueprint, jsonify, make_response, request, abort
from app.routes.helpers import validate_model,validate_request_and_create_entry

bookings_bp = Blueprint("bookings_bp", __name__, url_prefix="/bookings")

#-------------------------------------------------------------------------------
# --------------------------- Helper Functions ---------------------------------
#-------------------------------------------------------------------------------

def sort_attribute_helper(cls, query, attr=None, sort_method="asc"):
    if attr:
        if attr == "name":
            if sort_method == "desc":
                query = query.order_by(cls.name.desc())
            else:
                query = query.order_by(cls.name.asc())
        elif attr == "booking_date":
            if sort_method == "desc":
                query = query.order_by(cls.booking_date.desc())
            else:
                query = query.order_by(cls.booking_date.asc())

    elif sort_method == "desc":
        query = query.order_by(cls.id.desc())
    else:
        # sort by id default
        query = query.order_by(cls.id.asc())

    return query
#-------------------------------------------------------------------------------
# ------------------------------ Routes ----------------------------------------
#-------------------------------------------------------------------------------
# POST /booking/booking_detail/<tour_id>
@bookings_bp.route("/<customer_id>/booking_detail/<tour_id>", methods=["POST"])
def booking_one_event(customer_id, tour_id):
    booking_data = request.get_json()
    
    customer = validate_model(Customer,customer_id)
    tour = validate_model(Tour, tour_id)
    
    # new_booking = validate_request_and_create_entry(Booking, booking_data)
    # print(new_booking)
    # new_booking["tour_id"] = tour_id
    # new_booking["customer_id"] = customer_id
    
    new_booking = Booking(
            customer_id = customer.id,
            tour_id = tour.id,
            tickets = booking_data["tickets"]
        )
    
    db.session.add(new_booking)
    db.session.commit()

    return make_response(new_booking.to_dict(),201)
    
    
# GET /booking/<customer_id>/transctions
@bookings_bp.route("/<customer_id>/transctions", methods=["GET"])
def get_transctions_by_customer_id(customer_id):
    customer = validate_model(Customer, customer_id)

    # test 1
    transctions_query = db.session.query(Booking).filter_by(customer_id = customer_id)
    
    # test 2
    # transctions_query = db.session.query(Customer).join(Booking).filter_by(customer_id = customer_id)
    
    ###########################
    # sorting not working yet #
    ###########################
    # sort by Tour name, date
    is_sort = request.args.get("sort")

    if is_sort:
        transctions_query = sort_attribute_helper(Booking, transctions_query, is_sort)
    else:
        # sort by id in asc default
        transctions_query = transctions_query.order_by(Booking.id.asc())
    
    print(transctions_query)
    transctions_response = []
    for transction in transctions_query:
        transctions_response.append(transction.to_dict())
    print(transctions_response)
    return make_response(jsonify(transctions_response), 200)


# PUT /booking/<customer_id>/transctions/<booking_id> 
# change the status from confirmed to the canceled 
@bookings_bp.route("/<customer_id>/transctions/<booking_id>", methods=["PUT"])
def change_transctions_by_customer_id_and_booking_id(customer_id, booking_id):
    validate_model(Customer, customer_id)
    booking = validate_model(Booking, booking_id)
    
    # booking_status : canceled 
    booking_status = request.args.get("status")
    
    if booking_status:
        if booking_status == "canceled":
            booking.status = "canceled"
            db.session.add(booking)
            db.session.commit()
        
    
    return make_response(jsonify(booking.to_dict()), 200)
            
            




# for handling the expire date stituation
# https://stackoverflow.com/questions/57292684/flask-sqlalchemy-update-record-automatically-after-specific-time