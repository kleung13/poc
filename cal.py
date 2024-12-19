import os
from datetime import datetime
from dotenv import load_dotenv
from resources.calendar import Calendar
from resources.food import Food, Macros

load_dotenv()

calendar = Calendar(os.getenv("API_KEY"), os.getenv("BASE_URL"))
start_date = datetime(2024, 12, 19)
end_date = datetime(2024, 12, 22)

workouts = calendar.fetch_workouts()

# print(f"{workouts}")
# x = calendar.parse_description(workouts['workout_doc']['description'])
# print(f"{x}")
wcal = calendar.filter_workouts_by_date(workouts, start_date, end_date)
# print(wcal)

workout_results = []

for workout in workouts:
    description = workout['workout_doc']['description']
    tss, intensity_factor, kilojoules = calendar.parse_description(description)
    start_date = workout['start_date_local']
    food = Food(30, "male", 60, 178, kilojoules)
    total = food.daily_calories()
    macros = Macros(total, 40, 40, 20)
    carbs, protein, fat = macros.calculate_macros()
    # date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S").date()
    workout_results.append({
    "date": start_date,
    "tss": tss,
    "intensity_factor": intensity_factor,
    "kilojoules": kilojoules,
    "total_calories": total,
    "carbs": carbs,
    "protein": protein,
    "fat": fat        
     })

print(workout_results)
    # calendar.save_to_db(tss, intensity_factor, kilojoules)
    # print(f"TSS: {tss}, IF: {intensity_factor}, kJ(Cal): {kilojoules}")
    # print(f"Name: {workout['name']}")
    # print(f"Description: {workout['workout_doc']['description']}")
    # print(f"Start: {workout['start_date_local']}")
    # print(f"End: {workout['end_date_local']}\n")