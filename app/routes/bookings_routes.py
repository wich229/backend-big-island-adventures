from app import db
from app.models.tour import Tour
from app.models.booking import Booking
from app.models.customer import Customer
from datetime import date
from sqlalchemy.sql import functions
from flask import Blueprint, jsonify, make_response, request, abort
from app.routes.helpers import validate_model

bookings_bp = Blueprint("bookings_bp", __name__, url_prefix="/bookings")

#-------------------------------------------------------------------------------
#---------------------------- Helper Functions ---------------------------------
#-------------------------------------------------------------------------------

def sort_attribute_helper(cls, query, attr=None, sort_method="asc"):
    if attr:
        # if attr == "name":
        #     if sort_method == "desc":
        #         query = query.order_by(cls.name.desc())
        #     else:
        #         query = query.order_by(cls.name.asc())
        if attr == "booking_date":
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
#------------------------------- Routes ----------------------------------------
#-------------------------------------------------------------------------------
# POST /bookings/booking_detail/<tour_id>
@bookings_bp.route("/<customer_id>/booking_detail/<tour_id>", methods=["POST"])
def booking_one_event(customer_id, tour_id):
    booking_data = request.get_json()
    print(booking_data)
    
    customer = validate_model(Customer,customer_id)
    tour = validate_model(Tour, tour_id)

    #----------------------------------------------------------------------
    # old version ---------------------------------------------------------
    #----------------------------------------------------------------------
    # invoke Tour.available_capacity(tour.id, saled_tickets_total) to get available_capacity
    # saled_tickets_total: sql => SELECT tour_id, SUM(tickets)FROM booking WHERE tour_id=1 GROUP BY tour_id;
    # if booking tickets greater than calcuated available_capacity reasie error
    #----------------------------------------------------------------------
    # saled_tickets_total_query = Booking.query.filter_by(tour_id=tour.id, status="confirmed")
    # total_saled = sum([ each_sale.tickets for each_sale in saled_tickets_total_query])
    # print(total_saled)
    #available_tickets = tour.available_capacity(total_saled)
    
    #----------------------------------------------------------------------
    #new version ----------------------------------------------------------
    #----------------------------------------------------------------------
    available_tickets = tour.available_capacity()
    
    print(available_tickets)
    
    try:
        if(booking_data["tickets"] > available_tickets):
            abort(make_response({"message": f"No available_tickets for customer {customer.id} and tour {tour.id}"}, 400))    
        
        new_booking = Booking(
                customer_id = customer.id,
                tour_id = tour.id,
                tickets = booking_data["tickets"]
            )
        db.session.add(new_booking)
        db.session.commit() 
    
    except KeyError as keyerror:
        abort(make_response(
            {"details": f"Request body must include {keyerror.args[0]}."}, 400))
    
    return make_response(new_booking.to_dict(),201)
    
# GET /booking/<customer_id>/transctions
@bookings_bp.route("/<customer_id>/transctions", methods=["GET"])
def get_transctions_by_customer_id(customer_id):
    validate_model(Customer, customer_id)

    # test 1
    transctions_query = db.session.query(Booking).filter_by(customer_id = customer_id)
    
    # test 2
    # transctions_query = db.session.query(Customer).join(Booking).filter_by(customer_id = customer_id)
    
    # sort by Tour date
    is_sort = request.args.get("sort")

    if is_sort:
        transctions_query = sort_attribute_helper(Booking, transctions_query, is_sort)
    else:
        # sort by id in asc default
        transctions_query = transctions_query.order_by(Booking.id.asc())
    
    
    transctions_response = []
    for transction in transctions_query:
        transctions_response.append(transction.to_dict())
    return make_response(jsonify(transctions_response), 200)


# PUT /booking/<customer_id>/transctions/<booking_id> 
# change the status from confirmed to the canceled 
@bookings_bp.route("/<customer_id>/transctions/<booking_id>", methods=["PUT"])
def change_transctions_by_customer_id_and_booking_id(customer_id, booking_id):
    validate_model(Customer, customer_id)
    booking = validate_model(Booking, booking_id)
    
    # booking_status : canceled 
    booking_status = request.args.get("status")
    
    # add the tickets back to the capacity???
    
    if booking_status:
        if booking_status == "canceled":
            booking.status = "canceled"
            db.session.add(booking)
            db.session.commit()
        
    
    return make_response(jsonify(booking.to_dict()), 200)
            
            


# for handling the expire date stituation
# https://stackoverflow.com/questions/57292684/flask-sqlalchemy-update-record-automatically-after-specific-time

