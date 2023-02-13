from app import db
from app import bcrypt
from app.models.tour import Tour
from app.models.booking import Booking
from app.models.customer import Customer
# from flask_session import Session
from flask import Blueprint, jsonify, abort, make_response, request
from app.routes.helpers import validate_model,validate_request_and_create_entry


customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

### how Session tracking user_ID when user login

# POST /add customer
@customers_bp.route("/register", methods=["POST"])
def create_one_customer():
    customer_data = request.get_json()
    new_customer = validate_request_and_create_entry(Customer, customer_data)
    new_customer.password = bcrypt.generate_password_hash(customer_data["password"])
    db.session.add(new_customer)
    db.session.commit()
    return make_response(new_customer.to_dict(), 201)


# POST /get customer or # GET customers/<customer_id>
# @customers_bp.route("/login", methods=["GET, POST"])



# POST /logout
# @app.route("/logout", methods=["POST"])



# DELETE /customers/<customer_id>
customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_one_customer_by_id(customer_id):
    customer = validate_model(Customer, customer_id)

    db.session.delete(customer)
    db.session.commit()

    return make_response(jsonify({"message": f"customer #{customer.id} successfully deleted"}), 200)


#--------------------------------------------------------------------
#--------------------------------------------------------------------
#--------------------------------------------------------------------
#--------------------------------------------------------------------
#--------------------------------------------------------------------

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     """Log user in"""
#     # Forget any user_id
#     session.clear()

#     # User reached route via POST (as by submitting a form via POST)
#     if request.method == "POST":

#         # Ensure username was submitted
#         if not request.form.get("username"):
#             return apology("must provide username", 403)

#         # Ensure password was submitted
#         elif not request.form.get("password"):
#             return apology("must provide password", 403)

#         # Query database for username
#         rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

#         # Ensure username exists and password is correct
#         if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
#             return apology("invalid username and/or password", 403)

#         # Remember which user has logged in
#         session["user_id"] = rows[0]["id"]

#         # Redirect user to home page
#         return redirect("/")

#     # User reached route via GET (as by clicking a link or via redirect)
#     else:
#         return render_template("login.html")
    
    
    
    
# @app.route("/logout")
# def logout():
#     """Log user out"""

#     # Forget any user_id
#     session.clear()

#     # Redirect user to login form
#     return redirect("/")


# @app.route("/quote", methods=["GET", "POST"])
# @login_required
# def quote():
#     """Get stock quote."""
#     if request.method == "POST":
#         symbol = request.form.get("symbol")
#         item = lookup(symbol)
#         if item is None or not item:
#             return apology("Please enter valid stock symbol.")
#         else:
#             return render_template("quoted.html",item=item, usd_function = usd )
#     else:
#         return render_template("quote.html")
    
    


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     """Register user"""
#     if request.method == "POST":
#         username = request.form.get("username")
#         password = request.form.get("password")
#         confirmation = request.form.get("confirmation")
#         data_username = db.execute('''SELECT username FROM users WHERE username=?''',username)


#         if not username:
#             return apology("Please enter the username.")
#         elif data_username:
#             return apology("Username already exist.")
#         elif not password:
#             return apology("Please enter the password.")
#         elif not confirmation:
#             return apology("Please enter the confirmation.")
#         elif password != confirmation:
#             return apology("Paasword and confirmation do not match.")
#         else:
#             hashed_password = generate_password_hash(password)
#             db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashed_password)

#         return redirect("login")
#     else:
#         return render_template("register.html")