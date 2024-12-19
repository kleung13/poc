from db import db

class WorkoutModel(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    tss = db.Column(db.Integer)
    intensity_factor = db.Column(db.Float)
    kilojoules = db.Column(db.Integer)
    total_calories = db.Column(db.Float)
    carbs = db.Column(db.Float)
    protein = db.Column(db.Float)
    fat = db.Column(db.Float)
    