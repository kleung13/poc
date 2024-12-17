import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import bikes
from schema import BikeSchema, BikeUpdateSchema

blp = Blueprint("bikes", __name__, description="Operations on bikes")

@blp.route("/bike/<string:bike_id>")

class Bike(MethodView):
    @blp.response(200, BikeSchema)
    def get(self, bike_id=None):
        try:
            return bikes[bike_id]
        except KeyError:
            abort(404, message="Bike not found")    

    def delete(self, bike_id):
        try:
            del bikes[bike_id]
            return {"message": "Bike deleted"}
        except KeyError:
            abort(404, message="Bike not found")

    @blp.arguments(BikeUpdateSchema)
    @blp.response(200, BikeSchema)
    def put(self, bike_data, bike_id):

        if bike_id not in bikes:
            abort(
                400,
                message="Bad request. Bike not found"            
            )

        bikes[bike_id].update(**bike_data)

        return bikes[bike_id]

@blp.route("/bike")

class BikeList(MethodView):
    @blp.response(200, BikeSchema(many=True))
    def get(self):
     return bikes.values() #This will return the bike
    
    @blp.arguments(BikeSchema)
    @blp.response(201, BikeSchema)
    def post(self, bike_data):
        
        for bike in bikes.values():
            if(
                bike_data["make"] == bike["make"]
                and bike_data["model"] == bike["model"]
            ):
                abort(
                    400,
                    message = "Duplicate Request"
                )

        bike_id = uuid.uuid4().hex
        bike = {**bike_data, "bike_id":bike_id}

        bikes[bike_id] = bike 
        return bike