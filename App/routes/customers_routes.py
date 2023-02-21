from app import db
from app.models.tour import Tour
from app.models.booking import Booking
from app.models.customer import Customer
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from flask import Blueprint,jsonify, abort, make_response,request,session,redirect
from app.routes.helpers import validate_model




customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

#-------------------------------------------------------------------------------
#---------------------------- Helper Functions ---------------------------------
#-------------------------------------------------------------------------------
# def login_required(f):
#     """
#     Decorate routes to require login.
#     https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
#     """
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if session.get("user_id") is None:
#             return redirect("/login")
#         return f(*args, **kwargs)
#     return decorated_function
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

@customers_bp.route("/@user" , methods=["GET"])
def get_current_user():
    user_id = session.get("customer_id")

    if not user_id:
        return make_response(jsonify({"error": "Unauthorized"}), 401)
    
    user = Customer.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "email": user.email
    },) 

# POST /add customer
@customers_bp.route("/register", methods=["POST"])
def create_one_customer():
    # first create without hash passoword
    # customer_data = request.get_json()
    # new_customer = validate_request_and_create_entry(Customer, customer_data)

    # db.session.add(new_customer)
    # db.session.commit()
    # return make_response(new_customer.to_dict(), 201)
    
    # new -------------------------------------------------
    # customer_data = request.get_json()  //not sure why is not working?
    customer_name = request.json["name"]
    customer_email = request.json["email"]
    customer_phone = request.json["phone"]
    customer_password = request.json["password"]
    
    # check if user is exist
    customer_exist = Customer.query.filter_by(email=customer_email).first() is not None
    if customer_exist:
        return make_response(jsonify({"error": "User already exists"}), 409)
    
    #########################
    # without hash password #
    #########################
    new_customer = Customer(
            name = customer_name,
            email = customer_email,
            phone = customer_phone,
            password = customer_password
        )
    
    ######################
    # with hash password #
    ######################
    # hashed_password = generate_password_hash(customer_password)
    # # new_customer = validate_request_and_create_entry(Customer, customer_data)
    # new_customer = Customer(
    #         name = customer_name,
    #         email = customer_email,
    #         phone = customer_phone,
    #         password = hashed_password 
    #     )
    
    db.session.add(new_customer)
    db.session.commit()
    
    # remember the user 
    session["customer_id"] = new_customer.id
    
    return make_response(new_customer.to_dict(), 201)


# POST /get customer or # GET customers/<customer_id>
@customers_bp.route("/login", methods=["POST"])
def login_customer():
    
    session.clear()

    # checking for login
    try:
        email_data = request.json["email"]
        password_data = request.json["password"]
        
    except KeyError as e:
        abort(make_response(
            {"details": f"Request body must include {e.args[0]}."}, 400))
        
    # select password from customer where email='tt123@gmail.com';
    customer = Customer.query.filter_by(email=email_data).first()
    
    #########################
    # without hash password #
    #########################
    if customer is None or customer.password!= password_data:
        return make_response(jsonify({"error": "Unauthorized"}), 401) 
    
    ######################
    # with hash password #
    ######################
    # if customer is None or ( not
    #                         check_password_hash(customer.password, password_data)):
    #     return make_response(jsonify({"error": "Unauthorized"}), 401) 

    # remember the user 
    session["customer_id"] = customer.id
    print(session["customer_id"])
    
    return make_response(customer.to_dict(), 201)

# POST /logout
@customers_bp.route("/logout", methods=["POST"])
def logout_customer():
    session.clear()
    print(session)
    return make_response(jsonify({"message": "successful logout."}), 200)



# DELETE /customers/<customer_id>
@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_one_customer_by_id(customer_id):
    customer = validate_model(Customer, customer_id)

    db.session.delete(customer)
    db.session.commit()

    return make_response(jsonify({"message": f"customer #{customer.id} successfully deleted"}), 200)

