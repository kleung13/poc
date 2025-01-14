from db import db

class UserProfileModel(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)
    profile = db.relationship("UserModel", back_populates="profile")
    # weight = db.Column(db.Integer, nullable=False)
    # height = db.Column(db.Float, nullable=False)