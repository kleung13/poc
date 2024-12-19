from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from resources.calendar import Calendar
from resources.food import Food, Macros
from datetime import datetime

from db import db
from models import WorkoutModel
from schema import WorkoutSchema

blp = Blueprint("workouts", __name__, description="Operations on Workouts")

@blp.route("/workout/<int:workout_id>")

class Bike(MethodView):
    @blp.response(200, WorkoutSchema)
    def get(self, workout_id):
        workout = WorkoutModel.query.get_or_404(workout_id)
        return workout

    def delete(self, workout_id):
        workout = WorkoutModel.query.get_or_404(workout_id)
        db.session.delete(workout)
        db.session.commit()
        return {"message": "Workout Deleted"}

@blp.route('/workout')
class Workout(MethodView):
    @blp.response(200, WorkoutSchema(many=True))
    def get(self):
        return WorkoutModel.query.all() 
    
    @blp.arguments(WorkoutSchema)
    def post(self, workout_data):

        api_url = "https://intervals.icu/api/v1/athlete/0/events?category=WORKOUT&ext=zwo&resolve=true"
        password = workout_data["api_key"]

        calendar = Calendar(password, api_url)

        workouts = calendar.fetch_workouts()

        for workout in workouts:
            start_date_str = workout['start_date_local']
            start_date = datetime.fromisoformat(start_date_str)  # Convert to datetime object
            description = workout['workout_doc']['description']
            tss, intensity_factor, kilojoules = calendar.parse_description(description)
            food = Food(30, "male", 60, 178, kilojoules)
            total = food.daily_calories()
            macros = Macros(total, 40, 40, 20)
            carbs, protein, fat = macros.calculate_macros()            
            try:
                workout_data = WorkoutModel(
                        date=start_date,
                        tss=tss,
                        intensity_factor=intensity_factor,
                        kilojoules=kilojoules,
                        total_calories=total,
                        carbs=carbs,
                        protein=protein,
                        fat=fat                                
                )                
                db.session.add(workout_data)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                print(str(e))  
                abort(500, message=f"An error occurred while removing the tag: {str(e)}")

        return {"message": "Workouts imported successfully"}
