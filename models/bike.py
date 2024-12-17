from db import db

class BikeModel(db.Model):
    __tablename__ = "bikes"

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String, nullable=False)
    model = db.Column(db.String, unique=True, nullable=False)
    dimensions = db.relationship("DimensionModel", back_populates="bike", lazy="dynamic", cascade="all, delete")# Check delete-orphan documentation