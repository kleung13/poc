from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

from blocklist import BLOCKLIST

from db import db
from models import UserModel
from schema import UserSchema

blp = Blueprint("User", __name__, description="Operations on Users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A User with that Username already exists"
            )

        return {"message": "User created successfully."}, 201
    
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(identity=str(user.id))
            # return {"access_token": access_token, "refresh_token": refresh_token}
            return {"access_token": access_token, "refresh_token": refresh_token}
        
        abort(401, message="Invalid username/password")

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)

        return {"message": "User logged out successfully."}

    
@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        return user
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError as e:
            print(str(e))  # Log the exception
            abort(500, message=f"An error occurred while removing the tag: {str(e)}")
        
        return {"message": "User deleted successfuly"}