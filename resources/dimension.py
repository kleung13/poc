from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from db import db
from models import DimensionModel
from schema import DimensionSchema, DimensionUpdateSchema

blp = Blueprint("dimensions", __name__, description="Operations on dimensions")

@blp.route("/dimension/<int:dimension_id>")

class dimension(MethodView):
    @blp.response(200, DimensionSchema)
    def get(self, dimension_id):
        dimension = DimensionModel.query.get_or_404(dimension_id)
        return dimension

    def delete(self, dimension_id):
        dimension = DimensionModel.query.get_or_404(dimension_id)
        db.session.delete(dimension)
        db.session.commit()
        return {"message": "Dimension Deleted"}

    @blp.arguments(DimensionUpdateSchema)
    @blp.response(200, DimensionSchema)
    def put(self, dimension_data, dimension_id):
        dimension = DimensionModel.query.get(dimension_id)
        if dimension:
            dimension.stack = dimension_data["stack"]
            dimension.reach = dimension_data["reach"]
            dimension.size = dimension_data["size"]
        else:
            dimension = DimensionModel(**dimension_data, dimension_id=dimension_id)

        db.session.add(dimension)
        db.session.commit()

        return dimension

@blp.route("/dimension")

class dimensionList(MethodView):
    @blp.response(200, DimensionSchema(many=True))
    def get(self):
     return DimensionModel.query.all()
    
    # @jwt_required()
    @blp.arguments(DimensionSchema)
    @blp.response(201, DimensionSchema)
    def post(self, dimension_data):
        dimension = DimensionModel(**dimension_data)

        try:
            db.session.add(dimension)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error insering the dimension")

        return dimension