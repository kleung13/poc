from db import db

class DimensionTagModel(db.Model): #Check for Uniqueness for the tags
    __tablename__ = "dimension_tags"

    id = db.Column(db.Integer, primary_key=True)
    dimension_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("dimensions.id"))
    # db.UniqueConstraint("dimension_id", "tag_id", name="unique_dimension_tag")


