from flask import abort, make_response, request
from app.models.tour import Tour
from app.models.booking import Booking
from app.models.customer import Customer

def get_all(records):
    response = []
    for record in records:
        response.append(record.to_dict())
    return response

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))
    model = cls.query.get(model_id)
    if model:
        return model 
    abort(make_response({"message": f"{cls.__name__} {model_id} was not found"}, 404))



def validate_request_and_create_entry(cls, request_data):
    try:
        new_obj = cls.from_dict(request_data)
    except KeyError as e:
        abort(make_response(
            {"details": f"Request body must include {e.args[0]}."}, 400))
    return new_obj


def pagination_helper(page_num_query, count_query, query, get_all):
    try:
        page_num_query = int(request.args.get("page_num"))
    except:
        page_num_query = None

    try :
        count_query = int(request.args.get("count"))
    except:
        count_query = None

    if page_num_query and count_query:
        query = query.paginate(page = page_num_query, per_page = count_query).items
    elif page_num_query:
        query = query.paginate(page = page_num_query).items
    elif count_query:
        query = query.paginate(per_page = count_query).items
    else:
        query = query.all()
    return get_all(query)


def get_all_tours_bookings_customers_helper(customer_list):
    customer_response = []
    for customer in customer_list:
        customer_response.append(
            customer.to_dict()
        )
    return customer_response
