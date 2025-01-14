import os
from datetime import datetime
from dotenv import load_dotenv

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from sqlalchemy.ext.declarative import declarative_base
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy

from db import db
# from blocklist import BLOCKLIST
from resources.calendar import Calendar

from resources.bike import blp as BikeBlueprint
from resources.dimension import blp as DimensionBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from resources.workout import blp as WorkoutBlueprint
from resources.profile import blp as ProfileBlueprint

load_dotenv()

calendar = Calendar(os.getenv("API_KEY"), os.getenv("BASE_URL"))
start_date = datetime(2024, 12, 19)
end_date = datetime(2024, 12, 22)

workouts = calendar.fetch_workouts()
# print(f"{workouts}")
# x = calendar.parse_description(workouts['workout_doc']['description'])
# print(f"{x}")
wcal = calendar.filter_workouts_by_date(workouts, start_date, end_date)
# Initialize Cloud SQL Connector
connector = Connector()

# Function to create a database connection using the Google Cloud SQL Connector
def getconn():
    return connector.connect(
        os.getenv("INSTANCE_CONNECTION_NAME"),  # Format: "project:region:instance-name"
        "pg8000",  # Driver
        user=os.getenv("DB_USER"),  # Database user
        password=os.getenv("DB_PASSWORD"),  # Database password
        db=os.getenv("DB_NAME"),  # Database name
        ip_type=IPTypes.PUBLIC if os.getenv("USE_PRIVATE_IP", "false").lower() != "true" else IPTypes.PRIVATE,
    )

def create_app(db_url=None):

    # load_dotenv()

    app = Flask(__name__)

    # App configuration
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Bike REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

    # Configure SQLAlchemy
    if db_url:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+pg8000://"
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"creator": getconn}
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    # JWT Configuration
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt = JWTManager(app)

    # @jwt.token_in_blocklist_loader
    # def check_if_token_in_blocklist(jwt_header, jwt_payload):
    #     return jwt_payload["jti"] in BLOCKLIST

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    # Register blueprints
    api.register_blueprint(BikeBlueprint)
    api.register_blueprint(DimensionBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(WorkoutBlueprint)
    api.register_blueprint(ProfileBlueprint)

    return app
