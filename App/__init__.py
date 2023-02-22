from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    # app.url_map.strict_slashes = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # Configure session to use filesystem (instead of signed cookies)
    # app.config["SESSION_PERMANENT"] = False
    # app.config["SESSION_TYPE"] = "filesystem"

    if not test_config:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    
    # Import models here for Alembic setup
    from app.models.customer import Customer
    from app.models.tour import Tour
    from app.models.booking import Booking

    # Setup DB
    db.init_app(app)
    migrate.init_app(app, db)
    Session(app)

    # Register Blueprints here
    # from .routes import example_bp
    # app.register_blueprint(example_bp)

    from .routes.customers_routes import customers_bp
    app.register_blueprint(customers_bp)

    from .routes.tours_routes import tours_bp
    app.register_blueprint(tours_bp)

    from .routes.bookings_routes import bookings_bp
    app.register_blueprint(bookings_bp)

    CORS(app)

    return app
