from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import TagModel, BikeModel, DimensionModel
from schema import TagSchema, TagUpdateSchema, TagAndDimensionSchema

blp = Blueprint("Tag", __name__, description="Operations on Tags")

@blp.route("/bike/<int:bike_id>/tag")

class TagsInBikes(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, bike_id):
        bike = BikeModel.query.get_or_404(bike_id)
        return bike.tags.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, bike_id):

        tag = TagModel(**tag_data, bike_id=bike_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A Tag already exists"
            )
        except SQLAlchemyError:
            abort(500, message="Error insering the tag")

        return tag

    @blp.arguments(TagUpdateSchema)
    @blp.response(200, TagSchema)
    def put(self, tag_data, tag_id):
        tag = TagModel.query.get(tag_id)
        if tag:
            tag.name = tag_data["name"]
        else:
            tag = TagModel(**tag_data, tag_id=tag_id)

        db.session.add(tag)
        db.session.commit()

        return tag
    

@blp.route("/tag")

class TagList(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self):
     return TagModel.query.all()
    

@blp.route("/tag/<int:tag_id>")

class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it.",
        example={"message": "Tag deleted"}
    )
    @blp.alt_response(404, description="Tag not found")
    @blp.alt_response(
        400,
        description="Returned if the tag is assinged to on or more Dimensions, in this case the tag is not deleted"
    )
   
    def delete(self, tag_id):

        tag = TagModel.query.get_or_404(tag_id)
        if not tag.dimensions:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag Deleted"}
        abort(
            400,
            message="Could not delete tag. Make sure tag is not associated with any dimensions"
        )

@blp.route("/dimension/<int:dimension_id>/tag/<int:tag_id>")
class LinkTagsToDimensions(MethodView):
    @blp.response(201, TagSchema)
    def post(self, dimension_id, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        dimension = DimensionModel.query.get_or_404(dimension_id)

        dimension.tags.append(tag)

        try:
            db.session.add(dimension)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag")

        return tag

    @blp.response(200, TagAndDimensionSchema)
    def delete(self, dimension_id, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        dimension = DimensionModel.query.get_or_404(dimension_id)

        if tag not in dimension.tags:
            abort(400, message="Tag not associated with the dimension")

        dimension.tags.remove(tag)

        try:
            # db.session.add(dimension)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()  # Roll back the session to prevent further issues
            print(str(e))  # Log the exception
            abort(500, message=f"An error occurred while removing the tag: {str(e)}")
        
        return {"message": "Dimension removed from tag", "Dimension": dimension, "Tag": tag}