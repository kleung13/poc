from db import db

class DimensionModel(db.Model):
    __tablename__ = "dimensions"

    id = db.Column(db.Integer, primary_key=True)
    stack = db.Column(db.Integer, nullable=False)
    reach = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String, nullable=False)
    bike_id = db.Column(db.Integer, db.ForeignKey("bikes.id"), unique=False, nullable=False)
    bike = db.relationship("BikeModel", back_populates="dimensions")
    tags = db.relationship("TagModel", back_populates="dimensions", secondary="dimension_tags")