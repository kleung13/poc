from db import db

class DimensionModel(db.Model):
    __tablename__ = "dimensions"

    id = db.Column(db.Integer, primary_key=True)
    