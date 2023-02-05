from app import db
from app.models.tour import Tour
from app.models.booking import Booking
from app.models.customer import Customer
from flask import Blueprint, jsonify, abort, make_response, request

tours_bp = Blueprint("tours_bp", __name__, url_prefix="/tours")

# GET /tours
@tours_bp.route("", methods=["GET"])
def get_tours_optional_query():
    tours_query = Tour.query

    category_query = request.args.get("category")
    if category_query == "category":
        tours_query = tours_query.order_by(Tour.category.asc())

    city_query = request.args.get("city")
    if city_query == "city":
        tours_query = city_query.order_by(Tour.city.asc())

    tours = tours_query.all()

    tours_response = []
    for tour in tours:
        tours_response.append(tour.to_dict())

    return jsonify(tours_response)

# GET /tours/<id>
@tours_bp.route("/<tour_id>", methods=["GET"])
def get_tour_by_id(tour_id):
    tour_data = validate_model(Tour, tour_id)

    return tour_data.to_dict()


# POST /tours
@tours_bp.route("", methods=["POST"])
def create_tour():
    tour_data = request.get_json()

    # ###### refactor ######
    # if "title" not in tour_data.keys():
    #     abort(make_response({"details": f"Request body must include title."}, 400))
    # if "release_date" not in tour_data.keys():
    #     abort(make_response({"details": f"Request body must include release_date."}, 400))
    # if  "total_inventory" not in tour_data.keys():
    #     abort(make_response({"details": f"Request body must include total_inventory."}, 400))

    new_tour = Tour(
        name=tour_data["name"],
        city=tour_data["city"],
        address=tour_data["address"],
        date=tour_data["date"],
        duration_in_min=tour_data["duration_in_min"],
        price=tour_data["price"],
        category=tour_data["category"],
        is_outdoor=tour_data["outdoor"],
        capacity=tour_data["capacity"]
    )

    db.session.add(new_tour)
    db.session.commit()

    return make_response(jsonify(new_tour.to_dict()), 201)

# PUT /tours/<id>
@tours_bp.route("/<tour_id>", methods=["PUT"])
def update_tour_by_id(tour_id):
    pass
    #     tour = validate_model(Tour,tour_id)
    #     tour_data = request.get_json()

    #     # ###### refactor ######
    #     # if "title" not in tour_data.keys():
    #     #     abort(make_response({"details": f"Request body must include title."}, 400))
    #     # if "release_date" not in tour_data.keys():
    #     #     abort(make_response({"details": f"Request body must include release_date."}, 400))
    #     # if  "total_inventory" not in tour_data.keys():
    #     #     abort(make_response({"details": f"Request body must include total_inventory."}, 400))

    #     # tour.title = tour_data["title"]
    #     # tour.release_date =tour_data["release_date"]
    #     # tour.total_inventory = tour_data["total_inventory"]

    #     db.session.commit()

    #     return make_response(tour_data, 200)

# DELETE /tours/<id>
@tours_bp.route("/<tour_id>", methods=["DELETE"])
def delete_customer_by_id(tour_id):
    pass
    # tour_to_delete = validate_model(Tour,tour_id)
    # db.session.delete(tour_to_delete)
    # db.session.commit()

    # msg = f"Customer {tour_to_delete.id} successfully deleted"
    # return make_response(jsonify({"id":tour_to_delete.id, "message":msg}), 200)

# GET /id/bookings
@tours_bp.route("/<tour_id>/bookings", methods=["GET"])
def bookings_by_tour(tour_id):
    pass
    # tour = validate_model(Tour, tour_id)
    # # bookings = Booking.query.all()
    # bookings = Booking.query.filter(Booking.tour_id == tour.id).all()
    # customer_query = Customer.query

    # # sort queries for title and release date
    # sort_query = request.args.get("sort")

    # if sort_query == "name":
    #     customer_query = customer_query.order_by(Customer.name.asc())
    # elif sort_query == "postal_code":
    #     customer_query = customer_query.order_by(Customer.postal_code.asc())

    # #exception handling: page_num and count queries are invalid
    # try:
    #     page_num_query = int(request.args.get("page_num"))
    # except:
    #     page_num_query = None

    # try :
    #     count_query = int(request.args.get("count"))
    # except:
    #     count_query = None

    # if page_num_query and count_query:
    #     customers = customer_query.paginate(page = page_num_query, per_page = count_query).items
    # elif page_num_query:
    #     customers = customer_query.paginate(page = page_num_query).items
    # elif count_query:
    #     customers = customer_query.paginate(per_page = count_query).items
    # else:
    #     customers = customer_query.all()

    # # get bookings
    # customer_list = []
    # for booking in bookings:
    #     customer_list.append(Customer.query.get(booking.customer_id))

    # booking_response = []
    # for customer in customers:
    #     if customer in customer_list:
    #         booking_response.append(customer.to_dict())

    # return make_response(jsonify(booking_response), 200)

# DELETE /tours/<id>
@tours_bp.route("/<tour_id>", methods=["DELETE"])
def delete_customer_by_id(video_id):
    # video_to_delete = validate_model(Video,video_id)
    # db.session.delete(video_to_delete)
    # db.session.commit()

    # msg = f"Customer {video_to_delete.id} successfully deleted"
    # return make_response(jsonify({"id":video_to_delete.id, "message":msg}), 200)