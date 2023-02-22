from app import db
from app.models.tour import Tour
from app.models.booking import Booking
from app.models.customer import Customer
from flask import Blueprint, jsonify, abort, make_response, request
from app.routes.helpers import get_all, pagination_helper, validate_model
from datetime import datetime, timedelta
from datetime import datetime, date

tours_bp = Blueprint("tours_bp", __name__, url_prefix="/tours")

#-------------------------------------------------------------------------------
# ------------------------------ Routes ----------------------------------------
#-------------------------------------------------------------------------------
# GET /tours (get all tours and limit showing 6 for each call)
# ( query by => city / category / date / is_outdoor )
@tours_bp.route("", methods=["GET"])
def get_tours_optional_query():
    tours_query = Tour.query
    
    # Filter Queries
    category_query = request.args.getlist("category")
    city_query = request.args.getlist("city")
    print(city_query)
    is_outdoor_query = request.args.getlist("is_outdoor")
    date_query = request.args.get("date")

    if date_query:
        date_query = datetime.strptime(date_query, ("%m/%d/%Y"))
        tours_query = tours_query.filter_by(date=date_query)
    if category_query: 
        print(category_query)
        tours_query = tours_query.filter(Tour.category.in_(category_query))
    if city_query:
        tours_query = tours_query.filter(Tour.city.in_(city_query))
    if is_outdoor_query:
        tours_query = tours_query.filter(Tour.is_outdoor.in_(is_outdoor_query))

    if not tours_query:
        tours_query = tours_query.all()

    # Pagination queries
    count_query = request.args.get("count")
    page_num_query = request.args.get("page_num")
    tours_response = pagination_helper(
        page_num_query, count_query, tours_query, get_all)

    return make_response(jsonify(tours_response), 200)


# GET /tours/<tour_id> (get a tour by tour_id )
@tours_bp.route("/<tour_id>", methods=["GET"])
def get_tour_by_id(tour_id):
    tour_data = validate_model(Tour, tour_id)

    return make_response(jsonify(tour_data.to_dict()), 200)


# POST /tours (create tour)
@tours_bp.route("", methods=["POST"])
def create_tour():
    tour_data = request.get_json()
    try:
        new_tour = Tour.from_dict(tour_data)
    except KeyError as e:
        abort(make_response({"details": f"Request body must include {e[0]}"}, 400))

    db.session.add(new_tour)
    db.session.commit()

    return make_response(jsonify(new_tour.to_dict()), 201)


# PUT /tours/<tour_id>  (optional)
@tours_bp.route("/<tour_id>", methods=["PUT"])
def update_tour_by_id(tour_id):
    tour = validate_model(Tour, tour_id)
    tour_data = request.get_json()
    
    try:
        tour.name=tour_data["name"]
        tour.city=tour_data["city"]
        tour.address=tour_data["address"]
        tour.date=tour_data["date"]
        tour.duration_in_min=tour_data["duration_in_min"]
        tour.price=tour_data["price"]
        tour.category=tour_data["category"]
        tour.is_outdoor=tour_data["is_outdoor"]
        tour.capacity=tour_data["capacity"]
        tour.description=tour_data["description"]
        tour.photo_url=tour_data["photo_url"],
        tour.time = tour_data["time"]
    except KeyError as e:
        abort(make_response({"details": f"Request boy must include {e[0]}"}, 400))
    db.session.commit()

    return make_response(jsonify(tour.to_dict()), 200)



# DELETE /tours/<tours_id>
@tours_bp.route("/<tour_id>", methods=["DELETE"])
def delete_customer_by_id(tour_id):
    tour_to_delete = validate_model(Tour,tour_id)
    db.session.delete(tour_to_delete)
    db.session.commit()

    msg = f"Tour {tour_to_delete.id} successfully deleted"
    return make_response(jsonify({"id":tour_to_delete.id, "message":msg}), 200)



# GET /id/bookings    (no need)
@tours_bp.route("/<tour_id>/bookings", methods=["GET"])
def bookings_by_tour(tour_id):
    tour = validate_model(Tour, tour_id)

    bookings = Booking.query.filter(Booking.tour_id == tour.id).all()
    customer_query = Customer.query

    sort_query = request.args.get("sort")

    if sort_query == "name":
        customer_query = customer_query.order_by(Customer.name.asc())

    count_query = request.args.get("count")
    page_num_query = request.args.get("page_num")
    customers = pagination_helper(page_num_query, count_query, sort_query, get_all)

    # get bookings
    customer_list = []
    for booking in bookings:
        customer_list.append(Customer.query.get(booking.customer_id))
    
    booking_response = []
    for customer in customers:
        if customer in customer_list:
            booking_response.append(customer.to_dict())

    return make_response(jsonify(booking_response), 200)
