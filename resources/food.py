import requests, re
from datetime import datetime



class Food:
    def __init__(self, age, gender, weight, height, excercise_calories):
        self.age = age
        self.gender = gender
        self.weight = weight
        self.height = height
        self.excercise_calories = excercise_calories

    def calculate_bmr(self):
        if self.gender == "male":
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        elif self.gender == "female":
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age + 161
        return bmr
    
    def daily_calories(self):
        bmr = self.calculate_bmr()
        excercise_calories = self.excercise_calories
        total_cals = bmr + excercise_calories
        return float(total_cals)

class Macros:
    def __init__(self, total_calories, carb_percentage, protein_percentage, fat_percentage):
        if carb_percentage + protein_percentage + fat_percentage != 100:
            raise ValueError("Sum of macro's is not 100")
    
        self.total_calories = total_calories
        self.carbs = carb_percentage
        self.protein = protein_percentage
        self.fat = fat_percentage

    def calculate_macros(self):
        carb_calories = (self.carbs/ 100) * self.total_calories
        protein_calories = (self.protein / 100) * self.total_calories
        fat_calories = (self.fat / 100) * self.total_calories

        carbs_grams = carb_calories / 4  # 1g carbs = 4 calories
        protein_grams = protein_calories / 4  # 1g protein = 4 calories
        fat_grams = fat_calories / 9  # 1g fat = 9 calories

        return float(round(carbs_grams, 2)), float(round(protein_grams,2)), float(round(fat_grams,2))
        # return {
        #     "carbs": round(carbs_grams, 2),
        #     "protein": round(protein_grams, 2),
        #     "fat": round(fat_grams, 2),
        # }