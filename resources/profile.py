from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
# from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

# from blocklist import BLOCKLIST

from db import db
from models import UserProfileModel
from schema import UserProfileSchema

blp = Blueprint("profiles", __name__, description="Operations on profiles")


# @blp.route("/profile/<int:profile_id>")

# class Profile(MethodView):
#     @blp.response(200, UserProfileSchema)
#     def get(self, profile_id=None):
#         profile = UserProfileModel.query.get_or_404(profile_id)
#         return profile
    
#     def delete(self, profile_id):
#         profile = UserProfileModel.query.get_or_404(profile_id)
#         db.session.delete(profile)
#         db.session.commit()
#         return {"message": "Profile Deleted"}

#     @blp.response(200, UserProfileSchema)
#     def put(self, profile_data, profile_id):
#         profile = UserProfileModel.query.get(profile_id)
#         if profile:
#             profile.age = profile_data["age"]
#             profile.gender = profile_data["gender"]
#         else:
#             profile = UserProfileModel(**profile_data, profile_id=profile_id)

#         db.session.add(profile)
#         db.session.commit()

#         return profile

@blp.route("/profile")

class ProfileList(MethodView):
    @blp.response(200, UserProfileSchema(many=True))
    def get(self):
     return UserProfileModel.query.all()
    
    @blp.arguments(UserProfileSchema)
    @blp.response(201, UserProfileSchema)
    def post(self, profile_data):

        profile = UserProfileModel(**profile_data)

        try:
            db.session.add(profile)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A Profile already exists"
            )
        except SQLAlchemyError:
            abort(500, message="Error insering the profile")

        return profile    