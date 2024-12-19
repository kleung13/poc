from db import db

class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    bike_id = db.Column(db.Integer, db.ForeignKey("bikes.id"), nullable=False)

    bike = db.relationship("BikeModel", back_populates="tags")
    dimensions = db.relationship("DimensionModel", back_populates="tags", secondary="dimension_tags")
