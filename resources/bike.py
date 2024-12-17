import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import BikeModel
from schema import BikeSchema, BikeUpdateSchema

blp = Blueprint("bikes", __name__, description="Operations on bikes")

@blp.route("/bike/<string:bike_id>")

class Bike(MethodView):
    @blp.response(200, BikeSchema)
    def get(self, bike_id=None):
        bike = BikeModel.query.get_or_404(bike_id)
        return bike
    
    def delete(self, bike_id):
        bike = BikeModel.query.get_or_404(bike_id)
        db.session.delete(bike)
        db.session.commit()
        return {"message": "Bike Deleted"}

    @blp.arguments(BikeUpdateSchema)
    @blp.response(200, BikeSchema)
    def put(self, bike_data, bike_id):
        bike = BikeModel.query.get_or_404(bike_id)
        raise NotImplementedError("Updating a bike is not implemented")

@blp.route("/bike")

class BikeList(MethodView):
    @blp.response(200, BikeSchema(many=True))
    def get(self):
     return BikeModel.query.all()
    
    @blp.arguments(BikeSchema)
    @blp.response(201, BikeSchema)
    def post(self, bike_data):

        bike = BikeModel(**bike_data)

        try:
            db.session.add(bike)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A Bike Make/Model already exists"
            )
        except SQLAlchemyError:
            abort(500, message="Error insering the bike")

        return bike