from app import db
from app.models.tour import Tour
from app.models.booking import Booking
from app.models.customer import Customer
from datetime import date
from flask import Blueprint, jsonify, make_response, request, abort

bookings_bp = Blueprint("bookings_bp", __name__, url_prefix="/bookings")

#-------------------------------------------------------------------------------
# --------------------------- Helper Functions ---------------------------------
#-------------------------------------------------------------------------------
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{model_id} invalid"}, 400))
    model = cls.query.get(model_id)
    if model:
        return model

    abort(make_response(
        {"message": f"{cls.__name__} {model_id} was not found"}, 404))


def sort_attribute_helper(cls, query, attr=None, sort_method="asc"):
    if attr:
        if attr == "name":
            if sort_method == "desc":
                query_parm = query.order_by(cls.name.desc())
            else:
                query_parm = query.order_by(cls.name.asc())
        elif attr == "id":
            if sort_method == "desc":
                query_parm = query.order_by(cls.id.desc())
            else:
                query_parm = query.order_by(cls.id.asc())
        elif attr == "booking_date":
            if sort_method == "desc":
                query_parm = query.order_by(cls.booking_date.desc())
            else:
                query_parm = query.order_by(cls.booking_date.asc())

    elif sort_method == "desc":
        query_parm = query.order_by(cls.id.desc())
    else:
        # sort by id default
        query_parm = query.order_by(cls.id.asc())

    return query_parm
#-------------------------------------------------------------------------------
# ------------------------------ Routes ----------------------------------------
#-------------------------------------------------------------------------------
# POST /booking/<customer_id>/register
@bookings_bp.route("/<customer_id>/register", methods=["POST"])


# GET /booking/<customer_id>/transctions
@bookings_bp.route("/<customer_id>/transctions", methods=["GET"])
def get_transctions_by_customer_id(customer_id):
    customer = validate_model(Customer, customer_id)
    
    # sort by Tour name and date
    is_sort = request.args.get("sort")
    # for pagination
    # count_query = request.args.get("count")
    # page_num_query = request.args.get("page_num")

    transctions_query = db.session.query(Booking, Tour.name).filter(Booking.customer_id == customer.id, Booking.tour_id == Tour.id)

    if is_sort:
        transctions_query = sort_attribute_helper(Tour, transctions_query, is_sort)
    else:
        # sort by id in asc default
        transctions_query = transctions_query.order_by(Tour.id.asc())
    
    transctions_response = []
    for transction in transctions_query:
        transctions_response.append(transction.to_dict())

    return make_response(jsonify(transctions_response), 200)

# DELETE /booking/<customer_id>/transctions/<booking_id>
@bookings_bp.route("/<customer_id>/transctions/<booking_id>", methods=["DELETE"])