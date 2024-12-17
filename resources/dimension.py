import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import dimensions, bikes
from schema import DimensionSchema, DimensionUpdateSchema

blp = Blueprint("dimensions", __name__, description="Operations on dimensions")

@blp.route("/dimension/<string:dimension_id>")

class dimension(MethodView):
    @blp.response(200, DimensionSchema)
    def get(self, dimension_id=None):
        try:
            return dimensions[dimension_id]
        except KeyError:
            abort(404, message="dimension not found")    

    def delete(self, dimension_id):
        try:
            del dimensions[dimension_id]
            return {"message": "dimension deleted"}
        except KeyError:
            abort(404, message="dimension not found")

    @blp.arguments(DimensionUpdateSchema)
    @blp.response(200, DimensionSchema)
    def put(self, dimension_data, dimension_id):
        
        try:
            dimensions[dimension_id].update(**dimension_data)
            return dimensions[dimension_id]
        except KeyError:
            abort(
                404,
                message="Bad request. Dimensions not found"            
            )

@blp.route("/dimension")

class dimensionList(MethodView):
    @blp.response(200, DimensionSchema(many=True))
    def get(self):
     return dimensions.values() #This will return the dimension
    
    @blp.arguments(DimensionSchema)
    @blp.response(201, DimensionSchema)
    def post(self, dimension_data):

        if dimension_data["bike_id"] not in bikes:
            abort(404, message="Bike not found")

        for dimension in dimensions.values():
            if (
                dimension_data["bike_id"] == dimension["bike_id"]
            ):
                abort(
                    400,
                    message="Duplicate Bike Dimension."
                )

        dimension_id = uuid.uuid4().hex
        dimension = {**dimension_data, "dimension_id": dimension_id}

        dimensions[dimension_id] = dimension 
        return dimension